from datetime import datetime, timedelta, date
import pytz, re

def get_week_start(date: datetime) -> datetime:
	return date.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
		days=date.weekday()
	)

def get_week_end(date: datetime) -> datetime:
	week_start = get_week_start(date)
	return week_start + timedelta(days = 7) - timedelta(seconds=1)

def get_month_start(date: datetime) -> datetime:
	return date.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
		days=date.day - 1
	)

def get_month_end(date: datetime) -> datetime:
    next_month = date.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)

def iso_duration_to_work_seconds(iso_duration: str, work_hours_per_day: int) -> int:
	weeks = 0
	if weeks_list := re.findall(r"(\d+)W", iso_duration):
		weeks = int(weeks_list[0])
	days = 0
	if days_list := re.findall(r"(\d+)D", iso_duration):
		days = int(days_list[0])
	minutes = 0
	if minutes_list := re.findall(r"(\d+)M", iso_duration):
		minutes = int(minutes_list[0])
	hours = 0
	if hours_list := re.findall(r"(\d+)H", iso_duration):
		hours = int(hours_list[0])
	return (
		weeks * 7 * work_hours_per_day * 60 * 60
		+ days * work_hours_per_day * 60 * 60
		+ hours * 60 * 60
		+ minutes * 60
	)
