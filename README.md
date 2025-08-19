# 🏎️ Fast-F1-api - Learning Project

A **FastAPI-based REST API** for managing Formula 1 drivers, teams, and rankings. Built as a learning project to explore modern Python backend development.

> **Note:** Some architectural choices prioritize learning over best practices.

## 🛠️ Tech Stack

|                      |                                |
| -------------------- | ------------------------------ |
| **Web Framework**    | FastAPI 0.115.12               |
| **Database**         | PostgreSQL + SQLAlchemy 2.0.40 |
| **Validation**       | Pydantic 2.11.3                |
| **Testing**          | pytest 8.3.5 + httpx           |
| **Server**           | Uvicorn (ASGI)                 |
| **Environment**      | python-dotenv                  |
| **Containerization** | Docker + Docker Compose        |

## 🏗️ Project Structure

```
F1_API/
├── main.py              # FastAPI application entry point
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic data validation schemas
├── crud.py              # Database operations
├── database.py          # Database connection and session management
├── rate_limit.py        # Rate limiting middleware
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build instructions
├── docker-compose.yml   # Multi-container orchestration
├── .dockerignore        # Docker build context exclusions
├── .env.example         # Environment variables template
├── .env                 # Environment variables (not in repo)
└── test/
    ├── conftest.py      # pytest fixtures and test configuration
    ├── test_drivers.py  # Driver endpoint tests
    ├── test_teams.py    # Team endpoint tests
    └── test_rankings.py # Rankings endpoint tests
```

## 🚀 Features

### **Driver Management**

- ✅ Create new drivers with validation
- ✅ Get driver by number
- ✅ List all drivers
- ✅ Associate drivers with teams

### **Team Management**

- ✅ Create teams with statistics
- ✅ Get team information
- ✅ List team drivers
- ✅ Track victories and championships

### **Rankings System**

- ✅ Driver championship rankings
- ✅ Team championship standings
- ✅ Points-based ranking system

### **Additional Features**

- ✅ Rate limiting middleware
- ✅ Comprehensive test suite
- ✅ Data validation with Pydantic
- ✅ PostgreSQL database integration
- ✅ Environment-based configuration
- ✅ Docker containerization
- ✅ Hot reload development

## 🐳 Quick Start with Docker

### **Prerequisites**

- Docker and Docker Compose installed

### **1. Clone and Setup**

```bash
git clone https://github.com/AmineDELTA/F1_API.git
cd F1_API
```

### **2. Configure Environment**

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
# DATABASE_URL=postgresql://postgres:your_password@db:5432/F1_data
# POSTGRES_USER=postgres
# POSTGRES_PASSWORD=your_password
# POSTGRES_DB=F1_data
```

### **3. Run with Docker**

```bash
# Start the full application stack
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### **4. Access the Application**

- **API Documentation:** http://localhost:8000/docs
- **API Root:** http://localhost:8000
- **Database:** localhost:5432

### **5. Create Test Data**

Use the Swagger UI at http://localhost:8000/docs to:

1. Create teams using `POST /teams/create`
2. Create drivers using `POST /drivers/create`
3. Test endpoints like `GET /drivers/{number}`

## 🎓 Learning Notes

### **What I Learned:**

1. **FastAPI Fundamentals**

   - Route definitions and path parameters
   - Request/response models with Pydantic
   - Dependency injection system
   - Automatic API documentation

2. **Database Integration**

   - SQLAlchemy ORM relationships
   - Database session management
   - Migration patterns
   - Query optimization

3. **Testing Best Practices**

   - Test isolation with database transactions
   - Fixture design and dependency injection
   - HTTP client testing with TestClient
   - Mocking external dependencies

4. **API Design**
   - RESTful endpoint patterns
   - Error handling and status codes
   - Data validation and serialization
   - Rate limiting and middleware

## 👤 Author

**AmineDELTA** - [GitHub Profile](https://github.com/AmineDELTA)
