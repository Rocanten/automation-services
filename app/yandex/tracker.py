import requests, datetime, isodate, logging, uuid
from datetime import datetime as dt
from datetime import timedelta

from app.config import yandex_tracker_base_url, yandex_token, yandex_org_id, yandex_connect_base_url
from app.models.timelog import Timelog
from utils.datetime import iso_duration_to_work_seconds

PER_PAGE = 300

logging.basicConfig(level=logging.DEBUG)

headers = {
        'Authorization':f'OAuth {yandex_token}',
        'X-Org-ID': yandex_org_id,
        "Cache-Control": "no-cache, max-age=0"
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

def request_logged_time(email: str, days: int = 90) -> list:
    period_start = dt.now() - timedelta(days=days)
    period_end = dt.now()
    payload = {
    'createdBy': users[email],
        'createdAt': {
            'from': f'{(period_start - timedelta(minutes=1)).isoformat()}',
            'to': f'{period_end.isoformat()}'
            }
        }
    s = requests.session()
    response = s.post(yandex_tracker_base_url + f'/worklog/_search?perPage=1000', json=payload, headers=headers)
    return response.json()

def request_all_logged_time(period_start: datetime, period_end: datetime, page: int, per_page: int):
    result = []
    payload = {
        'createdAt':{}
    }

    if period_start:
        payload['createdAt']['from'] = period_start.isoformat()
    if period_end:
        payload['createdAt']['to'] = period_end.isoformat()
    s = requests.session()
    response = s.post(yandex_tracker_base_url + f'/worklog/_search?perPage={per_page}&page={page}', json=payload, headers=headers)
    raw = response.json()
    for item in raw:
        start = datetime.datetime.strptime(item['start'], '%Y-%m-%dT%H:%M:%S.%f%z')
        worklog = {
            'project': item['issue']['key'].split('-')[0],
            'issue_key': item['issue']['key'],
            'issue_display': item['issue']['display'],
            'author_id': item['createdBy']['id'],
            'author_name': item['createdBy']['display'],
            'createdAt': item['createdAt'],
            'start': item['start'],
            'start_date': start.strftime('%Y-%m-%d'),
            'duration': iso_duration_to_work_seconds(item['duration'], 8)
        }
        result.append(worklog)
    return result

def request_worklogs_count(period_start: datetime, period_end: datetime) -> int:
    payload = {
        'createdAt':{}
    }

    if period_start:
        payload['createdAt']['from'] = period_start.isoformat()
    if period_end:
        payload['createdAt']['to'] = period_end.isoformat()

    s = requests.session()
    response = s.post(yandex_tracker_base_url + f'/worklog/_search?perPage=1&page=1', json=payload, headers=headers)
    return int(response.headers['X-Total-Count'])

def get_all_worklogs(period_start: datetime = None, period_end: datetime = None):
    worklogs = []
    worklogs_count = request_worklogs_count(period_start, period_end)
    pages_count = worklogs_count // PER_PAGE + 1
    for page in range(1, pages_count + 1):
        chunk = request_all_logged_time(period_start, period_end, page, PER_PAGE)
        worklogs.extend(chunk)
    return worklogs


def get_raw_logged_time_period(email: str) -> list:
    result = []
    items = request_logged_time(email)
    for item in items:
        issue = parse_object('issue', item)
        if not issue:
            continue
        issue_key = parse_string('key', issue)
        if not issue_key:
            continue
        project = issue_key.split('-')[0]
        comment = parse_string('comment', item)
        author = parse_object('createdBy', item)
        if not author:
            continue
        author_id = parse_number('id', author)
        created = parse_string('createdAt', item)
        start = parse_string('start', item)
        start_date = dt.strptime(start, '%Y-%m-%dT%H:%M:%S.%f%z').date()
        duration = parse_string('duration', item)
        if not (created or author_id or start or duration):
            raise RuntimeError('Fields createdAt or start or duration failed to parse')
        timelog = {
            'issue_key': issue_key, 
            'project': project,
            'comment': comment, 
            'author_id': author_id, 
            'created': created, 
            'start': start,
            'start_date': start_date,
            'duration': iso_duration_to_work_seconds(duration, 8)
        }
        result.append(timelog)
    return result


def get_logged_time_period(email: str, period_start, period_end)-> list:
    logged = []
    items = request_logged_time(email, period_start, period_end)

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
