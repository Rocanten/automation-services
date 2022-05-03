import logging

from typing import Optional

from fastapi import FastAPI, Request, Form, Header, HTTPException

from app.mattermost.api import get_user_email

logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    return response

@app.get("/")
def get_main():
    return {
        "message": "Hello world :)",
        "user_message": "CD works"
    }

@app.post("/api/timelogged")
async def get_week_time(user_name: str = Form(...), text: str = Form(...),
                        authorization:str = Header(None)):
    try:
        email = get_user_email(user_name)
    except RuntimeError as error:
        raise HTTPException(status_code=404, detail=f"Cannot find user because an error occured: {error}")
    return {
        "response_type": "in_channel",
        "text": (f"Your email is: {email}")
    }
