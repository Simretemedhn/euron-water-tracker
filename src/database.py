import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
from src.logger import setup_logger

load_dotenv()
logger = setup_logger("database")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./water_tracker.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class WaterIntakeRecord(Base):
    __tablename__ = "water_intake"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    amount_ml = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    logger.info("Database session opened.")
    try:
        yield db
    finally:
        db.close()
        logger.info("Database session closed.")