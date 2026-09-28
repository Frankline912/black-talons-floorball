from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from .auth import get_current_admin

router = APIRouter(
    prefix="/socials",
    tags=["Social Media"]
)

@router.get("/", response_model=list[schemas.SocialLinkResponse])
def get_social_links(db: Session = Depends(get_db)):
    return db.query(models.SocialLink).all()

@router.post("/", response_model=schemas.SocialLinkResponse)
def upsert_social_link(link: schemas.SocialLinkCreate, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    existing = db.query(models.SocialLink).filter(models.SocialLink.platform == link.platform).first()
    if existing:
        existing.url = link.url
        db.commit()
        db.refresh(existing)
        return existing
    
    new_link = models.SocialLink(**link.dict())
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link