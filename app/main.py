import logging

from typing import Optional

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from fastapi import FastAPI, Request, Form, Header, HTTPException

from app.mattermost.api import get_user_email
=======
from fastapi import FastAPI, Request, Form, Header
>>>>>>> 6d7b134 (Testing back message)
=======
from fastapi import FastAPI, Request
>>>>>>> c209e46 (Added logging to file)
=======
from fastapi import FastAPI, Request, Form
>>>>>>> 8b86307 (Testing back message)
=======
from fastapi import FastAPI, Request, Form, Header
>>>>>>> c85d206 (Testing back message)
=======
from fastapi import FastAPI, Request, Form, Header, HTTPException

from app.mattermost.api import get_user_email
>>>>>>> dbdf893 (Added env)
=======
from fastapi import FastAPI, Request, Form, Header
>>>>>>> 9c9b9ec (Testing back message)

logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
    json = await request.json()
    print(json)
    logging.debug(json)
>>>>>>> c209e46 (Added logging to file)
=======
    body = b''
    async for chunk in request.stream():
        body += chunk
    print(body)
    logging.debug(body)
>>>>>>> 103c98d (Added logging to file)
=======
>>>>>>> 8b86307 (Testing back message)
    return response

@app.get("/")
def get_main():
    return {
        "message": "Hello world :)",
        "user_message": "CD works"
    }

@app.post("/api/timelogged")
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
async def get_week_time(user_name: str = Form(...), text: str = Form(...),
                        authorization:str = Header(None)):
    token = authorization.split(' ')[1]
<<<<<<< HEAD
    try:
        email = get_user_email(user_name)
    except RuntimeError as error:
        raise HTTPException(status_code=404, detail=f"Cannot find user because an error occured: {error}")
=======
>>>>>>> 6d7b134 (Testing back message)
=======
def get_week_time(command: str, ):
>>>>>>> c209e46 (Added logging to file)
    return {
        "response_type": "in_channel",
        "text": (f"Your email is: {email}")
=======
async def get_week_time(user_name: str = Form(...), text: str = Form(...)):
    return {
        "response_type": "in_channel",
        "text": f"Your parameters were: {text}"
>>>>>>> 8b86307 (Testing back message)
=======
async def get_week_time(user_name: str = Form(...), text: str = Form(...), token:str = Form(...)):
=======
async def get_week_time(user_name: str = Form(...), text: str = Form(...),
                        authorization:str = Header(None)):
    token = authorization.split(' ')[1]
<<<<<<< HEAD
>>>>>>> c85d206 (Testing back message)
=======
async def get_week_time(user_name: str = Form(...), text: str = Form(...),
                        authorization:str = Header(None)):
    token = authorization.split(' ')[1]
>>>>>>> 9c9b9ec (Testing back message)
    return {
        "response_type": "in_channel",
        "text": (f"Your parameters were: text={text} \n token={token}")
>>>>>>> 0923fde (Testing back message)
=======
    try:
        email = get_user_email(user_name)
    except RuntimeError as error:
        raise HTTPException(status_code=404, detail=f"Cannot find user because an error occured: {error}")
    return {
        "response_type": "in_channel",
        "text": (f"Your email is: {email}")
>>>>>>> dbdf893 (Added env)
    }
