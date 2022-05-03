import os

from misc.utils import *
from misc.export_env import *

set_env()

mattermost_base_url: str = os.getenv('MATTERMOST_BASE_URL')
mattermost_token: str = os.getenv('MATTERMOST_TOKEN')
