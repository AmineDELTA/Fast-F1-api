import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Driver, Team

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # update later on
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_team(db_session):
    team = Team(name="Mercedes", victories=125, championships=8)
    db_session.add(team)
    db_session.commit()
    return team

@pytest.fixture
def test_driver(db_session, test_team):
    driver = Driver(
        first_name="Lewis",
        last_name="Hamilton",
        number=44,
        age=38,
        nationality="British",
        team_name_id=test_team.id
    )
    db_session.add(driver)
    db_session.commit()
    return driver