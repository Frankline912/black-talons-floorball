from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update the filename here if your SQLite database file was named something specific (e.g., floorball.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./floorball.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency function used across your routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()