import logging
from fastapi import APIRouter, Request, Query
from typing import List

from app.schemas import JobOut

logger = logging.getLogger(__name__)

router = APIRouter(tags=["jobs"])


@router.get("/jobs", response_model=List[JobOut])
def list_jobs(
    request: Request,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return")
):
    """
    Get paginated list of jobs
    
    - **skip**: number of records to skip (default: 0)
    - **limit**: number of records to return, max 100 (default: 10)
    """
    jobs = request.app.state.jobs if hasattr(request.app.state, "jobs") else []
    
    total = len(jobs)
    paginated_jobs = jobs[skip:skip + limit]
    
    logger.info(f"Retrieved jobs: skip={skip}, limit={limit}, total={total}, returned={len(paginated_jobs)}")
    
    return paginated_jobs

