from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
import shutil
import os
import uuid
from typing import List

from database import get_db
import models
from schemas import GalleryResponse

router = APIRouter(prefix="/gallery", tags=["Gallery & Trophy Room"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 1. PUBLIC: Get all gallery photos
@router.get("/", response_model=List[GalleryResponse])
def get_gallery_photos(db: Session = Depends(get_db)):
    photos = db.query(models.Gallery).all()
    return photos

# 2. ADMIN: Upload a single trophy photo
@router.post("/", response_model=GalleryResponse, status_code=status.HTTP_201_CREATED)
async def upload_gallery_photo(
    request: Request,
    title: str = Form(...),
    image_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_extension = os.path.splitext(image_file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image_file.file, buffer)
        
    base_url = str(request.base_url).rstrip("/")
    image_url = f"{base_url}/static/uploads/{unique_filename}"

    try:
        new_photo = models.Gallery(
            title=title,
            image_url=image_url
        )
        db.add(new_photo)
        db.commit()
        db.refresh(new_photo)
        return new_photo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error saving photo: {str(e)}")

# 3. ADMIN: Upload multiple/bulk pictures at once
@router.post("/bulk", response_model=List[GalleryResponse], status_code=status.HTTP_201_CREATED)
async def upload_bulk_gallery_photos(
    request: Request,
    title_prefix: str = Form("Team Photo"),
    image_files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    uploaded_photos = []
    base_url = str(request.base_url).rstrip("/")
    
    try:
        for index, image_file in enumerate(image_files):
            file_extension = os.path.splitext(image_file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image_file.file, buffer)
                
            image_url = f"{base_url}/static/uploads/{unique_filename}"
            photo_title = f"{title_prefix} {index + 1}"

            new_photo = models.Gallery(
                title=photo_title,
                image_url=image_url
            )
            db.add(new_photo)
            uploaded_photos.append(new_photo)
            
        db.commit()
        for photo in uploaded_photos:
            db.refresh(photo)
            
        return uploaded_photos
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error uploading bulk photos: {str(e)}")

# 4. ADMIN: Delete a single gallery photo by ID
@router.delete("/{photo_id}", status_code=status.HTTP_200_OK)
def delete_gallery_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(models.Gallery).filter(models.Gallery.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    try:
        filename = photo.image_url.split("/")[-1]
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass

    try:
        db.delete(photo)
        db.commit()
        return {"message": "Photo successfully deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# 5. ADMIN: Delete all gallery photos
@router.delete("/", status_code=status.HTTP_200_OK)
def delete_all_gallery_photos(db: Session = Depends(get_db)):
    photos = db.query(models.Gallery).all()
    for photo in photos:
        try:
            filename = photo.image_url.split("/")[-1]
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass
        db.delete(photo)
        
    try:
        db.commit()
        return {"message": "All gallery photos cleared successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))