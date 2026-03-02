import logging
from fastapi import APIRouter, Request, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
import numpy as np

from app.schemas import MatchRequest, MatchResult, JobOut
from app.services.embeddings import EmbeddingService
from app.auth import get_current_user
from app.db import get_db
from app import models

logger = logging.getLogger(__name__)

router = APIRouter(tags=["matching"])
embedder = EmbeddingService()


def cosine_sim(a: np.ndarray, b: np.ndarray):
    """Calculate cosine similarity between two vectors"""
    a = a / (np.linalg.norm(a) + 1e-9)
    b = b / (np.linalg.norm(b) + 1e-9)
    return float(np.dot(a, b))


@router.post("/match", response_model=List[MatchResult])
def match(
    req: MatchRequest,
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Rank and match jobs to user's resume
    
    Supports two modes:
    - **resume_id**: Use stored resume from database
    - **resume_text**: Use inline resume text for one-off matching
    
    Returns top_k jobs ranked by similarity score (0-1)
    """
    try:
        # Determine resume text source
        resume_text = None
        resume_id = None

        if req.resume_id:
            # Use stored resume
            resume = db.query(models.Resume).filter(
                models.Resume.id == req.resume_id,
                models.Resume.user_id == current_user.id
            ).first()
            
            if not resume:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Resume not found"
                )
            resume_text = resume.resume_text
            resume_id = resume.id
        elif req.resume_text:
            # Use inline resume text
            resume_text = req.resume_text
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either resume_id or resume_text must be provided"
            )

        jobs = request.app.state.jobs if hasattr(request.app.state, "jobs") else []
        
        if not jobs:
            logger.warning(f"No jobs available for matching (user: {current_user.id})")
            return []

        # Generate embeddings
        texts = [job.get("description") or job.get("title") or "" for job in jobs]
        job_embs = embedder.embed(texts)
        resume_emb = embedder.embed([resume_text])[0]
        
        # Calculate similarity scores
        scores = [cosine_sim(resume_emb, j) for j in job_embs]
        ranked_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[: req.top_k]
        
        results = []
        for i in ranked_idx:
            job = jobs[i]
            score = scores[i]
            results.append(MatchResult(job=JobOut(**job), score=score))
            
            # Save match record to database
            try:
                db_match = models.Match(
                    user_id=current_user.id,
                    job_id=job.get("id"),
                    similarity_score=score
                )
                db.add(db_match)
            except Exception as e:
                logger.warning(f"Failed to record match: {str(e)}")
                # Don't fail the request if match recording fails
        
        db.commit()
        logger.info(f"Match completed for user {current_user.id}: {len(results)} results")
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error during matching for user {current_user.id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Matching failed"
        )

