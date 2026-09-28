from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from datetime import date, time, datetime

# --- USERS (Admin) ---
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Plain text password, to be hashed before saving")

class UserResponse(UserBase):
    id: int
    role: str = "admin"
    
    model_config = ConfigDict(from_attributes=True)


# --- PLAYERS ---
class PlayerBase(BaseModel):
    name: str = Field(..., min_length=2)
    jersey_number: int = Field(..., ge=0, le=99)
    position: str = Field(..., min_length=2)
    photo_url: Optional[str] = None
    bio: Optional[str] = None
    matches_played: Optional[int] = Field(default=0, ge=0)
    goals: Optional[int] = Field(default=0, ge=0)
    assists: Optional[int] = Field(default=0, ge=0)

class PlayerCreate(PlayerBase):
    pass

class PlayerResponse(PlayerBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# --- MATCHES ---
class MatchBase(BaseModel):
    opponent: str = Field(..., min_length=2)
    match_date: date
    match_time: time
    venue: str
    competition: str
    home_score: Optional[int] = Field(default=None, ge=0)
    away_score: Optional[int] = Field(default=None, ge=0)
    status: str = Field(default="upcoming", pattern="^(upcoming|ongoing|completed|postponed)$")

class MatchCreate(MatchBase):
    pass

class MatchResponse(MatchBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# --- NEWS ---
class NewsBase(BaseModel):
    title: str = Field(..., min_length=3)
    content: str = Field(..., min_length=10)
    image_url: Optional[str] = None
    pdf_url: Optional[str] = None

class NewsCreate(NewsBase):
    pass

class NewsResponse(NewsBase):
    id: int
    created_at: datetime
    author_id: int
    
    model_config = ConfigDict(from_attributes=True)


# --- CONTACT MESSAGES ---
class ContactBase(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: Optional[str] = None
    message: str = Field(..., min_length=5)

class ContactCreate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    status: str = "unread"
    
    model_config = ConfigDict(from_attributes=True)


# --- TRAINING SCHEDULE ---
class TrainingBase(BaseModel):
    day: str
    title: Optional[str] = None
    start_time: str
    end_time: str
    venue: str
    location: Optional[str] = None
    description: Optional[str] = None

class TrainingCreate(TrainingBase):
    pass

class TrainingResponse(TrainingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- GALLERY & TROPHY ROOM ---
class GalleryBase(BaseModel):
    title: str = Field(..., min_length=2)

class GalleryCreate(GalleryBase):
    pass

class GalleryResponse(GalleryBase):
    id: int
    image_url: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- LEAGUE STANDINGS ---
class StandingBase(BaseModel):
    team_name: str
    position: int
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0

class StandingCreate(StandingBase):
    pass

class StandingUpdate(BaseModel):
    position: Optional[int] = None
    played: Optional[int] = None
    won: Optional[int] = None
    drawn: Optional[int] = None
    lost: Optional[int] = None
    goals_for: Optional[int] = None
    goals_against: Optional[int] = None
    points: Optional[int] = None

class StandingResponse(StandingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- SOCIAL MEDIA LINKS ---
class SocialLinkCreate(BaseModel):
    platform: str
    url: str

class SocialLinkResponse(SocialLinkCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)