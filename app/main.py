from fastapi import FastAPI
from app.routers import health

app = FastAPI(
    title="PocketTrader API",
    description="Prop trading performance analytics for CSV and ProjectX/Topstep accounts",
    version="0.1.0"
)

app.include_router(health.router)
