import logging

from typing import Optional

from fastapi import FastAPI, Request, Form, Header

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
    token = authorization.split(' ')[1]
    return {
        "response_type": "in_channel",
        "text": (f"Your parameters were: text={text} \n token={token}")
    }
