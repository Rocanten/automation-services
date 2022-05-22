from app.timelog import get_logged_time


def test_sample():
    timelogs = get_logged_time("oleg@kingbird.ru", "week")
    print(f'timelogs: {timelogs}')
    assert True
