from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import SessionLocal

# Create the router
router = APIRouter(
    prefix="/players",
    tags=["Players"]
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET: Fetch all players
@router.get("/", response_model=List[schemas.PlayerResponse])
def get_players(db: Session = Depends(get_db)):
    return db.query(models.Player).all()

# POST: Add a new player (single)
@router.post("/", response_model=schemas.PlayerResponse)
def add_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    new_player = models.Player(**player.model_dump())
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player

# POST: Add multiple players at once (Batch)
@router.post("/batch", response_model=List[schemas.PlayerResponse])
def add_multiple_players(players: List[schemas.PlayerCreate], db: Session = Depends(get_db)):
    db_players = [models.Player(**p.model_dump()) for p in players]
    db.add_all(db_players)
    db.commit()
    for player in db_players:
        db.refresh(player)
    return db_players

# PUT: Update an existing player
@router.put("/{player_id}", response_model=schemas.PlayerResponse)
def update_player(player_id: int, updated_player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Update fields
    player.name = updated_player.name
    player.jersey_number = updated_player.jersey_number
    player.position = updated_player.position
    player.photo_url = updated_player.photo_url
    player.bio = updated_player.bio
    
    db.commit()
    db.refresh(player)
    return player

# DELETE: Remove a player
@router.delete("/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    db.delete(player)
    db.commit()
    return {"message": "Player deleted successfully"}