import unittest
import keboola.utils.formatter as futils


class TestFormatterUtils(unittest.TestCase):
    def test_comma_separated_values_to_list(self):
        csv_string_1 = '1,2,3,4,5'
        csv_list_1 = futils.comma_separated_values_to_list(csv_string_1)
        self.assertEqual(csv_list_1, ['1', '2', '3', '4', '5'])
        csv_string_2 = 'name,age,email'
        csv_list_2 = futils.comma_separated_values_to_list(csv_string_2)
        self.assertEqual(csv_list_2, ['name', 'age', 'email'])
        csv_string_3 = 'asdh7,asdhj$#@,p_.sd,96,5'
        csv_list_3 = futils.comma_separated_values_to_list(csv_string_3)
        self.assertEqual(csv_list_3, ['asdh7', 'asdhj$#@', 'p_.sd', '96', '5'])

    def test_comma_separated_values_to_list_throws_type_error(self):
        with self.assertRaises(TypeError):
            futils.comma_separated_values_to_list(123)
