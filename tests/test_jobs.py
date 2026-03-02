import pytest
from fastapi import status


class TestJobs:
    """Test jobs management endpoints"""

    def test_list_jobs_no_params(self, client):
        """Test getting jobs without parameters"""
        response = client.get("/jobs")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_list_jobs_with_pagination(self, client):
        """Test getting jobs with pagination"""
        response = client.get("/jobs?skip=0&limit=5")
        assert response.status_code == status.HTTP_200_OK
        jobs = response.json()
        assert isinstance(jobs, list)
        assert len(jobs) <= 5

    def test_list_jobs_pagination_skip(self, client):
        """Test pagination with skip"""
        # Get first page
        response1 = client.get("/jobs?skip=0&limit=5")
        jobs1 = response1.json()
        
        # Get second page
        response2 = client.get("/jobs?skip=5&limit=5")
        jobs2 = response2.json()
        
        # Ensure different results (if enough jobs exist)
        if len(jobs1) > 0 and len(jobs2) > 0:
            assert jobs1[0]["id"] != jobs2[0]["id"]

    def test_list_jobs_invalid_limit(self, client):
        """Test with invalid limit"""
        response = client.get("/jobs?skip=0&limit=200")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_list_jobs_negative_skip(self, client):
        """Test with negative skip"""
        response = client.get("/jobs?skip=-1&limit=10")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_list_jobs_zero_limit(self, client):
        """Test with zero limit"""
        response = client.get("/jobs?skip=0&limit=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_jobs_response_format(self, client):
        """Test jobs response format"""
        response = client.get("/jobs?skip=0&limit=1")
        assert response.status_code == status.HTTP_200_OK
        
        jobs = response.json()
        if len(jobs) > 0:
            job = jobs[0]
            assert "id" in job
            assert "title" in job
            assert "company" in job or "description" in job
