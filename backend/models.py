from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from datetime import datetime
from database import Base
from sqlalchemy import Boolean, Date


class Affirmation(Base):
    __tablename__ = "affirmations"

    id = Column(Integer, primary_key=True, index=True)
    
    text = Column(String, nullable=False)


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    mood = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )     
    
    

class MorningRoutine(Base):
    __tablename__ = "morning_routines"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date, unique=True, nullable=False)

    walk = Column(Boolean, default=False)
    yoga = Column(Boolean, default=False)

    surya_arghya = Column(Boolean, default=False)
    shiva_jal = Column(Boolean, default=False)
    vishnu_sahasranamam = Column(Boolean, default=False)  
    
class Sankalp(Base):
    __tablename__ = "sankalps"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date, unique=True, nullable=False)

    sankalp = Column(String, nullable=False)

    reflection = Column(String, nullable=True)

    fulfilled = Column(Boolean, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
class GratitudeEntry(Base):
    __tablename__ = "gratitude_entries"

    id = Column(Integer, primary_key=True)

    date = Column(Date)

    gratitude = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
              
