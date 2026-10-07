import pytest

from app.models.user import User
from app.database import Base,get_db
from app.models.task import Task
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.dependencies import get_current_user


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

def override_get_current_user():
    db = TestingSessionLocal()

    try:
        return db.query(User).filter(User.username == "testuser").first()
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def override_database_dependency():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    yield

    app.dependency_overrides.clear()

    
@pytest.fixture(autouse=True)
def reset_tasks():
    db = TestingSessionLocal()

    try:
        db.query(Task).delete()
        db.query(User).delete()

        test_user = User(
            username="testuser",
            password_hash="test-hash",
        )

        db.add(test_user)
        db.commit()
        db.refresh(test_user)

        task1 = Task(
            title="learn rest",
            description="understand http methods and status codes.",
            status="todo",
            priority="high",
            owner_id=test_user.id,
        )

        task2 = Task(
            title="learn git branches",
            description="practice feature branches and merging",
            status="todo",
            priority="medium",
            owner_id=test_user.id,
        )

        db.add_all([task1, task2])
        db.commit()

    finally:
        db.close()
