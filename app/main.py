import os
import asyncio
import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from app.solver import solve_quiz_task
from app.config import load_settings
from dotenv import load_dotenv
load_dotenv()
import os
import sys

# Required fix for Windows + Playwright
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


app = FastAPI(title="LLM Quiz Solver", version="2.0")

settings = load_settings()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

class QuizPayload(BaseModel):
    email: str
    secret: str
    url: str

@app.post("/quiz")
async def quiz_handler(payload: QuizPayload, request: Request):
    logging.info("Incoming request from %s", payload.email)

    # Validate secret
    if payload.secret != settings.SECRET_KEY:
        logging.warning("Invalid secret attempted: %s", payload.secret)
        raise HTTPException(status_code=403, detail="Invalid secret token")

    try:
        answer = await solve_quiz_task(
            email=payload.email,
            secret=payload.secret,
            first_url=payload.url
        )
        return {"success": True, "answer": answer}
    except Exception as e:
        logging.error("Quiz solving failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "LLM Quiz Solver is running!"}
