from datetime import datetime, timedelta

class Day:
    def __init__(self, date: datetime):
        self.dayweek = date.strftime("%A")
        self.date = date
        self.total_seconds = 0
        self.projects = {}

    def add_time(self, project_key: str, seconds):
        self.total_seconds += seconds
        if project_key in self.projects:
            self.projects[project_key] ++ seconds
        else:
            self.projects[project_key] = seconds

    def get_duration_formated(self):
        hours = int(self.total_seconds // (60 * 60))
        minutes = int(self.total_seconds // 60 - hours * 60)
        return f'hours: {hours}, minutes: {minutes}\n'

    def __str__(self):
        project_lines = ''
        for key, value in self.projects.items():
            hours = int(value // (60 * 60))
            minutes = int(value // 60 - hours * 60)
            project_lines += f'{key}(hours: {hours}, minutes: {minutes})\n'
        return (f'{self.dayweek} {self.date.strftime("%m/%d/%Y")}\n' +
                f'{self.get_duration_formated()}\n' +
                project_lines +
                '----------------------------\n')
