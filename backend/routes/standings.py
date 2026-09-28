from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models, schemas
from routes.auth import get_current_admin

router = APIRouter(prefix="/standings", tags=["League Standings"])

# 1. PUBLIC: Get all standings sorted by points (descending) then goal difference
@router.get("/", response_model=List[schemas.StandingResponse])
def get_standings(db: Session = Depends(get_db)):
    standings = db.query(models.Standing).order_by(
        models.Standing.points.desc(),
        (models.Standing.goals_for - models.Standing.goals_against).desc()
    ).all()
    return standings

# 2. ADMIN: Add a team to the standings table (Secured)
@router.post("/", response_model=schemas.StandingResponse, status_code=status.HTTP_201_CREATED)
def create_standing(
    standing: schemas.StandingCreate, 
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    existing_team = db.query(models.Standing).filter(models.Standing.team_name == standing.team_name).first()
    if existing_team:
        raise HTTPException(status_code=400, detail="Team already exists in the standings table")
    
    try:
        new_standing = models.Standing(**standing.model_dump())
        db.add(new_standing)
        db.commit()
        db.refresh(new_standing)
        return new_standing
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# 3. ADMIN: Update team stats (Secured)
@router.put("/{standing_id}", response_model=schemas.StandingResponse)
def update_standing(
    standing_id: int, 
    update_data: schemas.StandingUpdate, 
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    team = db.query(models.Standing).filter(models.Standing.id == standing_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team standings entry not found")
    
    try:
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(team, key, value)
            
        db.commit()
        db.refresh(team)
        return team
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# 4. ADMIN: Delete a team from standings (Secured)
@router.delete("/{standing_id}", status_code=status.HTTP_200_OK)
def delete_standing(
    standing_id: int, 
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    team = db.query(models.Standing).filter(models.Standing.id == standing_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team standings entry not found")
    
    try:
        db.delete(team)
        db.commit()
        return {"message": "Team removed from standings successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))