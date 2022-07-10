import requests

from app.config import yandex_token, yandex_org_id, yandex_connect_base_url

headers = {
        'Authorization':f'OAuth {yandex_token}',
        'X-Org-ID': yandex_org_id,
        "Cache-Control": "no-cache, max-age=0"
    }

def get_users_email_id():
    result = {}
    payload = {
        'fields': 'email',
        'page': 1,
        'per_page': 1000
        }
    r = requests.get(yandex_connect_base_url + '/users', params=payload, headers=headers)
    if r.status_code != 200:
        print(r.json())
    users = r.json()['result']
    for user in users:
        result[user['email']] = user['id']
    return result

def get_users_id_email():
    result = {}
    payload = {
        'fields': 'email',
        'page': 1,
        'per_page': 1000
        }
    r = requests.get(yandex_connect_base_url + '/users', params=payload, headers=headers)
    if r.status_code != 200:
        print(r.json())
    users = r.json()['result']
    for user in users:
        result[user['id']] = user['email']
    return result
