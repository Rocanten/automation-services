import isodate, re
from datetime import datetime, timedelta
from utils.datetime import iso_duration_to_work_seconds

class Timelog:
    def __init__(self, issue_key, comment,
                 author_id, created, start, duration):
        self.project = issue_key.split('-')[0]
        self.issue_key = issue_key
        self.comment = comment
        self.author_id = author_id
        self.created = isodate.parse_datetime(created)
        self.start = isodate.parse_datetime(start)
        self.total_seconds = iso_duration_to_work_seconds(duration, 8)

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
