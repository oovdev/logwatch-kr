# app/main.py

from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.routes import log_routes

load_dotenv()

app = FastAPI()

app.include_router(log_routes.router)

@app.get("/")
def root():
    return {
        "status": "LogWatch.kr API is running",
        "env": os.getenv("APP_ENV", "dev")
    }

