# Python Utility library

## Introduction

The library provides a useful set of utility functions frequently used when creating Python components for Keboola Connection. The utility library should be used in cooperation with the main [Python Component](https://github.com/keboola/python-component) library.

The Python Utility library is developed the Keboola Data Services team and is officially supported by Keboola. The library aims to ease the component creation process by removing the necessity to write frequently used functions all over again.

## Links

- API Documentation: [API Docs](https://github.com/keboola/python-utils/blob/main)
- Source code: [https://github.com/keboola/python-utils](https://github.com/keboola/python-utils)
- PYPI project code: [link](link)
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

### DateUtils

The class contains all date related functions, which can be utilized to effective work with dates, when creating components for Keboola Connection.

#### Initialization

No input parameters are required to utilize the `DateUtils` class.

The class can be imported and initialized using:

```python
from keboola.utils import DateUtils

dutils = DateUtils()
```

#### Getting converted date period from string

The function `get_date_period_converted()` allows to parse any string containing date format into a Python datetime; or if `strformat` parameter is specified, into a datetime formatted string.

```python
from keboola.utils import DateUtils

dutils = DateUtils()

dt_str_1 = '5 days ago'
dt_str_2 = 'today'
dt_format = '%Y-%m-%d'

start_date, end_date = dutils.get_date_period_converted(dt_str_1, dt_str_2, dt_format)
```

#### Generating date period chunks

The function `split_dates_to_chunks()` allows to split time interval into chunks of specified size.

```python
from keboola.utils import DateUtils
from datetime import date

dutils = DateUtils()
dt_1 = date(2021, 1, 1)
dt_2 = date(2021, 1, 10)
dt_format = '%Y-%m-%d'

intervals = dutils.split_dates_to_chunks(dt_1, dt_2, intv=2, strformat=dt_format)

for intv in intervals:
    print(intv['start_date'], intv['end_date'])
```

#### Usage Example

```python
from keboola.utils import DateUtils

dutils = DateUtils()

dt_str_1 = '5 days ago'
dt_str_2 = 'today'
dt_format = '%Y-%m-%d'

start_date, end_date = dutils.get_date_period_converted(dt_str_1, dt_str_2)

intervals = dutils.split_dates_to_chunks(start_date, end_date, intv=2, strformat=dt_format)

for intv in intervals:
    print(intv['start_date'], intv['end_date'])
```