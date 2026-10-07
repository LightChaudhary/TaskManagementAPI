import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./tasks.db",
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-secret-key-change-in-production",
)