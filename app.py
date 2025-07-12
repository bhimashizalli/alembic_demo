from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "postgresql://username:password@localhost/todo_db"

# Database connection setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")