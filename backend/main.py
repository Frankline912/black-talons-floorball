import os
import uuid
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import models
from database import engine

# Import all routers
from routes import players, matches, news, training, contact, auth, gallery, standings, socials

# Generate database tables 
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Black Talons API",
    description="Full-stack API for the DEKUT Floorball Club (Black Talons)",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the upload directory exists and mount static files
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# General File Upload Endpoint with Collision Protection & Dynamic URL
@app.post("/upload/")
async def upload_file(request: Request, file: UploadFile = File(...)):
    # Extract file extension and generate a unique filename to prevent overwrites
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save the file asynchronously
    contents = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(contents)
        
    # Dynamically build base URL from the incoming request (works locally and on Render!)
    base_url = str(request.base_url).rstrip("/")
    return {"url": f"{base_url}/static/uploads/{unique_filename}"}

# Attach all routers
app.include_router(players.router)
app.include_router(matches.router)
app.include_router(news.router)
app.include_router(training.router)
app.include_router(contact.router)
app.include_router(auth.router)
app.include_router(gallery.router)
app.include_router(standings.router)
app.include_router(socials.router)

@app.get("/")
def root():
    return {"message": "Welcome to the DEKUT Floorball (Black Talons) API"}