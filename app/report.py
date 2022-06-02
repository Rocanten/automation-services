from datetime import datetime, timedelta, date
import pytz, pandas, numpy
from pathlib import Path  

from app.yandex.tracker import get_all_worklogs
from utils.datetime import get_month_start, get_month_end


def get_report_link(period: str, project: str) -> str:
	report_link = ''
	if period == 'month':
		report_link = get_report_current_month(project)
	return report_link

def get_report_current_month(project: str) -> str:
    now = datetime.now()
    day_last_month = now - timedelta(days=now.day+5)
    month_start = get_month_start(day_last_month)
    month_end = get_month_end(day_last_month)
    worklogs = get_all_worklogs(month_start, month_end)
    df = pandas.DataFrame(worklogs)
    df_project = df[df['project'] == project.upper()]
    df_project = df_project.replace({'author_id': '1130000052766710'}, 'pm')
    df_pivot = pandas.pivot_table(df_project, values='duration', index=['issue_key'], columns='author_id', aggfunc=numpy.sum)
    df_pivot.to_csv('static/out.csv', index=True)
    return 'http://127.0.0.1:80/static/out.csv'

