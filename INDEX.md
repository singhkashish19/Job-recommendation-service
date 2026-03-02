# Intelligent Job Recommendation Service

A production-ready ML-powered job recommendation system with resume matching, user authentication, and comprehensive backend API.

## 📚 Documentation

All documentation has been organized in the `docs/` folder for better readability:

- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - Get started in 5 minutes ⚡
- **[docs/README.md](docs/README.md)** - Complete project documentation 📖
- **[docs/AWS_DEPLOYMENT.md](docs/AWS_DEPLOYMENT.md)** - AWS deployment guide 🚀
- **[docs/TESTING_CHECKLIST.md](docs/TESTING_CHECKLIST.md)** - Verify your setup ✅
- **[docs/IMPLEMENTATION_SUMMARY.md](docs/IMPLEMENTATION_SUMMARY.md)** - What was implemented 📋

## 🚀 Quick Start

### Using Docker (Easiest)
```bash
docker-compose up --build -d
```
Access API: http://localhost:8000/docs

### Local Development

See [docs/QUICKSTART.md](docs/QUICKSTART.md) for detailed setup instructions.

## 📁 Project Structure

```
job-recommendation-service/
├── app/                    # Application code
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── db.py
│   ├── core/
│   ├── routes/
│   └── services/
├── tests/                  # Test suite (28 tests)
├── docs/                   # Documentation
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── AWS_DEPLOYMENT.md
│   ├── TESTING_CHECKLIST.md
│   └── IMPLEMENTATION_SUMMARY.md
├── data/                   # Data files
│   ├── jobs_mock.json
│   └── test_api.sh
├── app.py                  # Start from docs/QUICKSTART.md
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker configuration
├── Dockerfile
├── .env                    # Configuration (customize)
├── .env.example            # Configuration template
└── .gitignore
```

## 🎯 Key Features

✅ **User Authentication** - JWT tokens
✅ **Resume Management** - Upload, update, delete
✅ **Job Matching** - ML-powered with embeddings
✅ **API Documentation** - Interactive Swagger UI at /docs
✅ **Full Test Suite** - 28 comprehensive tests
✅ **Docker Ready** - One-command deployment
✅ **AWS Ready** - Complete deployment guide

## 💻 Setup Overview

### Prerequisites
- Python 3.9+ (for local development)
- PostgreSQL 13+ (or use Docker)
- Docker & Docker Compose (optional)

### 1. Local Development Setup

**Step 1: Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Setup Environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

**Step 4: Run Application**
```bash
uvicorn app.main:app --reload --port 8000
```

Access: http://localhost:8000/docs

### 2. Docker Setup

```bash
docker-compose up --build -d
```

For detailed setup instructions, see **[docs/QUICKSTART.md](docs/QUICKSTART.md)**

## 📖 Documentation Reference

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](docs/QUICKSTART.md) | 5-minute setup guide |
| [README.md](docs/README.md) | Full documentation |
| [AWS_DEPLOYMENT.md](docs/AWS_DEPLOYMENT.md) | AWS deployment steps |
| [TESTING_CHECKLIST.md](docs/TESTING_CHECKLIST.md) | Verification steps |
| [IMPLEMENTATION_SUMMARY.md](docs/IMPLEMENTATION_SUMMARY.md) | What was built |

## 🧪 Testing

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py -v
```

## 🔐 Security

- Passwords hashed with bcrypt
- JWT tokens with expiration
- SQL injection protection (SQLAlchemy ORM)
- Input validation with Pydantic
- CORS configuration
- Error message sanitization

## 📊 Project Status

✅ **All Features Implemented**
✅ **All Tests Passing** (28 tests)
✅ **Documentation Complete**
✅ **Docker Ready**
✅ **AWS Deployment Guide Included**
✅ **Production Ready**

## 🛠️ Configuration

Edit `.env` file to customize:

```env
DATABASE_URL=postgres://user:password@localhost:5432/jobs_db
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
LOG_LEVEL=INFO
```

## 🤝 API Endpoints

All endpoints listed in interactive documentation: **http://localhost:8000/docs**

**Key Endpoints:**
- `POST /signup` - Create account
- `POST /login` - Get JWT token
- `POST /resumes` - Upload resume
- `POST /match` - Get job recommendations
- `GET /jobs` - List jobs

## 📞 Support

**Having issues?**
1. Check [docs/QUICKSTART.md](docs/QUICKSTART.md) troubleshooting section
2. Review [docs/README.md](docs/README.md) for detailed information
3. Check logs: `docker-compose logs -f web`

## 🚀 Next Steps

1. ✅ Read [docs/QUICKSTART.md](docs/QUICKSTART.md)
2. ✅ Run locally or with Docker
3. ✅ Test all endpoints at http://localhost:8000/docs
4. ✅ Deploy to AWS following [docs/AWS_DEPLOYMENT.md](docs/AWS_DEPLOYMENT.md)
5. ✅ Build frontend using the API

---

**Status: ✅ Production Ready** - Fully implemented and tested

For complete details, see [docs/README.md](docs/README.md)
