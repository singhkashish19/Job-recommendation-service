from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=128, description="Username")
    password: str = Field(..., min_length=6, max_length=256, description="Password must be at least 6 characters")


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeCreate(BaseModel):
    resume_text: str = Field(..., min_length=10, max_length=50000, description="Resume text (10-50000 characters)")


class ResumeUpdate(BaseModel):
    resume_text: str = Field(..., min_length=10, max_length=50000, description="Resume text (10-50000 characters)")


class ResumeOut(BaseModel):
    id: int
    user_id: int
    resume_text: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobOut(BaseModel):
    id: int
    title: str
    company: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class MatchRequest(BaseModel):
    top_k: int = Field(5, ge=1, le=50, description="Number of top matches to return (1-50)")
    resume_id: Optional[int] = Field(None, description="Resume ID from database (if not provided, uses request body text)")
    resume_text: Optional[str] = Field(None, max_length=50000, description="Resume text for one-off matching")

    class Config:
        json_schema_extra = {
            "example": {
                "top_k": 5,
                "resume_id": None,
                "resume_text": "Python developer with 5 years of experience..."
            }
        }


class MatchResult(BaseModel):
    job: JobOut
    score: float = Field(..., ge=0.0, le=1.0, description="Cosine similarity score")

    class Config:
        from_attributes = True


class MatchRecord(BaseModel):
    id: int
    user_id: int
    job_id: int
    similarity_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(10, ge=1, le=100, description="Number of records to return (1-100)")
