from datetime import datetime, timedelta, date
import pytz, pandas, numpy
from pathlib import Path  


from app.yandex.tracker import get_all_worklogs
from app.models.command import Command
from utils.datetime import get_month_start, get_month_end
from app.models.period import Period
from app.yandex.connect import get_users_email_id

delta_to_log_time = timedelta(days = 14)


def get_report_link(command: Command) -> str:
    report_link = ''
    if command.name == 'users':
        report_link = get_users_report(command)
    return report_link

def get_users_report(command: Command) -> str:
    if command.get_option('p'):
        period = command.get_period()


    worklogs = get_all_worklogs(period.startdate, period.enddate + delta_to_log_time)
    df = pandas.DataFrame(worklogs)

    print(command.get_option('u'))

    if command.get_option('u'):
        users_email_id = get_users_email_id()
        users = command.get_users()
        users = [str(users_email_id[user]) for user in users]
        df = df[df['author_id'].isin(users)]



    df['start'] = pandas.to_datetime(df['start'])
    df = df[(df['start'] > period.startdate.isoformat()) & (df['start'] <= period.enddate.isoformat())]

    if command.get_option('projects'):
        df = df.groupby(['author_name', 'start_date', 'project']).sum()
    else:
        df = df.groupby(['author_name', 'start_date']).sum()

    df.to_csv('static/tmp.csv', index=True, float_format='%.2f')

    df.sort_values(['author_name', 'start_date'], ascending=[True, True])

    if command.get_option('projects'):
        df_pivot = pandas.pivot_table(df, values='duration', index=['author_name', 'project'], columns='start_date', aggfunc=numpy.sum)
    else:
        df_pivot = df.pivot_table(values='duration', index=['author_name'], columns='start_date', aggfunc=numpy.sum)

    df_pivot = df_pivot/3600
    df_pivot['Всего за период'] = df_pivot.sum(axis=1)
    df_pivot = df_pivot.sort_index(axis=1)
    df_pivot.index.names = ['Сотрудник', 'Проект']
    report_name = generate_report_name('users')
    df_pivot.to_excel(f'static/{report_name}', index=True, float_format='%.2f')
    return f'http://127.0.0.1:80/static/{report_name}'

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

def generate_report_name(name: str) -> str:
    datepart = datetime.now().strftime('%Y%m%d%H%M%S%f')
    return f'report-{name}-{datepart}.xlsx'

