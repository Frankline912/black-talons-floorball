from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import SessionLocal

router = APIRouter(
    prefix="/matches",
    tags=["Matches"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET: Fetch all matches
@router.get("/", response_model=List[schemas.MatchResponse])
def get_matches(db: Session = Depends(get_db)):
    return db.query(models.Match).all()

# POST: Add a single match
@router.post("/", response_model=schemas.MatchResponse)
def add_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    new_match = models.Match(**match.model_dump())
    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    return new_match

# POST: Add multiple matches in bulk
@router.post("/bulk", response_model=List[schemas.MatchResponse])
def create_bulk_matches(matches: List[schemas.MatchCreate], db: Session = Depends(get_db)):
    created_matches = []
    try:
        for match_data in matches:
            new_match = models.Match(**match_data.model_dump())
            db.add(new_match)
            db.commit()
            db.refresh(new_match)
            created_matches.append(new_match)
        return created_matches
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating bulk matches: {str(e)}")

# PUT: Update an existing match (e.g., add scores or change status)
@router.put("/{match_id}", response_model=schemas.MatchResponse)
def update_match(match_id: int, updated_match: schemas.MatchCreate, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    match.opponent = updated_match.opponent
    match.match_date = updated_match.match_date
    match.match_time = updated_match.match_time
    match.venue = updated_match.venue
    match.competition = updated_match.competition
    match.home_score = updated_match.home_score
    match.away_score = updated_match.away_score
    match.status = updated_match.status
    
    db.commit()
    db.refresh(match)
    return match

# DELETE: Clear all matches
@router.delete("/")
def delete_all_matches(db: Session = Depends(get_db)):
    try:
        db.query(models.Match).delete()
        db.commit()
        return {"message": "All matches have been cleared successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# DELETE: Remove a single match by ID
@router.delete("/{match_id}")
def delete_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    db.delete(match)
    db.commit()
    return {"message": f"Match with ID {match_id} deleted successfully"}