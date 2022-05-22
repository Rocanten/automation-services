from datetime import datetime, timedelta, date
import pytz, re

def get_week_start(date: datetime) -> datetime:
	week_start = (date.replace(hour=0, minute=0, second=0, microsecond=0) - 
        timedelta(days=date.weekday()))
	return week_start

def get_week_end(date: datetime) -> datetime:
	week_start = get_week_start(date)
	week_end = week_start + timedelta(days = 7) - timedelta(seconds=1)
	return week_end

def get_month_start(date: datetime) -> datetime:
    month_start = date.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=date.day-1)
    return month_start

def get_month_end(date: datetime) -> datetime:
    next_month = date.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)

def iso_duration_to_work_seconds(iso_duration: str, work_hours_per_day: int) -> int:
    weeks = 0
    weeks_list = re.findall(r"(\d+)W", iso_duration)
    if weeks_list:
        weeks = int(weeks_list[0])
    days = 0
    days_list = re.findall(r"(\d+)D", iso_duration)
    if days_list:
        days = int(days_list[0])
    minutes = 0
    minutes_list = re.findall(r"(\d+)M", iso_duration)
    if minutes_list:
        minutes = int(minutes_list[0])
    hours = 0
    hours_list = re.findall(r"(\d+)H", iso_duration)
    if hours_list:
        hours = int(hours_list[0])
    total_seconds = weeks*7*work_hours_per_day*60*60 + days*work_hours_per_day*60*60 + hours*60*60 + minutes*60
    return total_seconds
