# Working Calendar

[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/igorxut/working-calendar/blob/master/LICENSE)
[![PyPi version](https://img.shields.io/pypi/v/working-calendar.svg)](https://test.pypi.org/project/working-calendar/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/working-calendar.svg)](https://pypi.python.org/pypi/working-calendar/)

## Description

Class `WorkingCalendar` is utility for operate with working days.

## Current version

0.0.1 (2018-07-13)

## Installation

```bash
pip install working_calendar
```

## Example

```python
from datetime import date
from working_calendar import WorkingCalendar


if __name__ == '__main__':
    wc = WorkingCalendar()

    holidays = [
        date(2018, 2, 23),
        date(2018, 3, 8),
        date(2018, 3, 9),
    ]
    additional_working_days = [
        date(2018, 3, 10),
    ]
    not_standard_working_day = (date(2018, 3, 10), 240)  # 240 min = 4 hours

    wc.extend_holidays(holidays)
    wc.extend_working_days(additional_working_days)
    wc.update_not_standard_working_day(not_standard_working_day[0], not_standard_working_day[1])

    print(wc.count_working_days_between(date(2018, 3, 1), date(2018, 3, 12)))  # 7 working days
    print(wc.count_working_days_in_year(2018))  # 259 working days
    print(wc.count_working_days_in_month(2018, 2))  # 19 working days

    print(wc.count_working_minutes_between(date(2018, 3, 1), date(2018, 3, 12)))  # 3120 minutes
    print(wc.count_working_minutes_in_year(2018))  # 124080 minutes
    print(wc.count_working_minutes_in_month(2018, 2))  # 9120 minutes

    print(wc.count_working_hours_between(date(2018, 3, 1), date(2018, 3, 12)))  # 52.0 hours
    print(wc.count_working_hours_in_year(2018))  # 2068.0 hours
    print(wc.count_working_hours_in_month(2018, 2))  # 152.0 hours

    print(wc.get_next_working_day(date(2018, 3, 7)))  # 2018-03-10
    print(wc.skip_working_days(date(2018, 3, 10), 10))  # 2018-03-23
```
