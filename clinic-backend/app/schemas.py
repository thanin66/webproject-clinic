from datetime import datetime
from pydantic import BaseModel, EmailStr

# สำหรับ User
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: datetime | None = None
    address: str | None = None
    phone_number: str | None = None
    allergies: str | None = None
    chronic_conditions: str | None = None
    current_medications: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
        
class UserOut(UserBase):
    id: int
    date_joined: datetime

    model_config = {
        "from_attributes": True  # แทน orm_mode
    }


class User(UserBase):
    id: int
    date_joined: datetime

    model_config = {
        "from_attributes": True  # แทน orm_mode
    }

# สำหรับ Appointment
class AppointmentBase(BaseModel):
    patient_name: str
    doctor_name: str
    date: datetime
    description: str | None = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    patient_name: str | None = None
    doctor_name: str | None = None
    date: datetime | None = None
    description: str | None = None

class AppointmentOut(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
class Appointment(AppointmentBase):
    id: int

    model_config = {
        "from_attributes": True
    }

# สำหรับ JWT token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
