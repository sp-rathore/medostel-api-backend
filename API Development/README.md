# Medostel API Backend

Healthcare AI Assistant - FastAPI Backend Service

## Overview

This is the backend API service for the Medostel Healthcare AI Assistant platform. It provides RESTful endpoints for:
- User authentication and management
- Medical report processing
- Geographic data management
- Role-based access control

## Technology Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 18
- **Authentication**: JWT / OAuth2
- **Deployment**: Google Cloud Run / Kubernetes (GKE)
- **API Documentation**: Swagger/OpenAPI 3.0

## Project Structure

```
medostel-api-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection setup
│   ├── security.py          # Authentication & security utilities
│   ├── models/              # Pydantic models (request/response)
│   │   ├── __init__.py
│   │   ├── user.py          # User models
│   │   ├── auth.py          # Authentication models
│   │   ├── report.py        # Report models
│   │   └── location.py      # Location models
│   ├── schemas/             # Database schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── report.py
│   │   └── location.py
│   ├── routes/              # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── users.py         # User management endpoints
│   │   ├── reports.py       # Report endpoints
│   │   └── locations.py     # Location endpoints
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── auth_service.py
│   │   └── report_service.py
│   └── dependencies/        # Dependency injection
│       ├── __init__.py
│       └── auth.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_users.py
│   └── test_reports.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── pytest.ini
└── README.md
```

## Prerequisites

- Python 3.11+
- PostgreSQL 18
- Docker (for containerized deployment)
- Git

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/medostel-api-backend.git
cd medostel-api-backend
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Run database migrations
```bash
alembic upgrade head
```

### 6. Start the application
```bash
uvicorn app.main:app --reload
```

Application will be available at: `http://localhost:8000`

## API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/medostel

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Cloud
GCP_PROJECT_ID=gen-lang-client-0064186167
GCP_REGION=asia-south1

# SendGrid Email
SENDGRID_API_KEY=your-api-key
```

## Database

### Connection Details
- **Host**: 35.200.195.16
- **Port**: 5432
- **Database**: medostel
- **Admin User**: medostel_admin_user
- **API User**: medostel_api_user

### Running Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - User logout

### Users
- `GET /api/v1/users/{userId}` - Get user profile
- `PUT /api/v1/users/{userId}` - Update user profile
- `DELETE /api/v1/users/{userId}` - Delete user

### Reports
- `POST /api/v1/reports/upload` - Upload medical report
- `GET /api/v1/reports/{userId}` - Get user's reports
- `GET /api/v1/reports/{reportId}` - Get report details
- `DELETE /api/v1/reports/{reportId}` - Delete report

### Locations (Updated March 2, 2026 - Numeric Types & pinCode as PK)
- `GET /api/v1/locations/all` - Get all locations (with filtering by country, state_id, status)
- `GET /api/v1/locations/pincodes` - Get pinCodes for a city (by city_id or city_name) - **NEW**
- `POST /api/v1/locations` - Create new location (pinCode, stateId, cityId now numeric)
- `PUT /api/v1/locations/{pin_code}` - Update location by pinCode (was {id})
- **REMOVED**: `DELETE /api/v1/locations/{id}` - Use status field instead

## Testing

### Run tests
```bash
pytest

# With coverage
pytest --cov=app

# Specific test file
pytest tests/test_auth.py -v
```

### Test configuration
See `pytest.ini` for test configuration.

## Docker

### Build image
```bash
docker build -t medostel-api:latest .
```

### Run container
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/medostel \
  medostel-api:latest
```

### Docker Compose
```bash
docker-compose up -d
```

## Deployment

### Google Cloud Run
```bash
gcloud run deploy medostel-api \
  --source . \
  --platform managed \
  --region asia-south1 \
  --project gen-lang-client-0064186167
```

### Kubernetes (GKE)
```bash
# Build and push image
docker build -t gcr.io/gen-lang-client-0064186167/medostel-api:latest .
docker push gcr.io/gen-lang-client-0064186167/medostel-api:latest

# Deploy to GKE
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Security

- ✅ JWT token-based authentication
- ✅ Password hashing with bcrypt
- ✅ CORS configuration
- ✅ Rate limiting
- ✅ Input validation
- ✅ SQL injection prevention
- ✅ XSS protection

## Monitoring

- Application logs: Google Cloud Logging
- Metrics: Google Cloud Monitoring
- Error tracking: Sentry (optional)
- Performance monitoring: Custom instrumentation

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add new feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit a pull request

## Code Style

- PEP 8 compliance
- Type hints for all functions
- Docstrings for modules, classes, and functions
- Black for code formatting
- Flake8 for linting

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## Troubleshooting

### Database connection error
```bash
# Check database URL
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port already in use
```bash
# Find and kill process using port 8000
lsof -i :8000
kill -9 <PID>
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/medostel-api-backend/issues
- Email: support@medostel.com
- Documentation: https://medostel-docs.com

## License

MIT License - See LICENSE file for details

## Authors

- Claude Code
- Your Team

---

**Last Updated**: 2026-03-02
**Status**: Development (Phase 3 - Documentation Updates in Progress)
**Version**: 0.2.0
