import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.schemas import ResumeCreate, ResumeOut, ResumeUpdate
from app.auth import get_current_user
from app.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("", response_model=ResumeOut, status_code=status.HTTP_201_CREATED)
def upload_resume(
    resume_data: ResumeCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload or update user resume"""
    try:
        # Check if user already has a resume
        existing_resume = db.query(models.Resume).filter(
            models.Resume.user_id == current_user.id
        ).first()

        if existing_resume:
            existing_resume.resume_text = resume_data.resume_text
            db.commit()
            db.refresh(existing_resume)
            logger.info(f"Resume updated for user {current_user.id}")
            return existing_resume
        else:
            db_resume = models.Resume(
                user_id=current_user.id,
                resume_text=resume_data.resume_text
            )
            db.add(db_resume)
            db.commit()
            db.refresh(db_resume)
            logger.info(f"Resume created for user {current_user.id}")
            return db_resume
    except Exception as e:
        db.rollback()
        logger.error(f"Error uploading resume for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload resume"
        )


@router.get("", response_model=ResumeOut)
def get_resume(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user's resume"""
    resume = db.query(models.Resume).filter(
        models.Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found. Please upload a resume first."
        )
    return resume


@router.put("", response_model=ResumeOut)
def update_resume(
    resume_data: ResumeUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user's resume"""
    try:
        resume = db.query(models.Resume).filter(
            models.Resume.user_id == current_user.id
        ).first()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        resume.resume_text = resume_data.resume_text
        db.commit()
        db.refresh(resume)
        logger.info(f"Resume updated for user {current_user.id}")
        return resume
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating resume for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update resume"
        )


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete user's resume"""
    try:
        resume = db.query(models.Resume).filter(
            models.Resume.user_id == current_user.id
        ).first()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        db.delete(resume)
        db.commit()
        logger.info(f"Resume deleted for user {current_user.id}")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting resume for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete resume"
        )
