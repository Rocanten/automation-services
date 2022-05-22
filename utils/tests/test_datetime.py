from datetime import datetime, timedelta, date

from utils.datetime import get_month_start, get_month_end


def test_month_start_is_correct():
	month_day = datetime(2022, 5, 22)
	month_start = get_month_start(month_day)
	month_start_correct = datetime(2022, 5, 1)
	assert month_start == month_start_correct

def test_month_end_is_correct():
	month_day = datetime(2020, 2, 5)
	month_end = get_month_end(month_day)
	month_end_correct = datetime(2020, 2, 29)
	assert month_end == month_end_correct