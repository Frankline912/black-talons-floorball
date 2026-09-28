from database import SessionLocal
import models
from datetime import date, time

def seed_data():
    db = SessionLocal()
    
    try:
        # Check if data already exists to prevent duplicates
        if db.query(models.Standing).first():
            print("Database already contains seed data.")
            return

        print("Seeding database with initial Black Talons data...")

        # 1. Seed Standings
        standings = [
            models.Standing(team_name="Black Talons DEKUT", position=1, played=5, won=4, drawn=1, lost=0, goals_for=22, goals_against=8, points=13),
            models.Standing(team_name="Nairobi Floorball Club", position=2, played=5, won=3, drawn=1, lost=1, goals_for=18, goals_against=12, points=10),
            models.Standing(team_name="Rift Valley Strikers", position=3, played=5, won=2, drawn=0, lost=3, goals_for=14, goals_against=16, points=6),
            models.Standing(team_name="Coastal Hawks", position=4, played=5, won=0, drawn=0, lost=5, goals_for=5, goals_against=23, points=0),
        ]
        db.add_all(standings)

        # 2. Seed Players
        players = [
            models.Player(name="Brian Kiprono", jersey_number=10, position="Forward", matches_played=5, goals=8, assists=4, bio="Team captain and leading goalscorer."),
            models.Player(name="Collins Mutua", jersey_number=1, position="Goaltender", matches_played=5, goals=0, assists=1, bio="Brick wall in defense with incredible reflexes."),
            models.Player(name="Amina Mohamed", jersey_number=7, position="Defender", matches_played=4, goals=2, assists=5, bio="Solid defensive anchor and playmaker."),
        ]
        db.add_all(players)

        # 3. Seed Matches
        matches = [
            models.Match(opponent="Nairobi Floorball Club", match_date=date(2026, 4, 10), match_time=time(14, 0), venue="DeKUT Indoor Arena", competition="National League", home_score=5, away_score=3, status="completed"),
            models.Match(opponent="Rift Valley Strikers", match_date=date(2026, 4, 18), match_time=time(16, 0), venue="Nakuru Gymnasium", competition="National League", status="upcoming"),
        ]
        db.add_all(matches)

        # 4. Seed News
        news_article = models.News(
            title="Black Talons Kick Off Season in Style!",
            content="The Black Talons floorball team started the new league campaign with a dominant 5-3 win over Nairobi Floorball Club.",
            author_id=1
        )
        db.add(news_article)

        db.commit()
        print("Successfully seeded database!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()