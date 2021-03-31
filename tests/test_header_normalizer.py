import unittest
from src.keboola.utils.header_normalizer import HeaderNormalizer


class TestFormatterUtils(unittest.TestCase):
    def test_normalize_header_default(self):
        head_norm = HeaderNormalizer(strategy="DEFAULT")
        headers_1 = ["name", "age", "email"]
        norm_headers_1 = head_norm.normalize_headers(headers_1)
        self.assertEqual(norm_headers_1, ["name", "age", "email"])

        headers_2 = ["name_lastname", "ag e", "email@domain.com", "123"]
        norm_headers_2 = head_norm.normalize_headers(headers_2)
        self.assertEqual(norm_headers_2, ["name_lastname", "ag_e", "emaildomaincom", "123"])

        headers_3 = ["&*D", "#%^", "email@domain.com", "123"]
        norm_headers_3 = head_norm.normalize_headers(headers_3)
        self.assertEqual(norm_headers_3, ["D", "empty_header_1", "emaildomaincom", "123"])

    def test_normalize_header_special_replace_non_permitted(self):
        head_norm = HeaderNormalizer(strategy="DEFAULT", non_permitted_sub="_")
        headers_1 = ["name", "age", "email"]
        norm_headers_1 = head_norm.normalize_headers(headers_1)
        self.assertEqual(norm_headers_1, ["name", "age", "email"])

        headers_2 = ["name_lastname", "age", "email@domain.com", "123"]
        norm_headers_2 = head_norm.normalize_headers(headers_2)
        self.assertEqual(norm_headers_2, ["name_lastname", "age", "email_domain_com", "123"])

        headers_3 = ["&*D", "#%^", "email@domain.com", "123"]
        norm_headers_3 = head_norm.normalize_headers(headers_3)
        self.assertEqual(norm_headers_3, ["__D", "___", "email_domain_com", "123"])

    def test_sub_not_permitted_raises_exception(self):
        with self.assertRaises(ValueError):
            HeaderNormalizer(strategy="DEFAULT", non_permitted_sub="#")
        with self.assertRaises(ValueError):
            HeaderNormalizer(strategy="DEFAULT", whitespace_sub="#")
        with self.assertRaises(ValueError):
            HeaderNormalizer(strategy="DICT", replace_dict={"_": "#"})

    def test_replace_chars_using_dict(self):
        head_norm = HeaderNormalizer(strategy="DICT", replace_dict={"#": "_hsh_"})
        headers = ["#name", "ag#e", "email"]
        norm_headers = head_norm.normalize_headers(headers)
        self.assertEqual(norm_headers, ["_hsh_name", "ag_hsh_e", "email"])

    def test_replace_whitespace(self):
        head_norm = HeaderNormalizer(strategy="DEFAULT", whitespace_sub="_w_")
        headers = ["n ame", "ag\te", "ema \n il"]
        norm_headers = head_norm.normalize_headers(headers)
        self.assertEqual(norm_headers, ["n_w_ame", "ag_w_e", "ema_w_il"])

    def test_replace_not_permitted(self):
        head_norm = HeaderNormalizer(strategy="DEFAULT", permitted_chars="abcd#$_")
        headers = ["dactor#fd", "a*ruas$", "48DHBb#@"]
        norm_headers = head_norm.normalize_headers(headers)
        self.assertEqual(norm_headers, ['dac#d', 'aa$', 'b#'])

    def test_normalize_header_encoding(self):
        head_norm = HeaderNormalizer(strategy="ENCODER",non_permitted_encoder="unicode")
        headers = ["dactor#fd", "a*ruas$", "48DHBb#@"]
        norm_headers = head_norm.normalize_headers(headers)
        self.assertEqual(norm_headers, ['dactor_35_fd', 'a_42_ruas_36_', '48DHBb_35__64_'])
