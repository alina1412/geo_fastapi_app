from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import Settings


if Settings().DEBUG:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}  # only for sqlite
    )
else:
    SQLALCHEMY_DATABASE_URL = Settings().DATABASE_URL
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        # connect_args={"check_same_thread": False}  # only for sqlite
    )

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False, 
    autoflush=False, 
    )

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
