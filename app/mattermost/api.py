import requests

from app.config import mattermost_base_url, mattermost_token

def get_user_email(username: str):
    headers = {
        'Authorization': f'Bearer {mattermost_token}'
        }
    r = requests.get(f'{mattermost_base_url}/users/username/{username}', headers=headers)
    if r.status_code == 404:
        raise RuntimeError("User not found in mattermost")
    elif r.status_code == 401:
        raise RuntimeError("Your mattermost token is invalid")
    elif r.status_code != 200:
        raise RuntimeError("Unexpected error from mattermosr")
    json = r.json()
    email = json['email']
    return email
