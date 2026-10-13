from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.database import engine, get_db, WaterIntakeRecord, Base
from src.agent import get_hydration_feedback
from src.logger import setup_logger

logger = setup_logger("api")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Euron Water Tracker API")

class IntakeCreate(BaseModel):
    user_id: str
    amount_ml: float

@app.post("/log-water/")
def log_water(intake: IntakeCreate, db: Session = Depends(get_db)):
    logger.info(f"API Request: Log water for user '{intake.user_id}' with amount {intake.amount_ml}ml")
    db_record = WaterIntakeRecord(user_id=intake.user_id, amount_ml=intake.amount_ml)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    logger.info(f"Successfully committed record ID {db_record.id}")
    return {"message": "Water intake logged successfully", "record_id": db_record.id}

@app.get("/feedback/{user_id}")
def get_feedback(user_id: str, db: Session = Depends(get_db)):
    logger.info(f"API Request: Get feedback for user '{user_id}'")
    records = db.query(WaterIntakeRecord)\
                .filter(WaterIntakeRecord.user_id == user_id)\
                .all()
    
    total_intake = sum([r.amount_ml for r in records])
    ai_feedback = get_hydration_feedback(total_intake)
    
    return {
        "user_id": user_id,
        "total_intake_ml": total_intake,
        "feedback": ai_feedback
    }