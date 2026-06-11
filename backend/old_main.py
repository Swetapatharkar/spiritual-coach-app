from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import schemas
from sqlalchemy import func


from database import engine
from database import SessionLocal
from datetime import datetime,timedelta
from datetime import date

from models import Base
from models import Affirmation
from models import JournalEntry
from collections import defaultdict
from models import MorningRoutine
from models import Sankalp
from models import GratitudeEntry

from schemas import (
    AffirmationCreate,
    AffirmationResponse,
    JournalCreate,
    JournalUpdate,
    JournalResponse
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Spiritual Coach API Running"
    }


# -------------------------
# AFFIRMATIONS
# -------------------------

@app.post("/affirmations", response_model=AffirmationResponse)
def create_affirmation(affirmation: AffirmationCreate):

    db: Session = SessionLocal()

    new_affirmation = Affirmation(
        text=affirmation.text
    )

    db.add(new_affirmation)
    db.commit()
    db.refresh(new_affirmation)

    db.close()

    return new_affirmation


@app.get("/affirmations", response_model=list[AffirmationResponse])
def get_affirmations():

    db: Session = SessionLocal()

    affirmations = db.query(Affirmation).all()

    db.close()

    return affirmations


# -------------------------
# JOURNALS
# -------------------------

@app.post("/journal", response_model=JournalResponse)
def create_journal(journal: JournalCreate):

    db: Session = SessionLocal()

    new_journal = JournalEntry(
        title=journal.title,
        content=journal.content,
        mood=journal.mood
    )

    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)

    db.close()

    return new_journal


@app.get("/journal", response_model=list[JournalResponse])
def get_journals(
    mood: Optional[schemas.Mood] = None,
    days: Optional[int] = None
):

    db: Session = SessionLocal()

    query = db.query(JournalEntry)

    if mood:
        query = query.filter(
            JournalEntry.mood == mood.value
        )

    if days:
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        query = query.filter(
            JournalEntry.created_at >= cutoff_date
        )

    journals = query.order_by(
        JournalEntry.created_at.desc()
    ).all()

    db.close()

    return journals


@app.get("/journal/stats")
def journal_stats():

    db: Session = SessionLocal()

    stats = db.query(
        JournalEntry.mood,
        func.count(JournalEntry.id)
    ).group_by(
        JournalEntry.mood
    ).all()

    db.close()

    return [
        {
            "mood": mood,
            "count": count
        }
        for mood, count in stats
    ]
    
@app.get("/journal/stats/top-moods")
def top_moods():

    db: Session = SessionLocal()

    stats = db.query(
        JournalEntry.mood,
        func.count(JournalEntry.id)
    ).group_by(
        JournalEntry.mood
    ).all()

    db.close()

    if not stats:
        return {
            "message": "No journal entries found"
        }

    max_count = max(
        count
        for mood, count in stats
    )

    return {
        "top_moods": [
            {
                "mood": mood,
                "count": count
            }
            for mood, count in stats
            if count == max_count
        ]
    }
    
    
@app.get("/journal/stats/daily-trend")
def daily_trend():

    db: Session = SessionLocal()

    # Get all entries (you can later optimize with filters)
    records = db.query(
        JournalEntry.mood,
        JournalEntry.created_at
    ).all()

    db.close()

    # Step 1: group by date
    trend = defaultdict(lambda: defaultdict(int))

    for mood, created_at in records:
        date = created_at.date()   # extract YYYY-MM-DD
        trend[date][mood] += 1

    # Step 2: convert to frontend format
    result = []

    for date, moods in trend.items():
        result.append({
            "date": str(date),
            **moods
        })

    # Step 3: sort by date
    result.sort(key=lambda x: x["date"])

    return {
        "trend": result
    }   
    
    
@app.get("/journal/stats/streak")
def mood_streak():

    db: Session = SessionLocal()

    records = db.query(JournalEntry.created_at).all()

    db.close()

    if not records:
        return {
            "current_streak": 0,
            "message": "No journal entries yet"
        }

    # Step 1: extract unique dates
    dates = set(
        record.created_at.date()
        for record in records
    )

    # Step 2: start from today
    today = date.today()
    streak = 0

    current_day = today

    # Step 3: count backwards
    while current_day in dates:
        streak += 1
        current_day = current_day - timedelta(days=1)

    return {
        "current_streak": streak
    }     

@app.get("/journal/{journal_id}", response_model=JournalResponse)
def get_journal(journal_id: int):

    db: Session = SessionLocal()

    journal = db.query(JournalEntry).filter(
        JournalEntry.id == journal_id
    ).first()

    db.close()

    if journal is None:
        raise HTTPException(
            status_code=404,
            detail="Journal not found"
        )

    return journal


@app.put("/journal/{journal_id}",
         response_model=JournalResponse)
def update_journal(
    journal_id: int,
    updated_journal: JournalUpdate
):

    db: Session = SessionLocal()

    journal = db.query(JournalEntry).filter(
        JournalEntry.id == journal_id
    ).first()

    if journal is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Journal not found"
        )

    journal.title = updated_journal.title
    journal.content = updated_journal.content
    journal.mood=update_journal.mood

    db.commit()
    db.refresh(journal)

    db.close()

    return journal


@app.get("/journal/stats/recent")
def recent_mood_stats():

    db: Session = SessionLocal()

    cutoff_date = datetime.utcnow() - timedelta(days=7)

    stats = db.query(
        JournalEntry.mood,
        func.count(JournalEntry.id)
    ).filter(
        JournalEntry.created_at >= cutoff_date
    ).group_by(
        JournalEntry.mood
    ).all()

    db.close()

    return {
        mood: count
        for mood, count in stats
    }
    
@app.get(
    "/journal/stats/top-moods",
    response_model=schemas.TopMoodsResponse
)
def top_moods():

    db: Session = SessionLocal()

    stats = db.query(
        JournalEntry.mood,
        func.count(JournalEntry.id)
    ).group_by(
        JournalEntry.mood
    ).all()

    db.close()

    if not stats:
        return {
            "message": "No journal entries found"
        }

    max_count = max(count for mood, count in stats)

    return {
        "top_moods": [
            {
                "mood": mood,
                "count": count
            }
            for mood, count in stats
            if count == max_count
        ]
    }
# -------------------------
# Morning Routine JOURNAL
# -------------------------
@app.post(
    "/morning-routine",
    response_model=schemas.MorningRoutineResponse
)
def create_morning_routine(
    routine: schemas.MorningRoutineCreate
):

    db: Session = SessionLocal()

    existing = db.query(
        MorningRoutine
    ).filter(
        MorningRoutine.date == routine.date
    ).first()

    if existing:
        db.close()

        raise HTTPException(
            status_code=400,
            detail="Routine already exists for this date"
        )

    new_routine = MorningRoutine(
        **routine.model_dump()
    )

    db.add(new_routine)
    db.commit()
    db.refresh(new_routine)

    db.close()

    return new_routine
# -------------------------
# DELETE JOURNAL (FIXED)
# -------------------------

@app.delete("/journal/{journal_id}")
def delete_journal(journal_id: int):

    db: Session = SessionLocal()

    journal = db.query(JournalEntry).filter(
        JournalEntry.id == journal_id
    ).first()

    if journal is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Journal not found"
        )

    db.delete(journal)
    db.commit()
    db.close()

    return {
        "message": "Journal deleted successfully"
    }
    
@app.patch(
    "/morning-routine/{routine_date}",
    response_model=schemas.MorningRoutineResponse
)
def update_morning_routine(
    routine_date: date,
    updates: schemas.MorningRoutineUpdate
):
    db: Session = SessionLocal()

    routine = db.query(MorningRoutine).filter(
        MorningRoutine.date == routine_date
    ).first()

    if routine is None:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Morning routine not found"
        )

    update_data = updates.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            routine,
            field,
            value
        )

    db.commit()
    db.refresh(routine)

    db.close()

    return routine    

@app.get(
    "/morning-routine/{routine_date}",
    response_model=schemas.MorningRoutineResponse
)
def get_morning_routine(routine_date: date):

    db: Session = SessionLocal()

    routine = db.query(MorningRoutine).filter(
        MorningRoutine.date == routine_date
    ).first()

    db.close()

    if routine is None:
        raise HTTPException(
            status_code=404,
            detail="Morning routine not found"
        )

    return routine

@app.get(
    "/morning-routine",
    response_model=list[schemas.MorningRoutineResponse]
)
def get_all_morning_routines():

    db: Session = SessionLocal()

    routines = db.query(
        MorningRoutine
    ).order_by(
        MorningRoutine.date.desc()
    ).all()

    db.close()

    return routines

#-------------------------
# CREATE SANKALP
#-------------------------

@app.post(
    "/sankalp",
    response_model=schemas.SankalpResponse
)
def create_sankalp(
    sankalp: schemas.SankalpCreate
):

    db: Session = SessionLocal()

    existing = db.query(Sankalp).filter(
        Sankalp.date == sankalp.date
    ).first()

    if existing:
        db.close()

        raise HTTPException(
            status_code=400,
            detail="Sankalp already exists for this date"
        )

    new_sankalp = Sankalp(
        date=sankalp.date,
        sankalp=sankalp.sankalp
    )

    db.add(new_sankalp)

    db.commit()

    db.refresh(new_sankalp)

    db.close()

    return new_sankalp

@app.get(
    "/sankalp",
    response_model=list[schemas.SankalpResponse]
)
def get_sankalps():

    db: Session = SessionLocal()

    sankalps = db.query(
        Sankalp
    ).order_by(
        Sankalp.date.desc()
    ).all()

    db.close()

    return sankalps


@app.get(
    "/sankalp/{sankalp_date}",
    response_model=schemas.SankalpResponse
)
def get_sankalp(
    sankalp_date: date
):

    db: Session = SessionLocal()

    sankalp = db.query(
        Sankalp
    ).filter(
        Sankalp.date == sankalp_date
    ).first()

    db.close()

    if sankalp is None:
        raise HTTPException(
            status_code=404,
            detail="Sankalp not found"
        )

    return sankalp


# -------------------------
# AFFIRMATIONS
# -------------------------
@app.post(
    "/gratitude",
    response_model=schemas.GratitudeResponse
)
def create_gratitude(
    gratitude: schemas.GratitudeCreate
):

    db: Session = SessionLocal()

    new_gratitude = GratitudeEntry(
        gratitude=gratitude.gratitude
    )

    db.add(new_gratitude)

    db.commit()

    db.refresh(new_gratitude)

    db.close()

    return new_gratitude


@app.get(
    "/gratitude",
    response_model=list[schemas.GratitudeResponse]
)
def get_gratitude_entries():

    db: Session = SessionLocal()

    entries = db.query(
        GratitudeEntry
    ).order_by(
        GratitudeEntry.created_at.desc()
    ).all()

    db.close()

    return entries


