import unittest
import keboola.utils.formatter as futils


class TestFormatterUtils(unittest.TestCase):
    def test_normalize_header(self):
        headers_1 = ["name", "age", "email"]
        norm_headers_1 = futils.normalize_header(headers_1)
        self.assertEqual(norm_headers_1, ["name", "age", "email"])

        headers_2 = ["name_lastname", "age", "email@domain.com", "123"]
        norm_headers_2 = futils.normalize_header(headers_2)
        self.assertEqual(norm_headers_2, ["name_lastname", "age", "emaildomaincom", "123"])

        headers_3 = ["&*D", "#%^", "email@domain.com", "123"]
        norm_headers_3 = futils.normalize_header(headers_3)
        self.assertEqual(norm_headers_3, ["D", "", "emaildomaincom", "123"])

        permitted_chars = "abcd"
        headers_4 = ["asdasfjsaifj", "acgdyescas", "ddopoiiasc"]
        norm_headers_4 = futils.normalize_header(headers_4, permitted_chars=permitted_chars)
        self.assertEqual(norm_headers_4, ['adaa', 'acdca', 'ddac'])

