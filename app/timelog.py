from datetime import datetime, timedelta, date
import pytz


from app.yandex.tracker import get_logged_time_period
from app.models.timelog import Timelog
from app.models.day import Day

def get_logged_time(email: str, period: str) -> str:
    result = ''
    if period == 'week':
        week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=datetime.today().weekday())
        week_end = week_start + timedelta(days = 7) - timedelta(seconds=1)
        timelogs = get_logged_time_period(email, week_start, week_end)
        total_seconds = 0
        for timelog in timelogs:
            total_seconds += timelog.duration.total_seconds()
        print(total_seconds)
        hours: int = int(total_seconds//(60*60))
        minutes: int = int(total_seconds//60 - hours*60)
        seconds = total_seconds - hours*60*60

        days_text = ''
        
        for i in range(0,6):
           day_date = week_start + timedelta(days=i)
           day = Day(day_date)
           for timelog in timelogs:
               print(f'day_date: {day_date}')
               print(f'timelog.start: {timelog.start}')
               day_date = day_date.replace(tzinfo=pytz.UTC)
               timelog.start = timelog.start.replace(tzinfo=pytz.UTC)
               if day_date + timedelta(days=1) >= timelog.start > day_date:
                   day.add_time(timelog.project, timelog.duration.total_seconds())
           days_text += str(day)
        
        result = f'{days_text} Total(hours: {hours}, minutes: {minutes})'
    else:
        raise RuntimeError('Unknown period')
    return result
