from datetime import date
from working_calendar import WorkingCalendar


def clear_working_calendar(working_calendar):
    working_calendar.clear_working_days()  # no additional working days
    working_calendar.clear_holidays()  # no holidays
    working_calendar.clear_not_standard_working_days()  # no not standard working days
    working_calendar.clear_weekends()  # no weekends
    working_calendar.update_working_time_minutes(480)  # 8 hours * 60 minutes


def test_add_working_day(working_calendar):
    clear_working_calendar(working_calendar)

    test_date = date(2018, 3, 1)

    assert len(working_calendar.get_working_days()) == 0

    working_calendar.add_working_day(test_date)
    assert len(working_calendar.get_working_days()) == 1
    assert test_date in working_calendar.get_working_days()


def test_add_holiday(working_calendar):
    clear_working_calendar(working_calendar)

    test_date = date(2018, 3, 1)

    assert len(working_calendar.get_holidays()) == 0

    working_calendar.add_holiday(test_date)
    assert len(working_calendar.get_holidays()) == 1
    assert test_date in working_calendar.get_holidays()


def test_update_not_standard_working_day(working_calendar):
    clear_working_calendar(working_calendar)

    test_date1 = date(2018, 3, 1)
    test_date2 = date(2018, 3, 2)

    try:
        working_calendar.update_not_standard_working_day(test_date1, -1)
    except ValueError:
        pass
    else:
        raise AssertionError

    try:
        working_calendar.update_not_standard_working_day(test_date1, 0)
    except ValueError:
        pass
    else:
        raise AssertionError

    try:
        working_calendar.update_not_standard_working_day(test_date1, '123')
    except ValueError:
        pass
    else:
        raise AssertionError

    assert len(working_calendar.get_not_standard_working_days()) == 0

    working_calendar.update_not_standard_working_day(test_date1, 1)
    assert len(working_calendar.get_not_standard_working_days()) == 1
    assert test_date1 in working_calendar.get_not_standard_working_days()

    working_calendar.update_not_standard_working_day(date(2018, 3, 2), 1)
    assert len(working_calendar.get_not_standard_working_days()) == 2
    assert test_date2 in working_calendar.get_not_standard_working_days()


def test_update_working_time_minutes(working_calendar):
    clear_working_calendar(working_calendar)

    assert working_calendar.get_working_time_minutes() == 480

    try:
        working_calendar.update_working_time_minutes(-1)
    except ValueError:
        pass
    else:
        raise AssertionError

    try:
        working_calendar.update_working_time_minutes(0)
    except ValueError:
        pass
    else:
        raise AssertionError

    try:
        working_calendar.update_working_time_minutes(1441)
    except ValueError:
        pass
    else:
        raise AssertionError

    try:
        working_calendar.update_working_time_minutes('123')
    except ValueError:
        pass
    else:
        raise AssertionError

    working_calendar.update_working_time_minutes(1)
    assert working_calendar.get_working_time_minutes() == 1


def test_is_additional_working_day(working_calendar):
    clear_working_calendar(working_calendar)

    test_date = date(2018, 3, 1)

    assert not working_calendar.is_additional_working_day(test_date)

    working_calendar.add_working_day(test_date)
    assert working_calendar.is_additional_working_day(test_date)


def test_is_holiday(working_calendar):
    clear_working_calendar(working_calendar)

    test_date = date(2018, 3, 1)

    assert not working_calendar.is_holiday(test_date)

    working_calendar.add_holiday(test_date)
    assert working_calendar.is_holiday(test_date)


def test_is_not_standard_working_day(working_calendar):
    clear_working_calendar(working_calendar)

    test_date = date(2018, 3, 1)

    assert not working_calendar.is_not_standard_working_day(test_date)

    working_calendar.update_not_standard_working_day(test_date, 1)
    assert working_calendar.is_not_standard_working_day(test_date)


def test_is_weekend(working_calendar):
    clear_working_calendar(working_calendar)

    test_date = date(2018, 3, 1)

    assert not working_calendar.is_weekend(test_date)

    working_calendar.add_weekend(4)
    assert working_calendar.is_weekend(test_date)


def test_is_working(working_calendar):
    clear_working_calendar(working_calendar)

    test_date = date(2018, 3, 1)

    assert working_calendar.is_working(test_date)

    working_calendar.add_weekend(4)
    assert not working_calendar.is_working(test_date)
    working_calendar.clear_weekends()

    working_calendar.add_holiday(test_date)
    assert not working_calendar.is_working(test_date)
    working_calendar.clear_holidays()

    working_calendar.add_weekend(4)
    working_calendar.add_holiday(test_date)
    working_calendar.add_working_day(test_date)
    assert working_calendar.is_working(test_date)


def test_count_working_days_between(working_calendar):
    clear_working_calendar(working_calendar)

    weekends = [6, 7]
    holidays = [
        date(2018, 3, 8),
        date(2018, 3, 9),
    ]
    additional_working_days = [
        date(2018, 3, 8),
        date(2018, 3, 10),
    ]

    start_date = date(2018, 3, 1)
    end_date = date(2018, 3, 12)

    assert working_calendar.count_working_days_between(start_date, end_date) == 12

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_days_between(start_date, end_date) == 8
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_days_between(start_date, end_date) == 10
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_days_between(start_date, end_date) == 6

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_days_between(start_date, end_date) == 8


def test_count_working_days_in_year(working_calendar):
    clear_working_calendar(working_calendar)

    weekends = [6, 7]
    holidays = [
        date(2018, 2, 23),
        date(2020, 2, 23),
    ]
    additional_working_days = [
        date(2018, 2, 23),
        date(2020, 2, 23),
        date(2018, 2, 3),
        date(2020, 2, 1),
    ]

    year1 = 2018
    year2 = 2020

    assert working_calendar.count_working_days_in_year(year1) == 365
    assert working_calendar.count_working_days_in_year(year2) == 366

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_days_in_year(year1) == 261
    assert working_calendar.count_working_days_in_year(year2) == 262
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_days_in_year(year1) == 364
    assert working_calendar.count_working_days_in_year(year2) == 365
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_days_in_year(year1) == 260
    assert working_calendar.count_working_days_in_year(year2) == 262

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_days_in_year(year1) == 262
    assert working_calendar.count_working_days_in_year(year2) == 264


def test_count_working_days_in_month(working_calendar):
    clear_working_calendar(working_calendar)

    weekends = [6, 7]
    holidays = [
        date(2018, 2, 23),
        date(2020, 2, 23),
    ]
    additional_working_days = [
        date(2018, 2, 23),
        date(2020, 2, 23),
        date(2018, 2, 3),
        date(2020, 2, 1),
    ]

    year1 = 2018
    year2 = 2020
    month = 2

    assert working_calendar.count_working_days_in_month(year1, month) == 28
    assert working_calendar.count_working_days_in_month(year2, month) == 29

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_days_in_month(year1, month) == 20
    assert working_calendar.count_working_days_in_month(year2, month) == 20
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_days_in_month(year1, month) == 27
    assert working_calendar.count_working_days_in_month(year2, month) == 28
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_days_in_month(year1, month) == 19
    assert working_calendar.count_working_days_in_month(year2, month) == 20

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_days_in_month(year1, month) == 21
    assert working_calendar.count_working_days_in_month(year2, month) == 22


def test_count_working_minutes_between(working_calendar):
    clear_working_calendar(working_calendar)

    weekends = [6, 7]
    holidays = [
        date(2018, 3, 8),
        date(2018, 3, 9),
    ]
    additional_working_days = [
        date(2018, 3, 8),
        date(2018, 3, 10),
    ]
    working_minutes = 100

    start_date = date(2018, 3, 1)
    end_date = date(2018, 3, 12)

    assert working_calendar.count_working_minutes_between(start_date, end_date) == 12 * 480

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_minutes_between(start_date, end_date) == 8 * 480
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_minutes_between(start_date, end_date) == 10 * 480
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_minutes_between(start_date, end_date) == 6 * 480

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_minutes_between(start_date, end_date) == 8 * 480

    clear_working_calendar(working_calendar)

    working_calendar.update_working_time_minutes(working_minutes)

    assert working_calendar.count_working_minutes_between(start_date, end_date) == 12 * 100

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_minutes_between(start_date, end_date) == 8 * 100
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_minutes_between(start_date, end_date) == 10 * 100
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_minutes_between(start_date, end_date) == 6 * 100

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_minutes_between(start_date, end_date) == 8 * 100


def test_count_working_minutes_in_year(working_calendar):
    clear_working_calendar(working_calendar)

    weekends = [6, 7]
    holidays = [
        date(2018, 2, 23),
        date(2020, 2, 23),
    ]
    additional_working_days = [
        date(2018, 2, 23),
        date(2020, 2, 23),
        date(2018, 2, 3),
        date(2020, 2, 1),
    ]

    working_minutes = 100
    year1 = 2018
    year2 = 2020

    assert working_calendar.count_working_minutes_in_year(year1) == 365 * 480
    assert working_calendar.count_working_minutes_in_year(year2) == 366 * 480

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_minutes_in_year(year1) == 261 * 480
    assert working_calendar.count_working_minutes_in_year(year2) == 262 * 480
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_minutes_in_year(year1) == 364 * 480
    assert working_calendar.count_working_minutes_in_year(year2) == 365 * 480
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_minutes_in_year(year1) == 260 * 480
    assert working_calendar.count_working_minutes_in_year(year2) == 262 * 480

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_minutes_in_year(year1) == 262 * 480
    assert working_calendar.count_working_minutes_in_year(year2) == 264 * 480

    clear_working_calendar(working_calendar)

    working_calendar.update_working_time_minutes(working_minutes)

    assert working_calendar.count_working_minutes_in_year(year1) == 365 * 100
    assert working_calendar.count_working_minutes_in_year(year2) == 366 * 100

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_minutes_in_year(year1) == 261 * 100
    assert working_calendar.count_working_minutes_in_year(year2) == 262 * 100
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_minutes_in_year(year1) == 364 * 100
    assert working_calendar.count_working_minutes_in_year(year2) == 365 * 100
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_minutes_in_year(year1) == 260 * 100
    assert working_calendar.count_working_minutes_in_year(year2) == 262 * 100

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_minutes_in_year(year1) == 262 * 100
    assert working_calendar.count_working_minutes_in_year(year2) == 264 * 100


def test_count_working_minutes_in_month(working_calendar):
    clear_working_calendar(working_calendar)

    weekends = [6, 7]
    holidays = [
        date(2018, 2, 23),
        date(2020, 2, 23),
    ]
    additional_working_days = [
        date(2018, 2, 23),
        date(2020, 2, 23),
        date(2018, 2, 3),
        date(2020, 2, 1),
    ]

    working_minutes = 100
    year1 = 2018
    year2 = 2020
    month = 2

    assert working_calendar.count_working_minutes_in_month(year1, month) == 28 * 480
    assert working_calendar.count_working_minutes_in_month(year2, month) == 29 * 480

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_minutes_in_month(year1, month) == 20 * 480
    assert working_calendar.count_working_minutes_in_month(year2, month) == 20 * 480
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_minutes_in_month(year1, month) == 27 * 480
    assert working_calendar.count_working_minutes_in_month(year2, month) == 28 * 480
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_minutes_in_month(year1, month) == 19 * 480
    assert working_calendar.count_working_minutes_in_month(year2, month) == 20 * 480

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_minutes_in_month(year1, month) == 21 * 480
    assert working_calendar.count_working_minutes_in_month(year2, month) == 22 * 480

    clear_working_calendar(working_calendar)

    working_calendar.update_working_time_minutes(working_minutes)

    assert working_calendar.count_working_minutes_in_month(year1, month) == 28 * 100
    assert working_calendar.count_working_minutes_in_month(year2, month) == 29 * 100

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_minutes_in_month(year1, month) == 20 * 100
    assert working_calendar.count_working_minutes_in_month(year2, month) == 20 * 100
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_minutes_in_month(year1, month) == 27 * 100
    assert working_calendar.count_working_minutes_in_month(year2, month) == 28 * 100
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_minutes_in_month(year1, month) == 19 * 100
    assert working_calendar.count_working_minutes_in_month(year2, month) == 20 * 100

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_minutes_in_month(year1, month) == 21 * 100
    assert working_calendar.count_working_minutes_in_month(year2, month) == 22 * 100


def test_count_working_hours_between(working_calendar):
    clear_working_calendar(working_calendar)

    weekends = [6, 7]
    holidays = [
        date(2018, 3, 8),
        date(2018, 3, 9),
    ]
    additional_working_days = [
        date(2018, 3, 8),
        date(2018, 3, 10),
    ]
    working_minutes = 100

    start_date = date(2018, 3, 1)
    end_date = date(2018, 3, 12)

    assert working_calendar.count_working_hours_between(start_date, end_date) == 12 * 480 / 60

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_hours_between(start_date, end_date) == 8 * 480 / 60
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_hours_between(start_date, end_date) == 10 * 480 / 60
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_hours_between(start_date, end_date) == 6 * 480 / 60

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_hours_between(start_date, end_date) == 8 * 480 / 60

    clear_working_calendar(working_calendar)

    working_calendar.update_working_time_minutes(working_minutes)

    assert working_calendar.count_working_hours_between(start_date, end_date) == 12 * 100 / 60

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_hours_between(start_date, end_date) == 8 * 100 / 60
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_hours_between(start_date, end_date) == 10 * 100 / 60
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_hours_between(start_date, end_date) == 6 * 100 / 60

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_hours_between(start_date, end_date) == 8 * 100 / 60


def test_count_working_hours_in_year(working_calendar):
    clear_working_calendar(working_calendar)

    weekends = [6, 7]
    holidays = [
        date(2018, 2, 23),
        date(2020, 2, 23),
    ]
    additional_working_days = [
        date(2018, 2, 23),
        date(2020, 2, 23),
        date(2018, 2, 3),
        date(2020, 2, 1),
    ]

    working_minutes = 100
    year1 = 2018
    year2 = 2020

    assert working_calendar.count_working_hours_in_year(year1) == 365 * 480 / 60
    assert working_calendar.count_working_hours_in_year(year2) == 366 * 480 / 60

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_hours_in_year(year1) == 261 * 480 / 60
    assert working_calendar.count_working_hours_in_year(year2) == 262 * 480 / 60
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_hours_in_year(year1) == 364 * 480 / 60
    assert working_calendar.count_working_hours_in_year(year2) == 365 * 480 / 60
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_hours_in_year(year1) == 260 * 480 / 60
    assert working_calendar.count_working_hours_in_year(year2) == 262 * 480 / 60

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_hours_in_year(year1) == 262 * 480 / 60
    assert working_calendar.count_working_hours_in_year(year2) == 264 * 480 / 60

    clear_working_calendar(working_calendar)

    working_calendar.update_working_time_minutes(working_minutes)

    assert working_calendar.count_working_hours_in_year(year1) == 365 * 100 / 60
    assert working_calendar.count_working_hours_in_year(year2) == 366 * 100 / 60

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_hours_in_year(year1) == 261 * 100 / 60
    assert working_calendar.count_working_hours_in_year(year2) == 262 * 100 / 60
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_hours_in_year(year1) == 364 * 100 / 60
    assert working_calendar.count_working_hours_in_year(year2) == 365 * 100 / 60
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_hours_in_year(year1) == 260 * 100 / 60
    assert working_calendar.count_working_hours_in_year(year2) == 262 * 100 / 60

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_hours_in_year(year1) == 262 * 100 / 60
    assert working_calendar.count_working_hours_in_year(year2) == 264 * 100 / 60


def test_count_working_hours_in_month(working_calendar):
    clear_working_calendar(working_calendar)

    weekends = [6, 7]
    holidays = [
        date(2018, 2, 23),
        date(2020, 2, 23),
    ]
    additional_working_days = [
        date(2018, 2, 23),
        date(2020, 2, 23),
        date(2018, 2, 3),
        date(2020, 2, 1),
    ]

    working_minutes = 100
    year1 = 2018
    year2 = 2020
    month = 2

    assert working_calendar.count_working_hours_in_month(year1, month) == 28 * 480 / 60
    assert working_calendar.count_working_hours_in_month(year2, month) == 29 * 480 / 60

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_hours_in_month(year1, month) == 20 * 480 / 60
    assert working_calendar.count_working_hours_in_month(year2, month) == 20 * 480 / 60
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_hours_in_month(year1, month) == 27 * 480 / 60
    assert working_calendar.count_working_hours_in_month(year2, month) == 28 * 480 / 60
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_hours_in_month(year1, month) == 19 * 480 / 60
    assert working_calendar.count_working_hours_in_month(year2, month) == 20 * 480 / 60

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_hours_in_month(year1, month) == 21 * 480 / 60
    assert working_calendar.count_working_hours_in_month(year2, month) == 22 * 480 / 60

    clear_working_calendar(working_calendar)

    working_calendar.update_working_time_minutes(working_minutes)

    assert working_calendar.count_working_hours_in_month(year1, month) == 28 * 100 / 60
    assert working_calendar.count_working_hours_in_month(year2, month) == 29 * 100 / 60

    working_calendar.extend_weekends(weekends)
    assert working_calendar.count_working_hours_in_month(year1, month) == 20 * 100 / 60
    assert working_calendar.count_working_hours_in_month(year2, month) == 20 * 100 / 60
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_hours_in_month(year1, month) == 27 * 100 / 60
    assert working_calendar.count_working_hours_in_month(year2, month) == 28 * 100 / 60
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.count_working_hours_in_month(year1, month) == 19 * 100 / 60
    assert working_calendar.count_working_hours_in_month(year2, month) == 20 * 100 / 60

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.count_working_hours_in_month(year1, month) == 21 * 100 / 60
    assert working_calendar.count_working_hours_in_month(year2, month) == 22 * 100 / 60


def test_get_next_working_day(working_calendar):
    clear_working_calendar(working_calendar)

    weekends = [6, 7]
    holidays = [
        date(2018, 3, 8),
        date(2018, 3, 9),
    ]
    additional_working_days = [
        date(2018, 3, 8),
        date(2018, 3, 10),
    ]

    assert working_calendar.get_next_working_day(date(2018, 3, 1)) == date(2018, 3, 2)
    assert working_calendar.get_next_working_day(date(2018, 3, 2)) == date(2018, 3, 3)
    assert working_calendar.get_next_working_day(date(2018, 3, 3)) == date(2018, 3, 4)
    assert working_calendar.get_next_working_day(date(2018, 3, 7)) == date(2018, 3, 8)
    assert working_calendar.get_next_working_day(date(2018, 3, 8)) == date(2018, 3, 9)

    working_calendar.extend_weekends(weekends)
    assert working_calendar.get_next_working_day(date(2018, 3, 1)) == date(2018, 3, 2)
    assert working_calendar.get_next_working_day(date(2018, 3, 2)) == date(2018, 3, 5)
    assert working_calendar.get_next_working_day(date(2018, 3, 3)) == date(2018, 3, 5)
    assert working_calendar.get_next_working_day(date(2018, 3, 7)) == date(2018, 3, 8)
    assert working_calendar.get_next_working_day(date(2018, 3, 8)) == date(2018, 3, 9)
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.get_next_working_day(date(2018, 3, 1)) == date(2018, 3, 2)
    assert working_calendar.get_next_working_day(date(2018, 3, 2)) == date(2018, 3, 3)
    assert working_calendar.get_next_working_day(date(2018, 3, 3)) == date(2018, 3, 4)
    assert working_calendar.get_next_working_day(date(2018, 3, 7)) == date(2018, 3, 10)
    assert working_calendar.get_next_working_day(date(2018, 3, 8)) == date(2018, 3, 10)
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.get_next_working_day(date(2018, 3, 1)) == date(2018, 3, 2)
    assert working_calendar.get_next_working_day(date(2018, 3, 2)) == date(2018, 3, 5)
    assert working_calendar.get_next_working_day(date(2018, 3, 3)) == date(2018, 3, 5)
    assert working_calendar.get_next_working_day(date(2018, 3, 7)) == date(2018, 3, 12)
    assert working_calendar.get_next_working_day(date(2018, 3, 8)) == date(2018, 3, 12)

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.get_next_working_day(date(2018, 3, 1)) == date(2018, 3, 2)
    assert working_calendar.get_next_working_day(date(2018, 3, 2)) == date(2018, 3, 5)
    assert working_calendar.get_next_working_day(date(2018, 3, 3)) == date(2018, 3, 5)
    assert working_calendar.get_next_working_day(date(2018, 3, 7)) == date(2018, 3, 8)
    assert working_calendar.get_next_working_day(date(2018, 3, 8)) == date(2018, 3, 10)


def test_skip_working_days(working_calendar):
    clear_working_calendar(working_calendar)

    weekends = [6, 7]
    holidays = [
        date(2018, 3, 8),
        date(2018, 3, 9),
    ]
    additional_working_days = [
        date(2018, 3, 8),
        date(2018, 3, 10),
    ]

    try:
        assert working_calendar.skip_working_days(date(2018, 3, 1), -1)
    except ValueError:
        pass
    else:
        raise AssertionError

    try:
        assert working_calendar.skip_working_days(date(2018, 3, 1), 0)
    except ValueError:
        pass
    else:
        raise AssertionError

    try:
        assert working_calendar.skip_working_days(date(2018, 3, 1), '123')
    except ValueError:
        pass
    else:
        raise AssertionError

    assert working_calendar.skip_working_days(date(2018, 3, 1), 1) == date(2018, 3, 2)
    assert working_calendar.skip_working_days(date(2018, 3, 3), 1) == date(2018, 3, 4)
    assert working_calendar.skip_working_days(date(2018, 3, 7), 1) == date(2018, 3, 8)
    assert working_calendar.skip_working_days(date(2018, 3, 8), 1) == date(2018, 3, 9)
    assert working_calendar.skip_working_days(date(2018, 3, 1), 2) == date(2018, 3, 3)
    assert working_calendar.skip_working_days(date(2018, 3, 3), 2) == date(2018, 3, 5)
    assert working_calendar.skip_working_days(date(2018, 3, 7), 2) == date(2018, 3, 9)
    assert working_calendar.skip_working_days(date(2018, 3, 8), 2) == date(2018, 3, 10)

    working_calendar.extend_weekends(weekends)
    assert working_calendar.skip_working_days(date(2018, 3, 1), 1) == date(2018, 3, 2)
    assert working_calendar.skip_working_days(date(2018, 3, 3), 1) == date(2018, 3, 6)
    assert working_calendar.skip_working_days(date(2018, 3, 7), 1) == date(2018, 3, 8)
    assert working_calendar.skip_working_days(date(2018, 3, 8), 1) == date(2018, 3, 9)
    assert working_calendar.skip_working_days(date(2018, 3, 1), 2) == date(2018, 3, 3)
    assert working_calendar.skip_working_days(date(2018, 3, 3), 2) == date(2018, 3, 7)
    assert working_calendar.skip_working_days(date(2018, 3, 7), 2) == date(2018, 3, 9)
    assert working_calendar.skip_working_days(date(2018, 3, 8), 2) == date(2018, 3, 10)
    working_calendar.clear_weekends()

    working_calendar.extend_holidays(holidays)
    assert working_calendar.skip_working_days(date(2018, 3, 1), 1) == date(2018, 3, 2)
    assert working_calendar.skip_working_days(date(2018, 3, 3), 1) == date(2018, 3, 4)
    assert working_calendar.skip_working_days(date(2018, 3, 7), 1) == date(2018, 3, 8)
    assert working_calendar.skip_working_days(date(2018, 3, 8), 1) == date(2018, 3, 11)
    assert working_calendar.skip_working_days(date(2018, 3, 1), 2) == date(2018, 3, 3)
    assert working_calendar.skip_working_days(date(2018, 3, 3), 2) == date(2018, 3, 5)
    assert working_calendar.skip_working_days(date(2018, 3, 7), 2) == date(2018, 3, 11)
    assert working_calendar.skip_working_days(date(2018, 3, 8), 2) == date(2018, 3, 12)
    working_calendar.clear_holidays()

    working_calendar.extend_weekends(weekends)
    working_calendar.extend_holidays(holidays)
    assert working_calendar.skip_working_days(date(2018, 3, 1), 1) == date(2018, 3, 2)
    assert working_calendar.skip_working_days(date(2018, 3, 3), 1) == date(2018, 3, 6)
    assert working_calendar.skip_working_days(date(2018, 3, 7), 1) == date(2018, 3, 8)
    assert working_calendar.skip_working_days(date(2018, 3, 8), 1) == date(2018, 3, 13)
    assert working_calendar.skip_working_days(date(2018, 3, 1), 2) == date(2018, 3, 3)
    assert working_calendar.skip_working_days(date(2018, 3, 3), 2) == date(2018, 3, 7)
    assert working_calendar.skip_working_days(date(2018, 3, 7), 2) == date(2018, 3, 13)
    assert working_calendar.skip_working_days(date(2018, 3, 8), 2) == date(2018, 3, 14)

    working_calendar.extend_working_days(additional_working_days)
    assert working_calendar.skip_working_days(date(2018, 3, 1), 1) == date(2018, 3, 2)
    assert working_calendar.skip_working_days(date(2018, 3, 3), 1) == date(2018, 3, 6)
    assert working_calendar.skip_working_days(date(2018, 3, 7), 1) == date(2018, 3, 8)
    assert working_calendar.skip_working_days(date(2018, 3, 8), 1) == date(2018, 3, 9)
    assert working_calendar.skip_working_days(date(2018, 3, 1), 2) == date(2018, 3, 3)
    assert working_calendar.skip_working_days(date(2018, 3, 3), 2) == date(2018, 3, 7)
    assert working_calendar.skip_working_days(date(2018, 3, 7), 2) == date(2018, 3, 9)
    assert working_calendar.skip_working_days(date(2018, 3, 8), 2) == date(2018, 3, 11)


if __name__ == '__main__':
    wc = WorkingCalendar()

    test_add_working_day(wc)
    test_add_holiday(wc)
    test_update_not_standard_working_day(wc)
    test_update_working_time_minutes(wc)
    test_is_additional_working_day(wc)
    test_is_holiday(wc)
    test_is_not_standard_working_day(wc)
    test_is_working(wc)
    test_count_working_days_between(wc)
    test_count_working_days_in_year(wc)
    test_count_working_days_in_month(wc)
    test_get_next_working_day(wc)
    test_skip_working_days(wc)
    test_count_working_minutes_between(wc)
    test_count_working_minutes_in_year(wc)
    test_count_working_minutes_in_month(wc)
    test_count_working_hours_between(wc)
    test_count_working_hours_in_year(wc)
    test_count_working_hours_in_month(wc)
