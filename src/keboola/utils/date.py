import math
from _datetime import timedelta
from datetime import datetime
from typing import Tuple, Generator, Union, Dict, List

import dateparser
import pytz
from dateutil.relativedelta import relativedelta

date_tuple = Union[Tuple[datetime, datetime], Tuple[str, str]]
date_gen = Generator[Dict[str, datetime], None, None]
date_chunk = Union[date_gen, List]


def parse_datetime_interval(period_from: str, period_to: str, strformat: str = None) -> date_tuple:
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


def get_past_date(str_days_ago: str, to_date: datetime = None,
                  tz: pytz.tzinfo = pytz.utc) -> object:
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
        tz: A timezone specifier of type pytz.tzinfo

    Returns:
        date: datetime
    """

    today_date = datetime.now(tz)
    if not to_date:
        to_date = today_date

    # add timezone awareness to allow date subtraction
    to_date = add_timezone_info(to_date, tz)

    try:
        today_diff = (today_date - to_date).days
        past_date = dateparser.parse(str_days_ago)
        past_date = past_date.replace(tzinfo=tz)
        date = past_date - relativedelta(days=today_diff)
        return date
    except TypeError as e:
        raise ValueError(
            f"Please enter valid date parameters. Some of the values ({str_days_ago}, {str(to_date)}) are "
            f"not in supported format. Raised: {e}")


def add_timezone_info(to_date: datetime, tz: pytz.tzinfo = pytz.utc) -> datetime:
    """
    Add timezone info if not present. Useful when making sure the datetime instances are offset-aware to allow
    date subtracting.
    Args:
        to_date: datetime
        tz: timezone

    Returns: datetime object with updated timezone info

    """
    if to_date.tzinfo is None:
        to_date = to_date.replace(tzinfo=tz)

    return to_date


def split_dates_to_chunks(start_date: datetime, end_date: datetime, intv: int,
                          strformat: str = "%Y-%m-%d", generator: bool = False) -> date_chunk:
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

    def split_dates_to_chunks_gen(start_date, end_date, intv, strformat):

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

    _gen = split_dates_to_chunks_gen(start_date, end_date, intv, strformat)

    if generator is True:
        return _gen
    else:
        return list(_gen)
