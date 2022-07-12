from app.yandex.tracker import get_raw_logged_time_period as get_worklogs_from_yandex
from app.jira.worklogs import get_worklogs as get_worklogs_from_jira
from app.models.worklog import Worklog
from app.yandex.tracker import get_all_worklogs as get_all_worklogs_from_yandex
from app.jira.worklogs import get_worklogs as get_all_worklogs_from_jira
from datetime import datetime


def get_raw_logged_time_period(email) -> list:
	yandex_worklogs = get_worklogs_from_yandex(email)
	jira_worklogs = get_worklogs_from_jira()
	jira_worklogs_filtered_by_email = [worklog for worklog in jira_worklogs if worklog.author_email == email]
	total_worklogs = yandex_worklogs
	for item in jira_worklogs_filtered_by_email:
		total_worklogs.append(item)
	return total_worklogs

def get_all_worklogs(period_start: datetime = None, period_end: datetime = None):
	yandex_worklogs = get_all_worklogs_from_yandex(period_start, period_end)
	jira_worklogs = get_all_worklogs_from_jira(int(round(period_start.timestamp()))*1000)
	total_worklogs = yandex_worklogs
	for item in jira_worklogs:
		total_worklogs.append(item)
	print(total_worklogs[:5])
	return total_worklogs
 