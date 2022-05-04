# Mattermost commands for Yandex Tracker

## Overview
This project provides a ready to use application for adding new commands to mattermost.

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
