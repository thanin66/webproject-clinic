from fastapi import FastAPI
from .database import engine, Base
import app.models  # ต้อง import models ก่อน create_all
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users, appointments

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created")

app = FastAPI()  # Instantiate FastAPI app

app.include_router(users.router)  
app.include_router(appointments.router)
# ตั้งค่า CORS

origins = [
    "http://localhost:8080",  # frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI with PostgreSQL!"}
