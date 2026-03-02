# Intelligent Job Recommendation Service

Production-ready ML-powered job recommendation system with resume matching, user authentication, and comprehensive API.

## Overview

This service combines:
- **FastAPI** backend for REST API
- **PostgreSQL** for persistent data storage
- **Sentence Transformers** for semantic resume/job matching
- **JWT Authentication** for secure user management
- **Docker** for containerized deployment

## Features

✅ User authentication with JWT tokens
✅ Resume upload, update, and deletion
✅ Job listing with pagination
✅ ML-powered job matching using embeddings
✅ Match history tracking
✅ Comprehensive error handling and logging
✅ CORS configuration for frontend integration
✅ Input validation with Pydantic
✅ Full test suite
✅ Production-ready deployment

## Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Docker & Docker Compose (optional)

### Option 1: Docker Compose (Recommended)

```bash
# Clone and navigate to project
cd job-recommendation-service

# Create .env file
cp .env.example .env

# Start services
docker-compose up --build -d

# Check logs
docker-compose logs -f web
```

Access API at `http://localhost:8000`

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Update .env with your settings
# DATABASE_URL=postgres://user:password@localhost:5432/jobs_db
# SECRET_KEY=your-secret-key

# Start PostgreSQL
# (ensure PostgreSQL is running locally)

# Run application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access API at `http://localhost:8000`

API Documentation available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
- `GET /health` - Service health status

### Authentication

**POST /signup** - Register new user
```json
{
  "username": "john_doe",
  "password": "secure_password_123"
}
```

**POST /login** - Get JWT access token
```json
{
  "username": "john_doe",
  "password": "secure_password_123"
}
```

### Resumes (Authenticated)

**POST /resumes** - Upload/create resume
```json
{
  "resume_text": "Senior Python Developer with 5+ years experience....."
}
```

**GET /resumes** - Retrieve your resume

**PUT /resumes** - Update your resume
```json
{
  "resume_text": "Updated resume content....."
}
```

**DELETE /resumes** - Delete your resume

### Jobs

**GET /jobs** - List jobs with pagination
- Query parameters:
  - `skip` (int, default=0): Records to skip
  - `limit` (int, default=10, max=100): Records per page

Example: `/jobs?skip=0&limit=10`

### Job Matching (Authenticated)

**POST /match** - Match jobs to resume
```json
{
  "top_k": 5,
  "resume_text": "Optional: inline resume text",
  "resume_id": null
}
```

Or use stored resume:
```json
{
  "resume_id": 1,
  "top_k": 5
}
```

Response:
```json
[
  {
    "job": {
      "id": 1,
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "description": "..."
    },
    "score": 0.87
  }
]
```

## Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test Suite
```bash
pytest tests/test_auth.py -v
pytest tests/test_resumes.py -v
pytest tests/test_jobs.py -v
pytest tests/test_match.py -v
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Test Endpoints Manually

```bash
# Signup
curl -X POST "http://localhost:8000/signup" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# Login
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# Get Jobs (no auth needed)
curl "http://localhost:8000/jobs?skip=0&limit=5"

# Upload Resume (replace TOKEN with actual token)
curl -X POST "http://localhost:8000/resumes" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"resume_text":"Python developer with 5 years experience..."}'

# Match Jobs
curl -X POST "http://localhost:8000/match" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"resume_text":"Python developer...","top_k":5}'
```

## Environment Configuration

Copy `.env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=postgres://user:password@localhost:5432/jobs_db

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Logging
LOG_LEVEL=INFO

# CORS (for frontend)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Architecture

### Database Schema

- **users** - User accounts with hashed passwords
- **resumes** - User resumes with timestamps
- **jobs** - Available job listings
- **matches** - Match history with similarity scores

### ML Pipeline

1. **Resume Upload** - User uploads resume text
2. **Embedding Generation** - Using Sentence Transformers (all-MiniLM-L6-v2)
3. **Job Matching** - Cosine similarity between resume and job embeddings
4. **Ranking** - Top-K results sorted by similarity score
5. **History** - Matches saved to database

### Fallback Mechanism

If Sentence Transformers fails to load, the service uses deterministic hashing for embeddings.

## Deployment

### AWS Deployment

For AWS deployment, update docker-compose.yml:
```yaml
environment:
  DATABASE_URL: postgresql://user:password@your-rds-endpoint:5432/jobs_db
  SECRET_KEY: ${SECRET_KEY}  # Set in AWS Secrets Manager
```

### Production Checklist

- [ ] Update `SECRET_KEY` to a strong random value
- [ ] Configure `ALLOWED_ORIGINS` for your frontend domain
- [ ] Use environment variables for all secrets
- [ ] Enable SSL/TLS in reverse proxy
- [ ] Set up database backups
- [ ] Configure monitoring and logging
- [ ] Enable rate limiting
- [ ] Set up CI/CD pipeline
- [ ] Run security audit: `bandit -r app/`
- [ ] Test all endpoints in staging

## Error Handling

The API follows standard HTTP status codes:

- `200 OK` - Successful request
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid auth
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

## Logging

All requests and events are logged with:
- Timestamp
- Log level (DEBUG, INFO, WARNING, ERROR)
- Component name
- Message

View logs:
```bash
# Docker
docker-compose logs -f web

# Local
# Check stderr output or configure logging to file
```

## Troubleshooting

### Database Connection Error
```
psycopg2.OperationalError: could not connect to server
```
Solution: Ensure PostgreSQL is running and DATABASE_URL is correct.

### Port Already in Use
```
OSError: [Errno 48] Address already in use: ('0.0.0.0', 8000)
```
Solution: Change port or kill existing process.

### Sentence Transformers Download Failed
The service falls back to hashing. Run offline or check internet connection.

## Development

### Code Structure
```
app/
├── main.py           # FastAPI app setup
├── models.py         # SQLAlchemy models
├── schemas.py        # Pydantic validation
├── auth.py           # JWT authentication
├── db.py             # Database configuration
├── core/
│   └── config.py     # Settings
├── routes/
│   ├── auth.py       # User endpoints
│   ├── resumes.py    # Resume endpoints
│   ├── jobs.py       # Job endpoints
│   └── match.py      # Matching endpoints
└── services/
    └── embeddings.py # ML embedding service

tests/
├── conftest.py       # Pytest configuration
├── test_auth.py      # Auth tests
├── test_resumes.py   # Resume tests
├── test_jobs.py      # Job tests
└── test_match.py     # Matching tests
```

### Adding New Features

1. Add database model in `models.py`
2. Add Pydantic schema in `schemas.py`
3. Create route in `routes/`
4. Add tests in `tests/`
5. Update this README

## Performance

### Optimization Tips

- Jobs are loaded into memory (app.state.jobs) at startup
- Database connection pooling enabled
- Pagination limits prevent large data transfers
- Input validation reduces processing

### Load Testing

```bash
# Install locust
pip install locust

# Run load test
locust -f locustfile.py
```

## Security

- Passwords hashed with bcrypt
- JWT tokens with expiration
- SQL injection protection via SQLAlchemy ORM
- Input validation with Pydantic
- CORS configuration for frontend

## Dependencies

See `requirements.txt` for complete list. Key:
- **fastapi** - Web framework
- **sqlalchemy** - ORM
- **psycopg2** - PostgreSQL adapter
- **sentence-transformers** - ML embeddings
- **pydantic** - Data validation
- **passlib** - Password hashing
- **python-jose** - JWT handling
- **pytest** - Testing framework

## License

MIT License

## Support & Contributing

For issues or feature requests, please open an issue.

## Next Steps

1. ✅ Test all endpoints locally
2. ✅ Configure production environment
3. ✅ Set up AWS deployment
4. ✅ Configure frontend (React/Vue)
5. ✅ Enable Redis caching (optional)
6. ✅ Set up monitoring with CloudWatch
