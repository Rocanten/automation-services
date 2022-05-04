import requests, datetime, isodate

from app.config import yandex_tracker_base_url, yandex_token, yandex_org_id, yandex_connect_base_url
from app.models.timelog import Timelog

headers = {
        'Authorization':f'OAuth {yandex_token}',
        'X-Org-ID': yandex_org_id
    }

def get_users():
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

users = get_users()

def get_logged_time_period(email: str, period_start, period_end)-> list:
    logged = []
    payload = {
        'createdBy': users[email],
        'createdAt': {
            'from': f'{period_start.isoformat()}',
            'to': f'{period_end.isoformat()}'
            }
        }
    r = requests.post(yandex_tracker_base_url + '/worklog/_search', json=payload, headers=headers)
    items = r.json()
    for item in items:
        issue = parse_object('issue', item)
        if not issue:
            continue
        issue_key = parse_string('key', issue)
        if not issue_key:
            continue
        comment = parse_string('comment', item)
        author = parse_object('createdBy', item)
        if not author:
            continue
        author_id = parse_number('id', author)
        created = parse_string('createdAt', item)
        start = parse_string('start', item)
        duration = parse_string('duration', item)
        if not (created or author_id or start or duration):
            raise RuntimeError('Fields createdAt or start or duration failed to parse')

        timelog = Timelog(issue_key, comment, author_id, created, start, duration)
        print(timelog)
        logged.append(timelog)
        
    return logged

def parse_string(name: str, obj):
    if not name in obj:
        return ''
    return obj[name]

def parse_number(name: str, obj):
    if not name in obj:
        return None
    return obj[name]

def parse_object(name: str, obj):
    if not name in obj:
        return None
    return obj[name]
