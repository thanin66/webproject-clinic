from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_appointments():
    return {"appointments": []}
