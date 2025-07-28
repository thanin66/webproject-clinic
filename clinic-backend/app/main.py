from fastapi import FastAPI
from app.database import Base, engine
from app.routes import users, appointments

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Clinic API"}
