import dateparser
import math
import pytz
from _datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Tuple, Generator, Union

date_tuple = Union[Tuple[datetime, datetime], Tuple[str, str]]
date_gen = Generator[dict[str, datetime], None, None]


class DateUtils:

    def __init__(self):
        pass

    def get_date_period_converted(self, period_from: str, period_to: str, strformat: str = None) -> date_tuple:
        """
        Returns given period parameters in datetime format, or next step in back-fill mode
        along with generated last state for next iteration.

        Args:
            period_from: YYYY-MM-DD or relative string supported by date parser e.g. 5 days ago
            period_to: YYYY-MM-DD or relative string supported by date parser e.g. 5 days ago
            strformat: A python strtime format, in which output dates will be returned. If not specified
                       function returns dates in datetime.datetime type

        Returns:
            start_date: datetime, end_date: datetime
        """

        start_date_form = dateparser.parse(period_from)
        end_date_form = dateparser.parse(period_to)
        day_diff = (end_date_form - start_date_form).days
        if day_diff < 0:
            raise ValueError("start_date cannot exceed end_date.")

        if strformat is None:
            return start_date_form, end_date_form
        else:
            return start_date_form.strftime(strformat), end_date_form.strftime(strformat)

    def get_backfill_period(self, period_from: str, period_to: str, last_state: dict) -> date_tuple:
        """
        Get backfill period, either specified period in datetime type or period based on a previous run (last_state)
        Continues iterating date periods based on the initial period size defined by from and to parameters.
        ex.:
        Run 1:
        _get_backfill_period("2018-01-01", "2018-01-03", None ) -> datetime("2018-01-01"),datetime("2018-01-03"),state)

        Run 2:
        _get_backfill_period("2018-01-01", "2018-01-03", last_state(from previous) )
                -> datetime("2018-01-03"), datetime("2018-01-05"), state)

        etc...

        :type last_state: dict
        - None or state file produced by backfill mode
        e.g. {"last_period" : {
                                "start_date": "2018-01-01",
                                "end_date": "2018-01-02"
                                }
            }

        Args:
            period_to: YYYY-MM-DD format or relative string supported by date parser e.g. 5 days ago
            period_from: YYYY-MM-DD format or relative string supported by date parser e.g. 5 days ago
            last_state: A dictionary containing last saved state or None
                        e.g. {
                              "last_period" : {
                              "start_date": "2018-01-01",
                              "end_date": "2018-01-02"
                            }
                        }

        Returns:
            start_date: datetime, end_date: datetime, state_file: dict
        """
        if last_state and last_state.get('last_period'):
            last_start_date = datetime.strptime(last_state['last_period']['start_date'], '%Y-%m-%d')
            last_end_date = datetime.strptime(last_state['last_period']['end_date'], '%Y-%m-%d')

            diff = last_end_date - last_start_date
            # if period is a single day
            if diff.days == 0:
                diff = timedelta(days=1)

            start_date = last_end_date
            if (last_end_date.date() + diff) >= datetime.now(pytz.utc).date() + timedelta(days=1):
                end_date = datetime.now(pytz.utc)
            else:
                end_date = last_end_date + diff
        else:
            start_date = dateparser.parse(period_from)
            end_date = dateparser.parse(period_to)
        return start_date, end_date

    def get_past_date(self, str_days_ago: str, to_date: datetime = None,
                      tz: pytz.tzinfo.BaseTzInfo = pytz.utc) -> object:
        """
        Returns date in specified timezone relative to to_date parameter.

        e.g.
        '5 hours ago',
        'yesterday',
        '3 days ago',
        '4 months ago',
        '2 years ago',
        'today'

        Args:
            str_days_ago: A string specifying some kind of date, in relative or absolute format
            to_date: A date, from which the relative date will be calculated. Default: today's date
            tz: A timezone specifier of type pytz.tzinfo.BaseTzInfo

        Returns:
            date: datetime
        """
        if to_date:
            TODAY = to_date
        else:
            TODAY = datetime.datetime.now(tz)

        try:
            today_diff = (datetime.datetime.now(tz) - TODAY).days
            past_date = dateparser.parse(str_days_ago)
            past_date.replace(tzinfo=tz)
            date = past_date - relativedelta(days=today_diff)
            return date
        except TypeError:
            raise ValueError(
                "Please enter valid date parameters. Some of the values (%s, %s)are not in supported format",
                str_days_ago)

    def split_dates_to_chunks(self, start_date: datetime, end_date: datetime, intv: int,
                              strformat: str = "%Y-%m-%d") -> list:
        """
        Splits dates in given period into chunks of specified max size.

        Args:
            start_date: Start date, from which periods will be calculated
            end_date: End date, to which periods will be calculated
            intv: Size of interval in days
            strformat: A strftime format string

        Returns:
            list

        Usage example:
        list(split_dates_to_chunks("2018-01-01", "2018-01-04", 2, "%Y-%m-%d"))

            returns [{start_date: "2018-01-01", "end_date":"2018-01-02"}
                     {start_date: "2018-01-02", "end_date":"2018-01-04"}]
        """
        return list(self._split_dates_to_chunks_gen(start_date, end_date, intv, strformat))

    def _split_dates_to_chunks_gen(self, start_date: datetime, end_date: datetime, intv: int,
                                   strformat: str = "%Y-%m-%d") -> date_gen:
        """
        Splits dates in given period into chunks of specified max size.

        Params:
        start_date -- start_period [datetime]
        end_date -- end_period [datetime]
        intv -- max chunk size
        strformat -- dateformat of result periods

        Usage example:
        list(split_dates_to_chunks("2018-01-01", "2018-01-04", 2, "%Y-%m-%d"))

            returns [{start_date: "2018-01-01", "end_date":"2018-01-02"}
                     {start_date: "2018-01-02", "end_date":"2018-01-04"}]
        """

        nr_days = (end_date - start_date).days

        if nr_days <= intv:
            yield {'start_date': start_date.strftime(strformat),
                   'end_date': end_date.strftime(strformat)}
        elif intv == 0:
            diff = timedelta(days=1)
            for i in range(nr_days):
                yield {'start_date': (start_date + diff * i).strftime(strformat),
                       'end_date': (start_date + diff * i).strftime(strformat)}
        else:
            nr_parts = math.ceil(nr_days / intv)
            diff = (end_date - start_date) / nr_parts
            for i in range(nr_parts):
                yield {'start_date': (start_date + diff * i).strftime(strformat),
                       'end_date': (start_date + diff * (i + 1)).strftime(strformat)}