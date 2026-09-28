import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile, Request
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil

import models, schemas
from database import SessionLocal
# Assuming you have your auth dependency function imported here:
# from auth import get_current_admin 

router = APIRouter(
    prefix="/news",
    tags=["News"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.NewsResponse])
def get_news(db: Session = Depends(get_db)):
    return db.query(models.News).all()

@router.get("/{news_id}", response_model=schemas.NewsResponse)
def get_single_news(news_id: int, db: Session = Depends(get_db)):
    article = db.query(models.News).filter(models.News.id == news_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="News article not found")
    return article

@router.post("/", response_model=schemas.NewsResponse)
def add_news(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    image_url: Optional[str] = Form(None),
    pdf_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    # current_admin = Depends(get_current_admin) # Uncomment when ready to enforce admin token check
):
    pdf_url = None
    if pdf_file:
        upload_dir = "static/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename to prevent overwrites
        file_extension = os.path.splitext(pdf_file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        local_path = os.path.join(upload_dir, unique_filename)
        
        with open(local_path, "wb") as buffer:
            shutil.copyfileobj(pdf_file.file, buffer)
            
        # Dynamically build the base URL from the incoming request (supports production domains & ports)
        base_url = str(request.base_url).rstrip("/")
        pdf_url = f"{base_url}/static/uploads/{unique_filename}"

    try:
        new_article = models.News(
            title=title,
            content=content,
            image_url=image_url,
            pdf_url=pdf_url,
            author_id=1
        )
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        return new_article
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error saving news article: {str(e)}")

@router.post("/bulk", response_model=List[schemas.NewsResponse])
def create_bulk_news(news_list: List[schemas.NewsCreate], db: Session = Depends(get_db)):
    created_news = []
    try:
        for item in news_list:
            new_article = models.News(
                title=item.title,
                content=item.content,
                image_url=getattr(item, 'image_url', None),
                pdf_url=getattr(item, 'pdf_url', None),
                author_id=1
            )
            db.add(new_article)
            db.commit()
            db.refresh(new_article)
            created_news.append(new_article)
        return created_news
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating bulk news: {str(e)}")

@router.delete("/")
def delete_all_news(db: Session = Depends(get_db)):
    try:
        db.query(models.News).delete()
        db.commit()
        return {"message": "All news articles have been cleared successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{news_id}")
def delete_news(news_id: int, db: Session = Depends(get_db)):
    article = db.query(models.News).filter(models.News.id == news_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="News article not found")
    
    try:
        db.delete(article)
        db.commit()
        return {"message": "News article deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))