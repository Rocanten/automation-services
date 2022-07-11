import os

from misc.utils import *
from misc.export_env import *

set_env()

mattermost_base_url: str = os.getenv('MATTERMOST_BASE_URL')
mattermost_token: str = os.getenv('MATTERMOST_TOKEN')

yandex_tracker_base_url: str = os.getenv('YANDEX_TRACKER_BASE_URL')
yandex_token: str = os.getenv('YANDEX_TOKEN')
yandex_org_id: str = os.getenv('YANDEX_ORG_ID')
yandex_connect_base_url: str = os.getenv('YANDEX_CONNECT_BASE_URL')

jira_server_base_url: str = os.getenv('JIRA_SERVER_BASE_URL')
jira_server_personal_token: str = os.getenv('JIRA_SERVER_PERSONAL_TOKEN')


service_url: str = os.getenv('SERVICE_ADDRESS')

departments_for_time_reports = (2, 5, 6, 7, 8, 9, 10, 11)
