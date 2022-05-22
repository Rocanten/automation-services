# Chat commands

## Overview
This project provides a ready to use application for adding new commands to mattermost and other messaging apps.

At this time the app supports following commands:
* time [me] [week] - get logged time from Yandex Tracker for current mattermost user during current week.

Important! Users in mattermost and yandex tracker must have the same email address.

## Install
First, you should create your local .env file and provide your settings for Mattermost and Yandex services. Below is an example of .env content:

    MATTERMOST_BASE_URL=<mattermost url>
    MATTERMOST_TOKEN=<mattermost token>
    YANDEX_TRACKER_BASE_URL=<yandex tracker base url>
    YANDEX_CONNECT_BASE_URL=<yandex connect base url>
    YANDEX_TOKEN=<yandex oauth token>
    YANDEX_ORG_ID=<yandex organization id>

You can build a docker image and run it locally or on you virtual machine.

    sudo docker build . -t <image-name>
    
After build you can run container with following command:

    docker run -p 80:80 -w /code -v "$(pwd):/code" <image-name>

Also the project has a ready build and deploy workflow for deploying in Yandex Cloud. You can find details in the workflow file: https://github.com/Rocanten/automation-services/blob/main/.github/workflows/main.yml

## Mattermost setup
You should setup a slash command to make everything work. 
The command for getting logged time should have two parameters:

    <command-name> [who] [period]
[who] is the user for whom logged time is displayed
[period] is the period for getting logged time. Now only one value is supported - _week_

## Dependencies
The app uses some third party libraries, which you can find in requirements.txt.
* fastapi - for simple web service with Rest API
* pydantic - fastapi dependency
* uvicorn - for simple python web server
* python-multipart - fastapi dependency to support form-data
* requests - for making http requests
* isodate - for parsing iso dates
* pytz - for timezones info

## Roadmap
I plan to add some features in the future:
* [x] Getting logged time for month
* [ ] Getting logged time for different user
* [ ] Integration with Jira
* [ ] Integration with Slack
* [ ] Integration with Telegram
* [ ] Auto sending messages about not logged time
* [ ] Deleting logged time
* [ ] Updating logged time

Also I would like to add commands for other info, like project metrics, team metrics, task stats etc.
    
## License
https://github.com/Rocanten/automation-services/blob/main/LICENSE
