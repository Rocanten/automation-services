import isodate
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
        self.duration = isodate.parse_duration(duration)

    def __str__(self):
        return ('Timelog:\n' +
                f'Issue: {self.issue_key}\n' +
                f'Comment: {self.comment}\n' +
                f'Duration: {self.get_formated_duration()}')

    def get_formated_duration(self):
        total_seconds = self.duration.total_seconds()
        hours = total_seconds%(60*60)
        minutes = total_seconds%60 - hours*60
        seconds = total_seconds - hours*60*60
        return f'Total(hours: {hours}, minutes: {minutes})'
