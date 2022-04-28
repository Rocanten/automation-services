from typing import Optional

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_main():
    return {"mes": False}

@app.post("/api/tracker/time")
def get_week_time(command: str, ):
    return {
        "response_type": "in_channel",
        "text": "Test"
    }
