def command_time() -> str:
    return (f'*/time me week* - get logged time during current week\n' +
        f'*/time me lastweek* - get logged time during last week\n' +
        f'*/time me month* - get logged time during current month\n' +
        f'*/time me lastmonth* - get logged time during last month\n')

def command_report() -> str:
    return (f'*/report tracker <Project code> month* - get report for project for current month from Yandex Tracker\n' +
        f'*/report tracker <Project code> lastmonth* - get report for project for previous month from Yandex Tracker\n')