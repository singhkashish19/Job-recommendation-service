import pytest
from fastapi import status


class TestResumes:
    """Test resume management endpoints"""

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

    def test_upload_resume_unauthenticated(self, client, test_resume):
        """Test uploading resume without authentication"""
        response = client.post(
            "/resumes",
            json=test_resume
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_upload_resume_success(self, authenticated_client, test_resume):
        """Test successful resume upload"""
        response = authenticated_client.post(
            "/resumes",
            json=test_resume,
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["resume_text"] == test_resume["resume_text"]
        assert "id" in response.json()

    def test_upload_resume_invalid_length(self, authenticated_client):
        """Test resume with invalid length"""
        response = authenticated_client.post(
            "/resumes",
            json={"resume_text": "short"},
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_resume(self, authenticated_client, test_resume):
        """Test getting user's resume"""
        # Upload resume
        authenticated_client.post(
            "/resumes",
            json=test_resume,
            headers=authenticated_client.headers
        )
        
        # Get resume
        response = authenticated_client.get(
            "/resumes",
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["resume_text"] == test_resume["resume_text"]

    def test_get_resume_not_found(self, authenticated_client):
        """Test getting resume when none exists"""
        response = authenticated_client.get(
            "/resumes",
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_resume(self, authenticated_client, test_resume):
        """Test updating resume"""
        # Upload initial resume
        authenticated_client.post(
            "/resumes",
            json=test_resume,
            headers=authenticated_client.headers
        )
        
        # Update resume
        new_resume = {"resume_text": test_resume["resume_text"] + " Additional experience..."}
        response = authenticated_client.put(
            "/resumes",
            json=new_resume,
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["resume_text"] == new_resume["resume_text"]

    def test_delete_resume(self, authenticated_client, test_resume):
        """Test deleting resume"""
        # Upload resume
        authenticated_client.post(
            "/resumes",
            json=test_resume,
            headers=authenticated_client.headers
        )
        
        # Delete resume
        response = authenticated_client.delete(
            "/resumes",
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's deleted
        response = authenticated_client.get(
            "/resumes",
            headers=authenticated_client.headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
