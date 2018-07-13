from collections import namedtuple
from enum import Enum
from typing import (
    Optional,
    Tuple,
    Union
)


Month = namedtuple('Month', ['ordinal', 'max_days'])


class DaysOfWeek(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Months(Enum):
    JANUARY = Month(1, 31)
    FEBRUARY = Month(2, (28, 29))
    MARCH = Month(3, 31)
    APRIL = Month(4, 30)
    MAY = Month(5, 31)
    JUNE = Month(6, 30)
    JULY = Month(7, 31)
    AUGUST = Month(8, 31)
    SEPTEMBER = Month(9, 30)
    OCTOBER = Month(10, 31)
    NOVEMBER = Month(11, 30)
    DECEMBER = Month(12, 31)

    @property
    def _max_days(self):
        # type: (...) -> Union[int, Tuple[int]]

        """
        Get number of days in month.

        :return: number of days
        :rtype: Union[int, Tuple[int]]
        """

        return self.value.max_days

    @property
    def ordinal(self):
        # type: (...) -> int

        """
        Get ordinal of month.

        :return: ordinal of month
        :rtype: int
        """

        return self.value.ordinal

    @staticmethod
    def get_by_ordinal(
        ordinal  # type: int
    ):
        # type: (...) -> Optional[namedtuple]

        """
        Return object 'Month' by ordinal.

        :param ordinal: ordinal of month
        :type ordinal: int

        :return: object 'Month'
        :rtype: Optional[namedtuple]
        """

        if not isinstance(ordinal, int):
            raise ValueError('Ordinal must be integer.')

        for month in Months:
            if month.ordinal == ordinal:
                return month

        return None

    @staticmethod
    def is_leap(
        year  # type: int
    ):
        # type: (...) -> bool

        """
        Checking if year is leap.

        :param year: year
        :type year: int

        :return: result of checking
        :rtype: bool
        """

        if isinstance(year, int):
            return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

        raise ValueError('Year must be integer.')

    def get_max_days(
        self,
        year=None,  # type: Optional[int]
    ):
        # type: (...) -> int

        """
        Get number of days in month.

        :param year: year
        :type year: Optional[int]

        :return: number of days
        :rtype: int
        """

        max_days = self._max_days

        if self.name == 'FEBRUARY':
            if year is None:
                raise ValueError('Year is necessary for \'FEBRUARY\'.')

            return max_days[1] if self.is_leap(year) else max_days[0]

        return max_days
