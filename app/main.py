import logging

from typing import Optional

from fastapi import FastAPI, Request

logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    json = await request.json()
    print(json)
    logging.debug(json)
    return response

@app.get("/")
def get_main():
    return {
        "message": "Hello world :)",
        "user_message": "CD works"
    }

@app.post("/api/timelogged")
def get_week_time(command: str, ):
    return {
        "response_type": "in_channel",
        "text": "Test"
    }
