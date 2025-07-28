from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        orm_mode = True

class AppointmentCreate(BaseModel):
    doctor_name: str
    appointment_date: datetime
    reason: Optional[str] = None

class AppointmentOut(AppointmentCreate):
    id: int
    user_id: int
    class Config:
        orm_mode = True
