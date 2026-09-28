from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Hashed password
    role = Column(String, default="admin")

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    jersey_number = Column(Integer)
    position = Column(String)
    photo_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    
    # --- Player Statistics Columns ---
    matches_played = Column(Integer, default=0)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    opponent = Column(String)
    match_date = Column(Date)
    match_time = Column(Time)
    venue = Column(String)
    competition = Column(String)
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    status = Column(String, default="upcoming") # upcoming, completed, or cancelled

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    image_url = Column(String, nullable=True)
    pdf_url = Column(String, nullable=True)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"))

class Gallery(Base):
    __tablename__ = "gallery"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Training(Base):
    __tablename__ = "training"
    id = Column(Integer, primary_key=True, index=True)
    day = Column(String, nullable=True)
    title = Column(String, nullable=True)
    start_time = Column(String)  # Stored as string to support "10:00 AM" format
    end_time = Column(String)    # Stored as string to support "12:00 PM" format
    venue = Column(String, nullable=True)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=True)

class ContactMessage(Base):
    __tablename__ = "contact_messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String, nullable=True)
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="unread")

class Standing(Base):
    __tablename__ = "standings"
    
    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, unique=True, index=True, nullable=False)
    position = Column(Integer, default=1)
    played = Column(Integer, default=0)
    won = Column(Integer, default=0)
    drawn = Column(Integer, default=0)
    lost = Column(Integer, default=0)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    points = Column(Integer, default=0)

class SocialLink(Base):
    __tablename__ = "social_links"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, unique=True, index=True)
    url = Column(String)