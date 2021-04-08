import unittest
from src.keboola.utils.char_encoder import CharEncoder


class TestFormatterUtils(unittest.TestCase):
    def test_unicode_encode_char(self):
        char_encoder = CharEncoder("unicode")
        encoded_char = char_encoder.encode_char("#")
        self.assertEqual(encoded_char, 35)

    def test_utf8_encode_char(self):
        char_encoder = CharEncoder("utf8")
        encoded_char = char_encoder.encode_char("š")
        self.assertEqual(encoded_char, b'\xc5\xa1')
