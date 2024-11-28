import dateparser
import datetime
import types
import unittest
import pytz
from freezegun import freeze_time
import keboola.utils.date as dutils


class TestDateUtils(unittest.TestCase):

    def test_parse_datetime_interval_success(self):
        period_1 = '5 days ago'
        period_2 = 'yesterday'
        dt_format = '%Y-%m-%d'

        period_1_str = dateparser.parse(period_1).strftime(dt_format)
        period_2_str = dateparser.parse(period_2).strftime(dt_format)

        self.assertTupleEqual((period_1_str, period_2_str),
                              dutils.parse_datetime_interval(period_1, period_2, dt_format))

    @freeze_time("2021-11-11 10:00:00")
    def test_get_past_date(self):
        str_days_ago = '3 days ago'
        tz = pytz.timezone('Europe/Prague')
        to_date = datetime.datetime(2021, 3, 10, 10, 0, 0, tzinfo=tz)

        expected_result = datetime.datetime(2021, 3, 7, 10, 0, 0
                                            , tzinfo=tz).strftime('%Y-%m-%d')

        self.assertEqual(expected_result,
                         dutils.get_past_date(str_days_ago=str_days_ago, to_date=to_date, tz=tz).strftime('%Y-%m-%d'))

    @freeze_time("2021-11-11 10:00:00")
    def test_get_past_date_no_tz(self):
        str_days_ago = '3 days ago'
        tz = pytz.timezone('Europe/Prague')
        to_date = datetime.datetime(2021, 3, 10, 10, 0, 0, tzinfo=tz)

        expected_result = datetime.datetime(2021, 3, 7, 10, 0, 0
                                            , tzinfo=tz).strftime('%Y-%m-%d')

        self.assertEqual(expected_result,
                         dutils.get_past_date(str_days_ago=str_days_ago, to_date=to_date, tz=tz).strftime('%Y-%m-%d'))

    def test_parse_datetime_interval_fail(self):
        period_1 = '5 days ago'
        period_2 = 'yesterday'

        with self.assertRaises(ValueError, msg='start_date cannot exceed end_date.'):
            dutils.parse_datetime_interval(period_2, period_1)

    def test_split_dates_to_chunks_list_interval_0(self):
        expected_result = [
            {'start_date': '2021-01-01', 'end_date': '2021-01-01'},
            {'start_date': '2021-01-02', 'end_date': '2021-01-02'},
            {'start_date': '2021-01-03', 'end_date': '2021-01-03'},
            {'start_date': '2021-01-04', 'end_date': '2021-01-04'},
        ]

        dt_1 = datetime.datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        dt_2 = datetime.datetime(2021, 1, 5, 0, 0, 0, tzinfo=pytz.UTC)
        dt_f = '%Y-%m-%d'

        self.assertCountEqual(expected_result,
                              dutils.split_dates_to_chunks(dt_1, dt_2, 0, dt_f, generator=False))

    def test_split_dates_to_chunks_list_interval_lower_than_nr(self):
        expected_result = [
            {'start_date': '2021-01-01', 'end_date': '2021-01-02'},
            {'start_date': '2021-01-02', 'end_date': '2021-01-04'},
            {'start_date': '2021-01-04', 'end_date': '2021-01-06'},
        ]

        dt_1 = datetime.datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        dt_2 = datetime.datetime(2021, 1, 6, 0, 0, 0, tzinfo=pytz.UTC)
        dt_f = '%Y-%m-%d'

        self.assertCountEqual(expected_result,
                              dutils.split_dates_to_chunks(dt_1, dt_2, 2, dt_f, generator=False))

    def test_split_dates_to_chunks_list_interval_higher_than_nr(self):
        expected_result = [
            {'start_date': '2021-01-01', 'end_date': '2021-01-06'}
        ]

        dt_1 = datetime.datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        dt_2 = datetime.datetime(2021, 1, 6, 0, 0, 0, tzinfo=pytz.UTC)
        dt_f = '%Y-%m-%d'

        self.assertCountEqual(expected_result,
                              dutils.split_dates_to_chunks(dt_1, dt_2, 10, dt_f, generator=False))

    def test_split_dates_to_chunks_gen_interval_0(self):
        expected_result = [
            {'start_date': '2021-01-01', 'end_date': '2021-01-01'},
            {'start_date': '2021-01-02', 'end_date': '2021-01-02'},
            {'start_date': '2021-01-03', 'end_date': '2021-01-03'},
            {'start_date': '2021-01-04', 'end_date': '2021-01-04'},
        ]

        dt_1 = datetime.datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        dt_2 = datetime.datetime(2021, 1, 5, 0, 0, 0, tzinfo=pytz.UTC)
        dt_f = '%Y-%m-%d'

        date_gen = dutils.split_dates_to_chunks(dt_1, dt_2, 0, dt_f, generator=True)

        self.assertIsInstance(date_gen, types.GeneratorType)
        self.assertCountEqual(expected_result, list(date_gen))

    def test_split_dates_to_chunks_gen_interval_lower_than_nr(self):
        expected_result = [
            {'start_date': '2021-01-01', 'end_date': '2021-01-02'},
            {'start_date': '2021-01-02', 'end_date': '2021-01-04'},
            {'start_date': '2021-01-04', 'end_date': '2021-01-06'},
        ]

        dt_1 = datetime.datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        dt_2 = datetime.datetime(2021, 1, 6, 0, 0, 0, tzinfo=pytz.UTC)
        dt_f = '%Y-%m-%d'

        date_gen = dutils.split_dates_to_chunks(dt_1, dt_2, 2, dt_f, generator=True)

        self.assertIsInstance(date_gen, types.GeneratorType)
        self.assertCountEqual(expected_result, list(date_gen))

    def test_split_dates_to_chunks_gen_interval_higher_than_nr(self):
        expected_result = [
            {'start_date': '2021-01-01', 'end_date': '2021-01-06'}
        ]

        dt_1 = datetime.datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        dt_2 = datetime.datetime(2021, 1, 6, 0, 0, 0, tzinfo=pytz.UTC)
        dt_f = '%Y-%m-%d'

        date_gen = dutils.split_dates_to_chunks(dt_1, dt_2, 10, dt_f, generator=True)

        self.assertIsInstance(date_gen, types.GeneratorType)
        self.assertCountEqual(expected_result, list(date_gen))
