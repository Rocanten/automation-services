import logging

from typing import Optional

from fastapi import FastAPI, Request, Form, Header, HTTPException

from app.timelog import get_logged_time
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
async def get_week_time(user_name: str = Form(...), text: Optional[str] = Form(None),
                        authorization:str = Header(None)):
    if not text:
        return message_back_response('You haven\'t provided any command. Please use help to get all available commands')
    try:
        email = get_user_email(user_name)
    except RuntimeError as error:
        raise HTTPException(status_code=404, detail=f"Cannot find user because an error occured: {error}")

    message = ''

    parameters = text.split(' ')[:2]
    if len(parameters) < 2:
        return message_back_response('Please, provide both parameters')

    if parameters[0] == 'me':
        try:
            message = get_logged_time(email, parameters[1])
        except RuntimeError as error:
            return message_back_response(str(error))
    else:
        return message_back_response('Unknown command')
    
    
    return message_back_response('You logged some time this week!\n'
                                 + message
                                 + '\nNote! You should log approx 40 hours per week and 8 hours per day')

def message_back_response(message: str):
    return {
        "response_type": "in_channel",
        "text": (message)
        }

