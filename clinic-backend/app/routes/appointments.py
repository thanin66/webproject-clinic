# routers/appointments.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, database, auth

router = APIRouter(prefix="/appointments", tags=["Appointments"])
get_db = database.get_db

# ---------------- Create ----------------
@router.post("/", response_model=schemas.AppointmentOut)
def create_appointment(appointment: schemas.AppointmentCreate,
                       db: Session = Depends(get_db),
                       current_user = Depends(auth.get_current_user)):
    if appointment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot create appointment for another user")
    return crud.create_appointment(db, appointment)

# ---------------- Read All ----------------
@router.get("/", response_model=List[schemas.AppointmentOut])
def read_appointments(skip: int = 0, limit: int = 100,
                      db: Session = Depends(get_db),
                      current_user = Depends(auth.get_current_user)):
    return [a for a in crud.get_appointments(db, skip, limit) if a.user_id == current_user.id]

# ---------------- Read One ----------------
@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def read_appointment(appointment_id: int,
                     db: Session = Depends(get_db),
                     current_user = Depends(auth.get_current_user)):
    appointment = crud.get_appointment(db, appointment_id)
    if not appointment or appointment.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

# ---------------- Update ----------------
@router.put("/{appointment_id}", response_model=schemas.AppointmentOut)
def update_appointment(appointment_id: int,
                       appointment_update: schemas.AppointmentUpdate,
                       db: Session = Depends(get_db),
                       current_user = Depends(auth.get_current_user)):
    appointment = crud.get_appointment(db, appointment_id)
    if not appointment or appointment.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return crud.update_appointment(db, appointment_id, appointment_update)

# ---------------- Delete ----------------
@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int,
                       db: Session = Depends(get_db),
                       current_user = Depends(auth.get_current_user)):
    appointment = crud.get_appointment(db, appointment_id)
    if not appointment or appointment.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Appointment not found")
    crud.delete_appointment(db, appointment_id)
    return {"detail": "Appointment deleted"}
