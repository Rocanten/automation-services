import requests
from datetime import datetime, timedelta, date

from app.config import jira_server_base_url, jira_server_personal_token
from app.yandex.connect import get_user_by
from app.models.worklog import Worklog


headers = {
        'Authorization':f'Bearer {jira_server_personal_token}',
        "Cache-Control": "no-cache, max-age=0"
    }

def request_logged_ids(since: int) -> dict:
	worklogIds = []
	s = requests.session()
	payload = {
		'since': since
	}
	response = s.get(
		jira_server_base_url + f'/worklog/updated', 
		params=payload, 
		headers=headers,
		timeout=6
		)
	response_json = response.json()
	values = response_json['values']
	for value in values:
		worklogIds.append(value['worklogId'])
	last_page = response_json['lastPage']
	until = response_json['until']
	result = {
		'worklogIds': worklogIds,
		'lastPage': last_page,
		'until': until
	}
	return result

def request_worklogs(ids: list) -> list:
	result = []
	s = requests.session()
	payload = {
		'ids': ids
	}
	response = s.post(
		jira_server_base_url + f'/worklog/list', 
		json=payload, 
		headers=headers,
		timeout=6
		)
	response_json = response.json()
	for item in response_json:
		start = datetime.strptime(item['started'], '%Y-%m-%dT%H:%M:%S.%f%z')
		created = datetime.strptime(item['started'], '%Y-%m-%dT%H:%M:%S.%f%z')
		try:
			user = get_user_by(item['author']['emailAddress'])
			author_id = user.yandex_id
		except KeyError as error:
			print(f'No user with email {item["author"]["emailAddress"]}')
			continue
		except AttributeError as error:
			print(f'No user with email {item["author"]["emailAddress"]}')
			continue
		worklog = Worklog(
				author_email=item['author']['emailAddress'],
				created=created,
				start=start,
				duration=item['timeSpentSeconds'],
				author_yandex_id=author_id,
				author_name=user.display_name,
				jira_issue_id=item['issueId']
			)
		result.append(worklog)
	return result

def attribute_worklogs(worklogs: list) -> list:
	attributed_worklogs = []
	issue_ids = []
	for worklog in worklogs:
		issue_ids.append(str(worklog.jira_issue_id))

	s = requests.session()
	ids = ','.join(issue_ids)
	payload = {
	    'jql': f'id in ({ids})',
	    'startAt': 0,
	    'maxResults': 1000,
	    'fields': [
	        'summary',
	        'status'
	    ]
	}
	response = s.post(
		jira_server_base_url + f'/search', 
		json=payload, 
		headers=headers,
		timeout=6
		)
	response_json = response.json()
	issues = response_json['issues']

	for worklog in worklogs:
		issue = next((issue for issue in issues if int(issue['id']) == worklog.jira_issue_id), None)
		if not issue:
			continue
		worklog.project = issue['key'].split('-')[0]
		worklog.issue_key = issue['key']
		worklog.issue_summary = issue['fields']['summary']
		worklog.status = issue['fields']['status']['name']
		attributed_worklogs.append(worklog)
	return attributed_worklogs
		

def get_worklogs(since: int = None) -> list:
	if not since:
		since = int(round((datetime.now() - timedelta(days=31)).timestamp()))*1000
	last_page = False
	since_timestamp = since
	worklogs = []
	while not last_page:
		result = request_logged_ids(since_timestamp)
		since_timestamp = result['until']
		last_page = result['lastPage']
		chunk = request_worklogs(result['worklogIds'])
		attributed_chunk = attribute_worklogs(chunk)
		worklogs.extend(attributed_chunk)
	return worklogs



		

