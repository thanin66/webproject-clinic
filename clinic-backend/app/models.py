from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    date_joined = Column(DateTime, default=datetime.utcnow)

    # ข้อมูล profile เพิ่มเติม
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    address = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    allergies = Column(String, nullable=True)
    chronic_conditions = Column(String, nullable=True)
    current_medications = Column(String, nullable=True)

    appointments = relationship("Appointment", back_populates="user")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_name = Column(String, nullable=False)
    appointment_time = Column(String, nullable=False)
    description = Column(String, nullable=True)
    reason = Column(String, nullable=True)
    status = Column(String, default="Scheduled")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="appointments")
