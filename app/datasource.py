from app.yandex.tracker import get_raw_logged_time_period as get_worklogs_from_yandex
from app.jira.worklogs import get_worklogs as get_worklogs_from_jira

def get_raw_logged_time_period(email) -> list:
	yandex_worklogs = get_worklogs_from_yandex(email)
	jira_worklogs = get_worklogs_from_jira()
	jira_worklogs_filtered_by_email = [worklog for worklog in jira_worklogs if worklog['author_email'] == email]
	total_worklogs = yandex_worklogs
	for item in jira_worklogs_filtered_by_email:
		total_worklogs.append(item)
	return total_worklogs

 