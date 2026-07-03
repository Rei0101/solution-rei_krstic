from fastapi import FastAPI
from src.routers import tickets

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "TicketHub API is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(tickets.router)
