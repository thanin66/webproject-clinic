from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from .. import schemas, crud, database, auth
from ..auth import get_current_user

router = APIRouter(tags=["Users"])
get_db = database.get_db

# Register
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(crud.models.User).filter(
        (crud.models.User.username == user.username) | (crud.models.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    return crud.create_user(db, user)

# Login
from pydantic import BaseModel
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=schemas.Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, data.email)
    if not user or not auth.verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user
@router.get("/me")
def read_users_me(current_user: crud.models.User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "date_of_birth": current_user.date_of_birth,
        "address": current_user.address,
        "phone_number": current_user.phone_number,
        "allergies": current_user.allergies,
        "chronic_conditions": current_user.chronic_conditions,
        "current_medications": current_user.current_medications
    }

# Update profile
@router.put("/me/profile", response_model=schemas.UserResponse)
def update_profile(
    updated_data: schemas.UserUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: crud.models.User = Depends(get_current_user)
):
    for key, value in updated_data.dict(exclude_unset=True).items():
        if hasattr(current_user, key):
            setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user
