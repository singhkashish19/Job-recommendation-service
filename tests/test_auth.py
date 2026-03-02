import pytest
from fastapi import status


class TestAuthentication:
    """Test authentication endpoints"""

    def test_signup_success(self, client, test_user_data):
        """Test successful user signup"""
        response = client.post(
            "/signup",
            json=test_user_data
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["username"] == test_user_data["username"]
        assert "id" in response.json()

    def test_signup_duplicate_username(self, client, test_user_data):
        """Test signup with duplicate username"""
        # First signup
        client.post("/signup", json=test_user_data)
        
        # Second signup with same username
        response = client.post("/signup", json=test_user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]

    def test_signup_invalid_username(self, client):
        """Test signup with invalid username"""
        response = client.post(
            "/signup",
            json={"username": "ab", "password": "password123"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_signup_invalid_password(self, client):
        """Test signup with invalid password"""
        response = client.post(
            "/signup",
            json={"username": "testuser", "password": "123"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_success(self, client, test_user_data):
        """Test successful login"""
        # Create user
        client.post("/signup", json=test_user_data)
        
        # Login
        response = client.post("/login", json=test_user_data)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client, test_user_data):
        """Test login with invalid credentials"""
        # Create user
        client.post("/signup", json=test_user_data)
        
        # Try login with wrong password
        response = client.post(
            "/login",
            json={
                "username": test_user_data["username"],
                "password": "wrongpassword"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post(
            "/login",
            json={"username": "nonexistent", "password": "password123"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
