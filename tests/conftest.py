import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from app.DB.database import Base
from app.DB import models

from fastapi.testclient import TestClient

from app.main import app
from app.DB.database import get_db

# Load environment variables
load_dotenv()

# Build a dedicated test database URL
TEST_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "5432")),
    database="task_manager_test_db",
)

# Create a dedicated test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    Base.metadata.create_all(bind=test_engine)
    yield

@pytest.fixture
def db_connection(create_test_tables):
    connection = test_engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()

@pytest.fixture
def db_session(db_connection):
    TestingSessionLocal = sessionmaker(
        bind=db_connection,
        autoflush=False,
        autocommit=False,
        join_transaction_mode="create_savepoint",
    )

    session = TestingSessionLocal()

    yield session

    session.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


