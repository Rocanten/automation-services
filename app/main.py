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
        "user_message": "CD works!"
    }


@app.post("/api/timelogged")
async def get_time(user_name: str = Form(...), text: Optional[str] = Form(None),
                        authorization: str = Header(None)):
    if not text:
        return message_back_response('You haven\'t provided any command. Please use help to get all available commands')
    try:
        email = get_user_email(user_name)
    except RuntimeError as error:
        raise HTTPException(status_code=404, detail=f"Cannot find user because an error occured: {error}")

    message = ''

    parameters = text.split(' ')[:2]
    if len(parameters) < 2:
        if parameters[0] == 'me':
            return message_back_response('Please, provide both parameters')
        elif parameters[0] == 'help':
            return message_back_response(get_help_text())
        else:
            return message_back_response('Unknown command. Please use help to get all available commands')

    if parameters[0] == 'me':
        try:
            message = get_logged_time(email, parameters[1])
        except RuntimeError as error:
            return message_back_response(str(error))
    else:
        return message_back_response('Unknown command. Please use help to get all available commands')
    
    
    return message_back_response('Here is your logged time for the period!\n'
                                 + message
                                 + '\n\nNote! You should log approx 40 hours per week and 8 hours per day')


def message_back_response(message: str):
    return {
        "response_type": "in_channel",
        "text": (message)
        }

def get_help_text() -> str:
    return (f'*/time me week* - get logged time during current week\n' +
        f'*/time me lastweek* - get logged time during last week\n' +
        f'*/time me month* - get logged time during current month\n' +
        f'*/time me lastmonth* - get logged time during last month\n')
