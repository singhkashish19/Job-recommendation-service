import pytest
from fastapi import status


class TestMatching:
    """Test job matching endpoints"""

    @pytest.fixture
    def authenticated_client(self, client, test_user_data):
        """Get authenticated client with token"""
        # Create user
        client.post("/signup", json=test_user_data)
        
        # Login
        response = client.post("/login", json=test_user_data)
        token = response.json()["access_token"]
        
        # Add auth header to client
        client.headers = {"Authorization": f"Bearer {token}"}
        return client

    def test_match_unauthenticated(self, client):
        """Test matching without authentication"""
        response = client.post(
            "/match",
            json={
                "resume_text": "Python developer with 5 years experience",
                "top_k": 5
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_match_with_inline_resume(self, authenticated_client, test_resume):
        """Test matching with inline resume text"""
        response = authenticated_client.post(
            "/match",
            json={
                "resume_text": test_resume["resume_text"],
                "top_k": 5
            },
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_200_OK
        results = response.json()
        assert isinstance(results, list)
        assert len(results) <= 5

    def test_match_with_stored_resume(self, authenticated_client, test_resume):
        """Test matching with stored resume"""
        # Upload resume
        resume_response = authenticated_client.post(
            "/resumes",
            json=test_resume,
            headers=authenticated_client.headers
        )
        resume_id = resume_response.json()["id"]
        
        # Match using stored resume
        response = authenticated_client.post(
            "/match",
            json={
                "resume_id": resume_id,
                "top_k": 5
            },
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_200_OK
        results = response.json()
        assert isinstance(results, list)

    def test_match_with_invalid_resume_id(self, authenticated_client):
        """Test matching with invalid resume ID"""
        response = authenticated_client.post(
            "/match",
            json={
                "resume_id": 9999,
                "top_k": 5
            },
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_match_no_resume_text_or_id(self, authenticated_client):
        """Test matching without resume text or ID"""
        response = authenticated_client.post(
            "/match",
            json={"top_k": 5},
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_match_response_format(self, authenticated_client, test_resume):
        """Test matching response format"""
        response = authenticated_client.post(
            "/match",
            json={
                "resume_text": test_resume["resume_text"],
                "top_k": 5
            },
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_200_OK
        
        results = response.json()
        if len(results) > 0:
            result = results[0]
            assert "job" in result
            assert "score" in result
            assert 0.0 <= result["score"] <= 1.0
            
            job = result["job"]
            assert "id" in job
            assert "title" in job

    def test_match_top_k_parameter(self, authenticated_client, test_resume):
        """Test top_k parameter"""
        response = authenticated_client.post(
            "/match",
            json={
                "resume_text": test_resume["resume_text"],
                "top_k": 3
            },
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_200_OK
        results = response.json()
        assert len(results) <= 3

    def test_match_results_ranked(self, authenticated_client, test_resume):
        """Test that results are properly ranked"""
        response = authenticated_client.post(
            "/match",
            json={
                "resume_text": test_resume["resume_text"],
                "top_k": 10
            },
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_200_OK
        results = response.json()
        
        if len(results) > 1:
            # Check that scores are in descending order
            scores = [result["score"] for result in results]
            assert scores == sorted(scores, reverse=True)

    def test_match_invalid_top_k(self, authenticated_client, test_resume):
        """Test with invalid top_k value"""
        response = authenticated_client.post(
            "/match",
            json={
                "resume_text": test_resume["resume_text"],
                "top_k": 100
            },
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
