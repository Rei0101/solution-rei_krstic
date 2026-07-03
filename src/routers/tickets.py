from fastapi import APIRouter

router = APIRouter()


@router.get("/tickets")
async def get_tickets():
    return {"message": "Needs to display all tickets"}
