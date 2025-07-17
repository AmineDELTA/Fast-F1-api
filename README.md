# 🏎️ Fast-F1-api - Learning Project

A **FastAPI-based REST API** for managing Formula 1 drivers, teams, and rankings. Built as a learning project to explore modern Python backend development.

> **Note:** Some architectural choices prioritize learning over best practices.

## 🛠️ Tech Stack

|           |            |
|-----------|------------|
| **Web Framework** | FastAPI 0.115.12 |
| **Database** | PostgreSQL + SQLAlchemy 2.0.40 |
| **Validation** | Pydantic 2.11.3 |
| **Testing** | pytest 8.3.5 + httpx |
| **Server** | Uvicorn (ASGI) |
| **Environment** | python-dotenv |


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

## 📦 Installation & Setup

### **1. Clone the Repository**
```bash
git clone https://github.com/AmineDELTA/F1_API.git
cd F1_API
```

### **2. Create Virtual Environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Database Setup**
```bash
# Create PostgreSQL database
createdb f1_api_db

# Set up environment variables
echo "DATABASE_URL=postgresql://username:password@localhost:5432/f1_api_db" > .env
```

### **5. Initialize Database**
```bash
python -c "from database import engine; from models import Base; Base.metadata.create_all(engine)"
```

### **6. Run the Application**
```bash
uvicorn main:app --reload
```

Visit: `http://localhost:8000/docs` for interactive API documentation



**Amine DELTA** - [GitHub Profile](https://github.com/AmineDELTA) - [LinkedIn Profile](www.linkedin.com/in/mohamed-amine-el-gueddar-312a2b26a)

Project Link: [https://github.com/AmineDELTA/F1_API](https://github.com/AmineDELTA/F1_API)
