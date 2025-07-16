import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Driver, Team
from main import app, get_db

@pytest.fixture(scope='session')
def db_engine():
    engine = create_engine('sqlite:///:memory:', connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
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