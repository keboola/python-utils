# Python Utility library

## Introduction

![Build & Test](https://github.com/keboola/python-utils/workflows/Build%20&%20Test/badge.svg?branch=main)
[![Code Climate](https://codeclimate.com/github/keboola/python-utils/badges/gpa.svg)](https://codeclimate.com/github/keboola/python-utils)

The library provides a useful set of utility functions frequently used when creating Python components for Keboola Connection. The utility library should be used in cooperation with the main [Python Component](https://github.com/keboola/python-component) library.

The Python Utility library is developed the Keboola Data Services team and is officially supported by Keboola. The library aims to ease the component creation process by removing the necessity to write frequently used functions all over again.

## Links

- API Documentation: [API Docs](https://htmlpreview.github.io/?https://raw.githubusercontent.com/keboola/python-utils/main/docs/api-html/utils/date.html)
- Source code: [https://github.com/keboola/python-utils](https://github.com/keboola/python-utils)
- PYPI project code: [https://pypi.org/project/keboola.utils](https://pypi.org/project/keboola.utils)
- Documentation: [https://developers.keboola.com/extend/component/python-component-library](https://developers.keboola.com/extend/component/python-component-library)

## Quick start

### Installation

The package can be installed via `pip` using:

```
pip install keboola.utils
```

### Structure and functionality

The package currently contains one core module:

- `keboola.utils.date` - a set of methods for date manipulation.

### Date Utilities

The module contains all date related functions, which can be utilized to effective work with dates, when creating components for Keboola Connection.

#### Initialization

All util functions can be imported from `keboola.utils` module.

```python
from keboola.utils import *
```

or 

```python
import keboola.utils.date
```

to import only functions from a certain module.

#### Getting converted date period from string

The function `parse_datetime_interval()` allows to parse any string containing date format into a Python datetime; or if `strformat` parameter is specified, into a datetime formatted string.

The positional arguments `period_from` and `period_to` can be specified in relative format (e.g. `3 days ago`, `2 months ago`, etc.) or in absolute format (e.g. `2020-01-01`). For full list of supported formats, please refer to [`dateparser` documentation](https://dateparser.readthedocs.io/en/latest/introduction.html#features).

```python
from keboola.utils import *

dt_str_1 = '5 days ago'
dt_str_2 = 'today'
dt_format = '%Y-%m-%d'

start_date, end_date = parse_datetime_interval(dt_str_1, dt_str_2, dt_format)
```

#### Generating date period chunks

The function `split_dates_to_chunks()` allows to split time interval into chunks of specified size.

```python
import keboola.utils.date as dutils
from datetime import date

dt_1 = date(2021, 1, 1)
dt_2 = date(2021, 1, 10)
dt_format = '%Y-%m-%d'

intervals = dutils.split_dates_to_chunks(dt_1, dt_2, intv=2, strformat=dt_format)

for intv in intervals:
    print(intv['start_date'], intv['end_date'])
```

#### Usage Example

```python
import keboola.utils.date as dutils

dt_str_1 = '5 days ago'
dt_str_2 = 'today'
dt_format = '%Y-%m-%d'

start_date, end_date = dutils.parse_datetime_interval(dt_str_1, dt_str_2)

intervals = dutils.split_dates_to_chunks(start_date, end_date, intv=2, strformat=dt_format)

for intv in intervals:
    print(intv['start_date'], intv['end_date'])
```