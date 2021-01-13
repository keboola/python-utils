import dateparser
import datetime
import unittest
import pytz

from src.keboola.utils.date import DateUtils


class TestDateUtils(unittest.TestCase):

    def test_get_date_period_converted_success(self):
        period_1 = '5 days ago'
        period_2 = 'yesterday'
        dt_format = '%Y-%m-%d'

        period_1_str = dateparser.parse(period_1).strftime(dt_format)
        period_2_str = dateparser.parse(period_2).strftime(dt_format)

        dutils = DateUtils()

        self.assertTupleEqual((period_1_str, period_2_str),
                              dutils.get_date_period_converted(period_1, period_2, dt_format))

    def test_get_date_period_converted_fail(self):
        period_1 = '5 days ago'
        period_2 = 'yesterday'

        dutils = DateUtils()

        with self.assertRaises(ValueError, msg='start_date cannot exceed end_date.'):
            dutils.get_date_period_converted(period_2, period_1)

    def test_split_dates_to_chunks_interval_0(self):
        dutils = DateUtils()
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
                              dutils.split_dates_to_chunks(dt_1, dt_2, 0, dt_f))

    def test_split_dates_to_chunks_interval_1(self):
        dutils = DateUtils()
        expected_result = [
            {'start_date': '2021-01-01', 'end_date': '2021-01-02'},
            {'start_date': '2021-01-02', 'end_date': '2021-01-04'},
            {'start_date': '2021-01-04', 'end_date': '2021-01-06'},
        ]

        dt_1 = datetime.datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        dt_2 = datetime.datetime(2021, 1, 6, 0, 0, 0, tzinfo=pytz.UTC)
        dt_f = '%Y-%m-%d'

        self.assertCountEqual(expected_result,
                              dutils.split_dates_to_chunks(dt_1, dt_2, 2, dt_f))

    def test_split_dates_to_chunks_interval_higher_than_nr(self):
        dutils = DateUtils()
        expected_result = [
            {'start_date': '2021-01-01', 'end_date': '2021-01-06'}
        ]

        dt_1 = datetime.datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        dt_2 = datetime.datetime(2021, 1, 6, 0, 0, 0, tzinfo=pytz.UTC)
        dt_f = '%Y-%m-%d'

        self.assertCountEqual(expected_result,
                              dutils.split_dates_to_chunks(dt_1, dt_2, 10, dt_f))


if __name__ == '__main__':
    unittest.main()
