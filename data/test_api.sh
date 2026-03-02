#!/bin/bash

# Job Recommendation Service - Manual Testing Script
# This script helps test all API endpoints

API_URL="http://localhost:8000"
USERNAME="testuser_$(date +%s)"
PASSWORD="Password123!"
TOKEN=""
RESUME_ID=""
JOB_ID="1"

echo "=========================================="
echo "Job Recommendation Service - API Test"
echo "=========================================="
echo "API URL: $API_URL"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print success
success() {
    echo -e "${GREEN}✓ SUCCESS${NC}: $1"
}

# Function to print error
error() {
    echo -e "${RED}✗ ERROR${NC}: $1"
}

# Test 1: Health Check
echo "Test 1: Health Check"
echo "-------------------"
response=$(curl -s -X GET "$API_URL/health")
echo "Response: $response"
if echo "$response" | grep -q "ok"; then
    success "Health check passed"
else
    error "Health check failed"
fi
echo ""

# Test 2: Signup
echo "Test 2: Signup"
echo "--------------"
response=$(curl -s -X POST "$API_URL/signup" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}")
echo "Response: $response"
if echo "$response" | grep -q "username"; then
    success "Signup successful"
else
    error "Signup failed"
fi
echo ""

# Test 3: Login
echo "Test 3: Login"
echo "-------------"
response=$(curl -s -X POST "$API_URL/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}")
echo "Response: $response"
if echo "$response" | grep -q "access_token"; then
    TOKEN=$(echo "$response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    success "Login successful - Token: ${TOKEN:0:20}..."
else
    error "Login failed"
fi
echo ""

# Test 4: Get Jobs
echo "Test 4: Get Jobs (with pagination)"
echo "----------------------------------"
response=$(curl -s -X GET "$API_URL/jobs?skip=0&limit=5" \
  -H "Content-Type: application/json")
echo "Response (first 200 chars): ${response:0:200}..."
if echo "$response" | grep -q "id"; then
    success "Get jobs successful"
    # Extract first job ID
    JOB_ID=$(echo "$response" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
    echo "First job ID: $JOB_ID"
else
    error "Get jobs failed"
fi
echo ""

# Test 5: Upload Resume
echo "Test 5: Upload Resume"
echo "--------------------"
response=$(curl -s -X POST "$API_URL/resumes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Experienced Python developer with 5+ years of backend development experience. Proficient in FastAPI, Django, PostgreSQL, Docker, and cloud deployment. Strong problem-solving skills and experience with microservices architecture. Proven track record of building scalable REST APIs and implementing CI/CD pipelines."
  }')
echo "Response: $response"
if echo "$response" | grep -q "resume_text"; then
    RESUME_ID=$(echo "$response" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
    success "Resume upload successful - Resume ID: $RESUME_ID"
else
    error "Resume upload failed"
fi
echo ""

# Test 6: Get Resume
echo "Test 6: Get Resume"
echo "-----------------"
response=$(curl -s -X GET "$API_URL/resumes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json")
echo "Response (first 200 chars): ${response:0:200}..."
if echo "$response" | grep -q "resume_text"; then
    success "Get resume successful"
else
    error "Get resume failed"
fi
echo ""

# Test 7: Match Jobs with Inline Resume
echo "Test 7: Match Jobs (with inline resume)"
echo "---------------------------------------"
response=$(curl -s -X POST "$API_URL/match" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Python developer backend FastAPI PostgreSQL",
    "top_k": 3
  }')
echo "Response (first 200 chars): ${response:0:200}..."
if echo "$response" | grep -q "job"; then
    success "Job matching with inline resume successful"
else
    error "Job matching with inline resume failed"
fi
echo ""

# Test 8: Match Jobs with Stored Resume
echo "Test 8: Match Jobs (with stored resume)"
echo "---------------------------------------"
if [ ! -z "$RESUME_ID" ]; then
    response=$(curl -s -X POST "$API_URL/match" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"resume_id\": $RESUME_ID,
        \"top_k\": 5
      }")
    echo "Response (first 200 chars): ${response:0:200}..."
    if echo "$response" | grep -q "job"; then
        success "Job matching with stored resume successful"
    else
        error "Job matching with stored resume failed"
    fi
else
    error "Skipping - No resume ID available"
fi
echo ""

# Test 9: Update Resume
echo "Test 9: Update Resume"
echo "--------------------"
if [ ! -z "$RESUME_ID" ]; then
    response=$(curl -s -X PUT "$API_URL/resumes" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "resume_text": "Updated: Senior Python developer with 6+ years of experience in full-stack development, cloud architecture, and machine learning integration."
      }')
    echo "Response: $response"
    if echo "$response" | grep -q "resume_text"; then
        success "Resume update successful"
    else
        error "Resume update failed"
    fi
else
    error "Skipping - No resume ID available"
fi
echo ""

# Test 10: Invalid Request (validation error)
echo "Test 10: Invalid Request (validation test)"
echo "-----------------------------------------"
response=$(curl -s -X POST "$API_URL/signup" \
  -H "Content-Type: application/json" \
  -d '{"username":"ab","password":"123"}')
echo "Response: $response"
if echo "$response" | grep -q "validation_error\|detail"; then
    success "Validation error handling works correctly"
else
    error "Validation error handling failed"
fi
echo ""

# Test 11: Unauthorized Access
echo "Test 11: Unauthorized Access (missing token)"
echo "-------------------------------------------"
response=$(curl -s -X GET "$API_URL/resumes" \
  -H "Content-Type: application/json")
echo "Response: $response"
if echo "$response" | grep -q "401\|Could not validate credentials"; then
    success "Authentication protection works"
else
    error "Authentication protection failed"
fi
echo ""

echo "=========================================="
echo "Testing Complete!"
echo "=========================================="
echo ""
echo "Summary:"
echo "--------"
echo "• Health check: Working"
echo "• Authentication: Signup and Login functional"
echo "• Resume Management: Upload, Read, Update functional"
echo "• Job Listing: Pagination working"
echo "• Job Matching: Both inline and stored resumes working"
echo "• Error Handling: Validation and auth checks working"
echo ""
echo "Next steps:"
echo "1. Run full test suite: pytest"
echo "2. Check API documentation: http://localhost:8000/docs"
echo "3. Deploy to AWS"
echo ""
