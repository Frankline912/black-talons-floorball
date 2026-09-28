from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

import models, schemas
from database import SessionLocal

router = APIRouter(
    prefix="/training",
    tags=["Training Schedule"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.TrainingResponse])
def get_training(db: Session = Depends(get_db)):
    schedules = db.query(models.Training).all()
    result = []
    for s in schedules:
        start_str = s.start_time.strftime("%H:%M") if hasattr(s.start_time, "strftime") else str(s.start_time)[:5]
        end_str = s.end_time.strftime("%H:%M") if hasattr(s.end_time, "strftime") else str(s.end_time)[:5]

        result.append({
            "id": s.id,
            "day": s.day,
            "title": s.day,
            "start_time": start_str,
            "end_time": end_str,
            "venue": s.venue,
            "location": s.venue,
            "description": s.description
        })
    return result

@router.post("/", response_model=schemas.TrainingResponse)
def create_training(training: schemas.TrainingCreate, db: Session = Depends(get_db)):
    try:
        s_time = datetime.strptime(training.start_time.strip(), "%H:%M").time()
        e_time = datetime.strptime(training.end_time.strip(), "%H:%M").time()
        
        new_schedule = models.Training(
            day=training.day,
            start_time=s_time,
            end_time=e_time,
            venue=training.venue,
            description=training.description
        )
        db.add(new_schedule)
        db.commit()
        db.refresh(new_schedule)
        
        return {
            "id": new_schedule.id,
            "day": new_schedule.day,
            "title": new_schedule.day,
            "start_time": s_time.strftime("%H:%M"),
            "end_time": e_time.strftime("%H:%M"),
            "venue": new_schedule.venue,
            "location": new_schedule.venue,
            "description": new_schedule.description
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid time format or data: {str(e)}")

@router.post("/bulk", response_model=List[schemas.TrainingResponse])
def create_bulk_training(trainings: List[schemas.TrainingCreate], db: Session = Depends(get_db)):
    created_schedules = []
    try:
        for training in trainings:
            s_time = datetime.strptime(training.start_time.strip(), "%H:%M").time()
            e_time = datetime.strptime(training.end_time.strip(), "%H:%M").time()
            
            new_schedule = models.Training(
                day=training.day,
                start_time=s_time,
                end_time=e_time,
                venue=training.venue,
                description=training.description
            )
            db.add(new_schedule)
            db.commit()
            db.refresh(new_schedule)
            
            created_schedules.append({
                "id": new_schedule.id,
                "day": new_schedule.day,
                "title": new_schedule.day,
                "start_time": s_time.strftime("%H:%M"),
                "end_time": e_time.strftime("%H:%M"),
                "venue": new_schedule.venue,
                "location": new_schedule.venue,
                "description": new_schedule.description
            })
        return created_schedules
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid time format or data: {str(e)}")

@router.delete("/")
def delete_all_training(db: Session = Depends(get_db)):
    try:
        db.query(models.Training).delete()
        db.commit()
        return {"message": "All training schedules have been cleared successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{training_id}")
def delete_single_training(training_id: int, db: Session = Depends(get_db)):
    training = db.query(models.Training).filter(models.Training.id == training_id).first()
    if not training:
        raise HTTPException(status_code=404, detail="Training schedule not found")
    
    db.delete(training)
    db.commit()
    return {"message": f"Training schedule with ID {training_id} deleted successfully"}