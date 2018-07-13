import datetime

from typing import (
    Dict,
    Iterable,
    Optional,
    Union
)

from .enumerations import (
    Months,
    DaysOfWeek
)
from .exceptions import (
    NotDateException,
    NotDayOfWeekException,
    StartGreaterEndException
)


class WorkingCalendar(object):
    """
    Utility for operates with working days.

    _working_days — set of additional working days (even for holiday or weekend) (datetime.date).
    _holidays — set of holidays (datetime.date).
    _not_standard_working_days — dictionary (key is working day (datetime.date) and value is working time minutes).
    _weekends — what days of week are weekends (int).
    _working_time_minutes — working minutes of normal working day
    """

    def __init__(
        self,
        weekends=None,  # type: Optional[Iterable[Union[DaysOfWeek, int]]]
        working_time_minutes=480  # type: Optional[int]
    ):
        """
        :param weekends: days of the week
        :type weekends: Optional[Iterable[Union[DaysOfWeek, int]]]

        :param working_time_minutes: working time for one working day in minutes, default: 8 * 60
        :type working_time_minutes: int
        """

        self._working_days = set()
        self._holidays = set()
        self._weekends = set()
        self._not_standard_working_days = dict()

        if weekends is None:
            self._weekends.add(DaysOfWeek.SATURDAY)
            self._weekends.add(DaysOfWeek.SUNDAY)
        else:
            self.extend_weekends(weekends)

        self._working_time_minutes = 0
        self.update_working_time_minutes(working_time_minutes)

    @staticmethod
    def _check_date(
        date  # type: datetime.date
    ):
        # type: (...) -> datetime.date

        """
        Check value and convert it if needed.

        :param date: int, datetime.date, datetime.datetime or any else representation of date
        :type date: datetime.date

        :return: converted date
        :rtype: datetime.date
        """

        if isinstance(date, int):
            date = datetime.date.fromordinal(date)

        if isinstance(date, datetime.datetime):
            date = date.date()

        if isinstance(date, datetime.date):
            return date

        raise NotDateException(date.__class__.__name__)

    @staticmethod
    def _check_day_of_week(
        day,  # type: Union[DaysOfWeek, int]
    ):
        # type: (...) -> DaysOfWeek

        """
        Check value and convert it to DaysOfWeek if needed.

        :param day: day of the week
        :type day: Union[DaysOfWeek, int]

        :return: day of the week
        :rtype: DaysOfWeek
        """

        if isinstance(day, int):
            return DaysOfWeek(day)

        if isinstance(day, DaysOfWeek):
            return day

        raise NotDayOfWeekException

    def add_holiday(
        self,
        date,  # type: datetime.date
    ):
        """
        Add date to set of holidays.

        :param date: date for adding
        :type date: datetime.date
        """

        self._holidays.add(self._check_date(date))

    def add_weekend(
        self,
        weekend,  # type: Union[DaysOfWeek, int]
    ):
        """
        Add day of the week to set of weekends.

        :param weekend: day of the week
        :type weekend: Union[DaysOfWeek, int]
        """

        self._weekends.add(self._check_day_of_week(weekend))

    def add_working_day(
        self,
        date,  # type: datetime.date
    ):
        """
        Add date to set of additional working days.

        :param date: date for adding
        :type date: datetime.date
        """

        self._working_days.add(self._check_date(date))

    def clear_holidays(self):
        """
        Clear set of holidays.
        """

        self._holidays.clear()

    def clear_not_standard_working_days(self):
        """
        Clear dictionary of not standard working days.
        """

        self._not_standard_working_days.clear()

    def clear_weekends(self):
        """
        Clear set of weekends.
        """

        self._weekends.clear()

    def clear_working_days(self):
        """
        Clear set of additional working days.
        """

        self._working_days.clear()

    def extend_holidays(
        self,
        dates,  # type: Iterable[datetime.date]
    ):
        """
        Extend set of holidays with new dates.

        :param dates: new dates for adding
        :type dates: Iterable[datetime.date]
        """

        for date in dates:
            self.add_holiday(date)

    def extend_weekends(
        self,
        weekends,  # type: Iterable[Union[DaysOfWeek, int]]
    ):
        """
        Extend set of weekends with new weekends.

        :param weekends: new weekends for adding
        :type weekends: Iterable[Union[DaysOfWeek, int]]
        """

        for weekend in weekends:
            self.add_weekend(weekend)

    def extend_working_days(
        self,
        dates,  # type: Iterable[datetime.date]
    ):
        """
        Extend set of additional working days with new dates.

        :param dates: new dates for adding
        :type dates: Iterable[datetime.date]
        """

        for date in dates:
            self.add_working_day(date)

    def get_holidays(self):
        # type: (...) -> set

        """
        Return set of holidays.

        :return: set of holidays
        :rtype: set
        """

        return self._holidays

    def get_not_standard_working_days(self):
        # type: (...) -> Dict[datetime.date: int]

        """
        Return dictionary of not standard working days.

        :return: dictionary of not standard working days
        :rtype: Dict[datetime.date: int]
        """

        return self._not_standard_working_days

    def get_working_days(self):
        # type: (...) -> set

        """
        Return set of additional working days.

        :return: set of additional working days
        :rtype: set
        """

        return self._working_days

    def get_working_time_minutes(self):
        # type: (...) -> int

        """
        Return sum of minutes of working time in working day.

        :return: minutes
        :rtype: int
        """

        return self._working_time_minutes

    def remove_holiday(
        self,
        date,  # type: datetime.date
    ):
        """
        Remove date from set of holidays.

        :param date: date for removing
        :type date: datetime.date
        """

        self._holidays.remove(self._check_date(date))

    def remove_not_standard_working_day(
        self,
        date,  # type: datetime.date
    ):
        """
        Remove date from dictionary of not standard working days.

        :param date: date for removing
        :type date: datetime.date
        """

        self._not_standard_working_days.pop(self._check_date(date), None)

    def remove_weekend(
        self,
        weekend,  # type: Union[DaysOfWeek, int]
    ):
        """
        Remove weekend from set of weekends.

        :param weekend: weekend for removing
        :type weekend: Union[DaysOfWeek, int]
        """

        self._weekends.remove(self._check_day_of_week(weekend))

    def remove_working_day(
        self,
        date,  # type: datetime.date
    ):
        """
        Remove date from set of additional working days.

        :param date: date for removing
        :type date: datetime.date
        """

        self._working_days.remove(self._check_date(date))

    def update_not_standard_working_day(
        self,
        date,  # type: datetime.date,
        working_time_minutes,  # type: int
    ):
        """
        Update dictionary of not standard working days.

        :param date: date for updating
        :type date: datetime.date

        :param working_time_minutes: number of working minutes of the working day
        :type working_time_minutes: int
        """

        if not (
            isinstance(working_time_minutes, int) and
            working_time_minutes > 0
        ):
            raise ValueError('Argument \'working_time_minutes\' must be integer greater than 0.')

        self._not_standard_working_days[self._check_date(date)] = working_time_minutes

    def update_working_time_minutes(
        self,
        minutes,  # type: int
    ):
        """
        Update working time in normal working day.

        :param minutes: minutes of the working time in normal working day
        :type minutes: int
        """

        if not (
            isinstance(minutes, int) and
            0 < minutes < 1441
        ):
            raise ValueError('Argument \'minutes\' must be integer in range [1; 1440].')

        self._working_time_minutes = minutes

    def is_additional_working_day(
        self,
        date,  # type: datetime.date
    ):
        # type: (...) -> bool

        """
        Checking if date is additional working day.

        :param date: date for checking
        :type date: datetime.date

        :return: result of checking
        :rtype: bool
        """

        return self._check_date(date) in self._working_days

    def is_holiday(
        self,
        date,  # type: datetime.date
    ):
        # type: (...) -> bool

        """
        Checking if date is holiday.

        :param date: date for checking
        :type date: datetime.date

        :return: result of checking
        :rtype: bool
        """

        return self._check_date(date) in self._holidays

    def is_not_standard_working_day(
        self,
        date,  # type: datetime.date
    ):
        # type: (...) -> bool

        """
        Checking if date is not standard working day.

        :param date: date for checking
        :type date: datetime.date

        :return: result of checking
        :rtype: bool
        """

        return self._check_date(date) in self._not_standard_working_days

    def is_weekend(
        self,
        date,  # type: datetime.date
    ):
        # type: (...) -> bool

        """
        Checking if date is weekend.

        :param date: date for checking
        :type date: datetime.date

        :return: result of checking
        :rtype: bool
        """

        return DaysOfWeek(self._check_date(date).isoweekday()) in self._weekends

    def is_working(
        self,
        date,  # type: datetime.date
    ):
        # type: (...) -> bool

        """
        Checking if date is working day.

        :param date: date for checking
        :type date: datetime.date

        :return: result of checking
        :rtype: bool
        """

        date = self._check_date(date)

        if self.is_additional_working_day(date):
            return True

        if self.is_holiday(date):
            return False

        return not self.is_weekend(date)

    def count_working_days_between(
        self,
        start_date,  # type: datetime.date
        end_date,  # type: datetime.date
    ):
        # type: (...) -> int

        """
        Count working days between 2 dates.

        :param start_date: date for start
        :type start_date: datetime.date

        :param end_date: date for end
        :type end_date: datetime.date

        :return: counter of working days
        :rtype: int
        """

        start_date = self._check_date(start_date)
        end_date = self._check_date(end_date)

        if start_date > end_date:
            raise StartGreaterEndException

        delta = (end_date - start_date).days
        date = start_date
        counter = 1 if self.is_working(date) else 0

        for day in range(delta):
            date += datetime.timedelta(days=1)

            if self.is_working(date):
                counter += 1

        return counter

    def count_working_days_in_month(
        self,
        year,  # type: int
        month,  # type: int
    ):
        # type: (...) -> int

        """
        Count working days in month.

        :param year: year
        :type year: int

        :param month: month
        :type month: int

        :return: counter of working days
        :rtype: int
        """

        return self.count_working_days_between(
            datetime.date(year, month, 1),
            datetime.date(year, month, Months.get_by_ordinal(month).get_max_days(year))
        )

    def count_working_days_in_year(
        self,
        year,  # type: int
    ):
        # type: (...) -> int

        """
        Count working days in year.

        :param year: year
        :type year: int

        :return: counter of working days
        :rtype: int
        """

        return self.count_working_days_between(
            datetime.date(year, 1, 1),
            datetime.date(year, 12, Months.get_by_ordinal(12).get_max_days(year))
        )

    def count_working_minutes_between(
        self,
        start_date,  # type: datetime.date
        end_date,  # type: datetime.date
    ):
        # type: (...) -> int

        """
        Sum of working minutes between 2 dates.

        :param start_date: date for start
        :type start_date: datetime.date

        :param end_date: date for end
        :type end_date: datetime.date

        :return: sum of working minutes
        :rtype: int
        """

        start_date = self._check_date(start_date)
        end_date = self._check_date(end_date)

        if start_date > end_date:
            raise StartGreaterEndException

        delta = (end_date - start_date).days
        date = start_date
        total = self._not_standard_working_days.get(date, self._working_time_minutes) if self.is_working(date) else 0

        for day in range(delta):
            date += datetime.timedelta(days=1)

            if self.is_working(date):
                total += self._not_standard_working_days.get(date, self._working_time_minutes)

        return total

    def count_working_minutes_in_year(
        self,
        year,  # type: int
    ):
        # type: (...) -> int

        """
        Sum of working minutes in year.

        :param year: year
        :type year: int

        :return: sum of working minutes
        :rtype: int
        """

        return self.count_working_minutes_between(
            datetime.date(year, 1, 1),
            datetime.date(year, 12, Months.get_by_ordinal(12).get_max_days(year))
        )

    def count_working_minutes_in_month(
        self,
        year,  # type: int
        month,  # type: int
    ):
        # type: (...) -> int

        """
        Sum of working minutes in month.

        :param year: year
        :type year: int

        :param month: month
        :type month: int

        :return: sum of working minutes
        :rtype: int
        """

        return self.count_working_minutes_between(
            datetime.date(year, month, 1),
            datetime.date(year, month, Months.get_by_ordinal(month).get_max_days(year))
        )

    def count_working_hours_between(
        self,
        start_date,  # type: datetime.date
        end_date,  # type: datetime.date
    ):
        # type: (...) -> int

        """
        Count working hours between 2 dates.

        :param start_date: date for start
        :type start_date: datetime.date

        :param end_date: date for end
        :type end_date: datetime.date

        :return: counter of working hours
        :rtype: float
        """

        return self.count_working_minutes_between(start_date, end_date) / 60

    def count_working_hours_in_year(
        self,
        year,  # type: int
    ):
        # type: (...) -> float

        """
        Sum of working hours in year.

        :param year: year
        :type year: int

        :return: sum of working hours
        :rtype: float
        """

        return self.count_working_minutes_in_year(year) / 60

    def count_working_hours_in_month(
        self,
        year,  # type: int
        month,  # type: int
    ):
        # type: (...) -> float

        """
        Sum of working hours in month.

        :param year: year
        :type year: int

        :param month: month
        :type month: int

        :return: sum of working hours
        :rtype: float
        """

        return self.count_working_minutes_in_month(year, month) / 60

    def get_next_working_day(
        self,
        date,  # type: datetime.date
    ):
        # type: (...) -> datetime.date

        """
        Return date of the next working day.

        :param date: date for start
        :type date: datetime.date

        :return: date of the next working day
        :rtype: datetime.date
        """

        date = self._check_date(date)

        while True:
            date += datetime.timedelta(days=1)

            if self.is_working(date):
                break

        return date

    def skip_working_days(
        self,
        date,  # type: datetime.date
        skip_days,  # type: int
    ):
        # type: (...) -> datetime.date

        """
        Return date after skipping from start date.

        :param date: date for start
        :type date: datetime.date

        :param skip_days: counter of working days for skipping
        :type skip_days: int

        :return: date after skipping
        :rtype: datetime.date
        """

        date = self._check_date(date)

        if not (
            isinstance(skip_days, int) and
            skip_days > 0
        ):
            raise ValueError('Argument \'skip_days\' must be integer greater than 0.')

        while skip_days > 0:
            if self.is_working(date):
                skip_days -= 1

            date += datetime.timedelta(days=1)

        return date
