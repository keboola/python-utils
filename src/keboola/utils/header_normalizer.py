"""
This module provides different strategies to normalize CSV column names
to a format supported by the [Keboola Connection Storage](https://help.keboola.com/):

`Only alphanumeric characters and underscores are allowed in column name.
Underscore is not allowed on the beginning.`

"""

import re
import string
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple, Union

from .char_encoder import CharEncoder, SupportedEncoder

PERMITTED_CHARS = string.digits + string.ascii_letters + '_'

DEFAULT_WHITESPACE_SUB = "_"
DEFAULT_NON_PERMITTED_SUB = ""
DEFAULT_ENCODE_DELIM = "_"
DEFAULT_ENCODER = SupportedEncoder.unicode


class HeaderNormalizer(ABC):
    """
    Abstract class for column normalization.

    """

    def __init__(self, permitted_chars: str = PERMITTED_CHARS, whitespace_sub: str = DEFAULT_WHITESPACE_SUB):
        """

        Args:
            permitted_chars: all characters that are permitted to be in a column concatenated together in one string
            whitespace_sub: character to substitute a whitespace
        """

        self.permitted_chars = permitted_chars
        self.whitespace_sub = whitespace_sub
        self._check_chars_permitted(self.whitespace_sub)

    @abstractmethod
    def _normalize_column_name(self, column_name: str):
        pass

    def _check_chars_permitted(self, in_string: str):
        """
        Checks whether characters of a string are within a permitted characters string

        Args:
            in_string: Input string

        Returns:

        Raises:
            ValueError
                If string contains characters that are not permitted

        """

        for char in in_string:
            if char not in self.permitted_chars:
                raise ValueError(f"Substitute: '{in_string}' not in permitted characters")

    def _replace_whitespace(self, in_string: str) -> str:
        """
        Replaces whitespaces with a substitute character
        Args:
            in_string:

        Returns:
            in_string : str
                A string with replaced whitespaces by a substitute character

        """
        in_string = self.whitespace_sub.join(in_string.split())
        return in_string

    def normalize_header(self, header: List[str]) -> List[str]:
        """
        Normalizes a list of columns to match the Keboola Connection Storage requirements:

        `Only alphanumeric characters and underscores are allowed in column name.
         Underscore is not allowed on the beginning.`

        It also checks for empty headers and adds a name to them so they do not remain empty

        Args:
            header:

        Returns:
            Normalized column.

        """

        normalized_header = []
        empty_column_id = 1

        for column in header:
            column = self._normalize_column_name(column)
            column, empty_column_id = self._check_empty_column(column, empty_column_id)
            normalized_header.append(column)
        return normalized_header

    @staticmethod
    def _check_empty_column(column: str, empty_column_id: int) -> Tuple[str, int]:
        """
        Checks if header is empty and fills it in

        Headers are checked if the string is empty, and if it is a new name is given.
        If the header contains more than 0 characters it will be returned.
        Each new name is appended a number, this number is increased and return as well if the
        header is empty.

        Args:
            column:
            empty_column_id: An integer contaning a number to be appended to the new name of an empty header

        Returns:
            column (str): The new name of an empty column
            empty_header_id (int) : An integer holding the id of the next empty column string

        """

        if not column:
            column = f"empty_{str(empty_column_id)}"
            empty_column_id += 1
        return column, empty_column_id


class DefaultHeaderNormalizer(HeaderNormalizer):
    """
        A class used to normalize headers using a substitute character
    """

    def __init__(self, permitted_chars: str = PERMITTED_CHARS, forbidden_sub: str = DEFAULT_NON_PERMITTED_SUB,
                 whitespace_sub: str = DEFAULT_WHITESPACE_SUB):
        """

        Args:
            permitted_chars: all characters that are permitted to be in a column concatenated together in one string
            forbidden_sub: substitute character for a forbidden character
            whitespace_sub: character to substitute a whitespace
        """

        super().__init__(permitted_chars=permitted_chars, whitespace_sub=whitespace_sub)

        self._check_chars_permitted(forbidden_sub)
        self.forbidden_sub = forbidden_sub

    def _normalize_column_name(self, header: str) -> str:
        header = self._replace_whitespace(header)
        header = self._replace_forbidden(header)
        return header

    def _replace_forbidden(self, in_string: str) -> str:
        """
        Replaces forbidden characters in a string by a substitute character

        Args:
            in_string:
        Returns:
            str - fixed name

        """

        in_string = re.sub("[^" + self.permitted_chars + "]", self.forbidden_sub, in_string)
        return in_string


class EncoderHeaderNormalizer(HeaderNormalizer):
    """
    Normalize headers by encoding character in utf8 or unicode. This enables unique mapping back
    to the original values. e.g. `a#` -> `a_35_`


    """

    def __init__(self, char_encoder: Union[SupportedEncoder, str] = DEFAULT_ENCODER,
                 encode_delimiter: str = DEFAULT_ENCODE_DELIM,
                 permitted_chars: str = PERMITTED_CHARS, whitespace_sub: str = DEFAULT_WHITESPACE_SUB):
        """

        Args:
            permitted_chars:
            char_encoder: type of encoder to be used for encoding forbidden characters
            encode_delimiter : str - character to put before and after an encoded character
            whitespace_sub : str - character to substitute a whitespace
        """

        super().__init__(permitted_chars=permitted_chars, whitespace_sub=whitespace_sub)

        self.encode_delimiter = encode_delimiter
        self.char_encoder = CharEncoder(char_encoder)

    def _normalize_column_name(self, column_name: str) -> str:

        new_column_name = self._replace_whitespace(column_name)
        new_column_name = self._encode_non_permitted_chars(new_column_name)
        return new_column_name

    def _encode_non_permitted_chars(self, in_string: str) -> str:

        column_characters = list(in_string)
        for i, char in enumerate(column_characters):
            if char not in self.permitted_chars:
                column_characters[i] = self.encode_delimiter + str(
                    self.char_encoder.encode_char(char)) + self.encode_delimiter
        return "".join(column_characters)


class DictHeaderNormalizer(HeaderNormalizer):
    """"
        A class used to normalize headers using a dictionary to replace characters.
     e.g. `{"#":"hsh"}`
    """

    def __init__(self, replace_dict: dict, permitted_chars: str = PERMITTED_CHARS,
                 whitespace_sub: str = DEFAULT_WHITESPACE_SUB):
        """

        Args:
            replace_dict: The dictionary contains a key representing the character to be replaced and a value which
                is used to replace the key character.
            permitted_chars:
            whitespace_sub:
        """

        super().__init__(permitted_chars=permitted_chars, whitespace_sub=whitespace_sub)

        self.replace_dict = replace_dict
        self._check_dict_permitted(replace_dict)

    def _normalize_column_name(self, column_name: str) -> str:

        new_column_name = self._replace_chars_using_dict(column_name, self.replace_dict)
        return new_column_name

    @staticmethod
    def _replace_chars_using_dict(in_string: str, replace_dict: dict) -> str:
        """
        Replaces characters in a string using a dictionary

        Args:
            in_string : str
                A string containing characters to be replaced using a dictionary
            replace_dict : dict
                A dictionary where keys are characters to be substituted by their specific values

        Returns:

        """

        for key in replace_dict:
            in_string = in_string.replace(key, replace_dict[key])
        return in_string

    def _check_dict_permitted(self, in_dict: dict):
        """
        Checks whether characters of strings in a dictionary are within a permitted characters string

        """
        for key in in_dict:
            self._check_chars_permitted(in_dict[key])


class NormalizerStrategy(Enum):
    """"
        Enumerator for column normalization strategies

        ...

        NormalizerStrategy
        ----------
        DEFAULT :
            Normalize headers using a substitute character
        ENCODER :
            Normalize headers using a character encoder
        DICT :
            Normalize headers using a dictionary to replace characters
        """
    DEFAULT = "DEFAULT"
    ENCODER = "ENCODER"
    DICT = "DICT"


def get_normalizer(strategy: NormalizerStrategy, **params) -> HeaderNormalizer:
    """

    Factory method to initialize a column normalizer with various strategies:

        DEFAULT :
            Normalize headers using a substitute character

        ENCODER :
            Normalize headers by encoding character in utf8 or unicode. This enables unique mapping back
             to the original values. e.g. `a#` -> `a_35_`

                 params:
                    `char_encoder: SupportedEncoder = DEFAULT_ENCODER, encode_delimiter: str = DEFAULT_ENCODE_DELIM`
        DICT :
            Specify a dictionary with character replacements. e.g. {"#":"hsh"}

                params:
                `replace_dict`
    Args:
        strategy:
        **params:

    Returns: HeaderNormalizer

    """

    if strategy == NormalizerStrategy.DEFAULT:
        return DefaultHeaderNormalizer(**params)

    elif strategy == NormalizerStrategy.ENCODER:
        return EncoderHeaderNormalizer(**params)

    elif strategy == NormalizerStrategy.DICT:
        return DictHeaderNormalizer(**params)
    else:
        raise ValueError(f"Strategy '{strategy}' is not supported")
