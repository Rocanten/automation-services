import isodate, re
from datetime import datetime, timedelta

class Timelog:
    def __init__(self, issue_key, comment,
                 author_id, created, start, duration):
        self.project = issue_key.split('-')[0]
        self.issue_key = issue_key
        self.comment = comment
        self.author_id = author_id
        self.created = isodate.parse_datetime(created)
        self.start = isodate.parse_datetime(start)
        weeks = 0
        weeks_list = re.findall(r"(\d+)W", duration)
        if weeks_list:
            weeks = int(weeks_list[0])
        days = 0
        days_list = re.findall(r"(\d+)D", duration)
        if days_list:
            days = int(days_list[0])
        minutes = 0
        minutes_list = re.findall(r"(\d+)M", duration)
        if minutes_list:
            minutes = int(minutes_list[0])
        hours = 0
        hours_list = re.findall(r"(\d+)H", duration)
        if hours_list:
            hours = int(hours_list[0])
        self.total_seconds = weeks*7*8*60*60 + days*8*60*60 + hours*60*60 + minutes*60
        print(f'total seconds: {self.total_seconds}')

    def __str__(self):
        return ('Timelog:\n' +
                f'Issue: {self.issue_key}\n' +
                f'Comment: {self.comment}\n' +
                f'Duration: {self.get_formated_duration()}')

    def get_formated_duration(self):
        hours = self.total_seconds % 60*60
        minutes = self.total_seconds%60 - hours*60
        seconds = self.total_seconds - hours*60*60
        return f'**Total(hours: {hours}, minutes: {minutes})**'
