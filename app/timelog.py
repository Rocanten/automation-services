from datetime import datetime, timedelta, date
import pytz, pandas, numpy, logging

from app.datasource import get_raw_logged_time_period
from app.models.timelog import Timelog
from app.models.day import Day
from utils.datetime import get_week_start, get_week_end, get_month_start, get_month_end

logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)

def get_logged_time(email: str, period: str) -> str:
    result = ''
    if period == 'week':
        result = get_week_time(email)
    elif period == 'lastweek':
        result = get_last_week_time(email)
    elif period == 'month':
        result = get_month_time(email)
    elif period == 'lastmonth':
        result = get_last_month_time(email)
    elif period == 'today':
        result = get_today_time(email)
    else:
        raise RuntimeError('Unknown period')
    return result

def get_day_project_message(project: str, seconds: int) -> str:
    hours = int(seconds // (60 * 60))
    minutes = int(seconds // 60 - hours * 60)
    return f'{project}(hours: {hours}, minutes:{minutes})'

def get_days_text_for_period(dataframe: pandas.DataFrame, period_start: date, period_end: date) -> str:
    current_day = period_start
    text = ''
    while current_day <= period_end:
        day_text = f'\n**{current_day.strftime("%A, %d %b %Y")}** \n'
        project_texts = []
        try:
            df_date = dataframe[dataframe['start_date'] == current_day]
        except Exception as e:
            raise RuntimeError(f"You haven't logged any time during this period")
        total_day_seconds = get_seconds_for_period(dataframe, current_day, current_day)
        df_date_grouped_by_project = df_date.groupby(by=['project']).sum().reset_index()
        project_texts = ([get_day_project_message(project, seconds) 
            for project, seconds 
            in zip(df_date_grouped_by_project['project'], df_date_grouped_by_project['duration'])])
        if len(project_texts) == 0:
            day_text += "No time logged"
        else:
            day_text += '\n'.join(project_texts)
        total_day_text = get_total_day_text(total_day_seconds)
        day_text += f'\n{total_day_text}\n'
        text += day_text
        current_day += timedelta(days=1)
    return text

def get_seconds_for_period(dataframe: pandas.DataFrame, period_start: date, period_end: date):
    total_seconds = 0
    try:
        df_date = dataframe[(dataframe['start_date'] >= period_start)&(dataframe['start_date'] <= period_end)]
        total_seconds = df_date['duration'].sum()
    except KeyError as error:
        logging.warning(f'No time logged in the period, error={error}')
    return total_seconds

def get_total_text(seconds: int) -> str:
    hours: int = int(seconds//(60*60))
    minutes: int = int(seconds//60 - hours*60)
    return f'Total(hours: {hours}, minutes: {minutes})'

def get_total_day_text(seconds: int) -> str:
    hours: int = int(seconds//(60*60))
    minutes: int = int(seconds//60 - hours*60)
    return f'Logged during day(hours: {hours}, minutes: {minutes})'

def get_week_time(email: str):
    result = ''
    now = datetime.now()
    week_start = get_week_start(now)
    week_end = get_week_end(now)
    timelogs_raw = get_raw_logged_time_period(email)
    df = pandas.DataFrame(timelogs_raw)
    total_seconds = get_seconds_for_period(df, week_start.date(), week_end.date())

    days_text = get_days_text_for_period(df, week_start.date(), week_end.date())
    total_text = get_total_text(total_seconds)

    result = f'{days_text}{total_text}'

    return result

def get_last_week_time(email: str) -> str:
    result = ''
    day_last_week = datetime.now() - timedelta(days=7)
    week_start = get_week_start(day_last_week)
    week_end = get_week_end(day_last_week)
    timelogs_raw = get_raw_logged_time_period(email)
    df = pandas.DataFrame(timelogs_raw)
    df.to_csv('static/timelogs.csv', index=True, float_format='%.2f')
    total_seconds = get_seconds_for_period(df, week_start.date(), week_end.date())

    days_text = get_days_text_for_period(df, week_start.date(), week_end.date())
    total_text = get_total_text(total_seconds)

    result = f'{days_text}{total_text}'

    return result

def get_month_time(email: str) -> str:
    result = ''
    now = datetime.now()
    month_start = get_month_start(now)
    month_end = get_month_end(now)
    timelogs_raw = get_raw_logged_time_period(email)
    df = pandas.DataFrame(timelogs_raw)
    total_seconds = get_seconds_for_period(df, month_start.date(), month_end.date())

    days_text = get_days_text_for_period(df, month_start.date(), month_end.date())
    total_text = get_total_text(total_seconds)

    result = f'{days_text}{total_text}'

    return result

def get_last_month_time(email: str) -> str:
    result = ''
    now = datetime.now()
    day_last_month = now - timedelta(days=now.day+5)
    month_start = get_month_start(day_last_month)
    month_end = get_month_end(day_last_month)
    timelogs_raw = get_raw_logged_time_period(email)
    df = pandas.DataFrame(timelogs_raw)
    df.to_csv('static/timelogs.csv', index=True, float_format='%.2f')
    total_seconds = get_seconds_for_period(df, month_start.date(), month_end.date())

    days_text = get_days_text_for_period(df, month_start.date(), month_end.date())
    total_text = get_total_text(total_seconds)

    result = f'{days_text}{total_text}'

    return result

def get_today_time(email: str) -> str:
    result = ''
    now = datetime.now()
    timelogs_raw = get_raw_logged_time_period(email)
    df = pandas.DataFrame(timelogs_raw)
    total_seconds = get_seconds_for_period(df, now.date(), now.date())

    days_text = get_days_text_for_period(df, now.date(), now.date())
    total_text = get_total_text(total_seconds)

    result = f'{days_text}{total_text}'

    return result
