import requests
from datetime import datetime, timedelta

from app.config import yandex_token, yandex_org_id, yandex_connect_base_url
from app.models.user import User

headers = {
        'Authorization':f'OAuth {yandex_token}',
        'X-Org-ID': yandex_org_id,
        "Cache-Control": "no-cache, max-age=0"
    }


def get_users():
    result = []
    payload = {
        'fields': 'email,is_dismissed,is_enabled,department,name',
        'page': 1,
        'per_page': 1000
        }
    r = requests.get(yandex_connect_base_url + '/users', params=payload, headers=headers)
    if r.status_code != 200:
        print(r.json())
    users_json = r.json()['result']
    for user_json in users_json:
        try:
            department_id = user_json['department']['id']
        except:
            department_id = None
        first_name = user_json['name']['first']
        last_name =user_json['name']['last'] 
        user = User(
                email=user_json['email'],
                yandex_id=user_json['id'],
                name=user_json['name']['first'],
                surname=user_json['name']['last'],
                display_name=f'{first_name} {last_name}',
                department_id=department_id
            )
        result.append(user)
    return result

users = get_users()

def get_user_by(email: str = None, yandex_id: str = None):
    if email:
        return next((user for user in users if user.email == email), None)
    if yandex_id:
        return next((user for user in users if user.yandex_id == yandex_id), None)