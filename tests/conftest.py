import pytest

from app.database import Base,get_db
from app.models.task import Task
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


TEST_DATABASE_URL = "sqlite:///./test_tasks.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def override_database_dependency():
    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.clear()

    
@pytest.fixture(autouse=True)
def reset_tasks():
    db = TestingSessionLocal()
    try:
        db.query(Task).delete()

        task1 = Task(
            title="learn rest",
            description="understand http methods and status codes.",
            status="todo",
            priority="high",
        )

        task2 = Task(
            title="learn git branches",
            description="practice feature branches and merging",
            status="todo",
            priority="medium",
        )

        db.add_all([task1, task2])
        db.commit()
    finally:
        db.close()
