from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List,Optional


class Mood(str, Enum):
    PEACEFUL = "Peaceful"
    GRATEFUL = "Grateful"
    HAPPY = "Happy"
    INSPIRED = "Inspired"
    MOTIVATED = "Motivated"
    ANXIOUS = "Anxious"
    SAD = "Sad"
    ANGRY = "Angry"
    CONFUSED = "Confused"
    HOPEFUL = "Hopeful"
    



class AffirmationCreate(BaseModel):
    text: str


class AffirmationResponse(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True


class JournalCreate(BaseModel):
    title: str
    content: str
    mood: Mood
    
class JournalUpdate(BaseModel):
    title: str
    content: str      
    mood: Mood     


class JournalResponse(BaseModel):
    id: int
    title: str
    content: str
    mood: Mood
    created_at: datetime

    class Config:
        from_attributes = True
        
        
class MoodStat(BaseModel):
    mood: str
    count: int


class TopMoodItem(BaseModel):
    mood: str
    count: int


class TopMoodsResponse(BaseModel):
    top_moods: List[TopMoodItem]  
    
from datetime import date

class MorningRoutineCreate(BaseModel):
    date: date

    walk: bool = False
    yoga: bool = False

    surya_arghya: bool = False
    shiva_jal: bool = False
    vishnu_sahasranamam: bool = False


class MorningRoutineResponse(BaseModel):
    id: int

    date: date
    walk: bool
    yoga: bool
    surya_arghya: bool
    shiva_jal: bool
    vishnu_sahasranamam: bool

    class Config:
        from_attributes = True        
        
class MorningRoutineUpdate(BaseModel):
    walk: Optional[bool] = None
    yoga: Optional[bool] = None

    surya_arghya: Optional[bool] = None
    shiva_jal: Optional[bool] = None
    vishnu_sahasranamam: Optional[bool] = None    
    
from datetime import date

class SankalpCreate(BaseModel):
    date: date
    sankalp: str
    
class SankalpResponse(BaseModel):
    id: int

    date: date

    sankalp: str

    reflection: str | None = None

    fulfilled: bool | None = None

    class Config:
        from_attributes = True
        
class SankalpUpdate(BaseModel):
    reflection: str | None = None

    fulfilled: bool | None = None
    
from datetime import datetime

class GratitudeCreate(BaseModel):
    gratitude: str
    
class GratitudeResponse(BaseModel):
    id: int

    gratitude: str

    created_at: datetime

    class Config:
        from_attributes = True                            
        
        

    

    
   



