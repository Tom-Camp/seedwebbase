import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import TestingConfig
from seedweb.main import app, get_db
from seedweb.models import Base

engine = create_engine(TestingConfig.SQLALCHEMY_DATABASE_URI)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(autouse=True)
def cleanup_tables():
    with engine.connect() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())


@pytest.fixture(scope="session")
def valid_project():
    project = {
        "name": "Test Project One",
        "bed_id": "lettuce",
        "description": "A test of the lettuce bed",
        "profile_id": 1,
        "start": "07:00:00",
        "end": "17:00:00",
    }
    return project
