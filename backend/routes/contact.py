from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import SessionLocal

router = APIRouter(
    prefix="/contact",
    tags=["Contact Messages"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ContactResponse)
def submit_contact(message: schemas.ContactCreate, db: Session = Depends(get_db)):
    new_message = models.ContactMessage(**message.model_dump())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

@router.get("/", response_model=List[schemas.ContactResponse])
def get_messages(db: Session = Depends(get_db)):
    return db.query(models.ContactMessage).all()