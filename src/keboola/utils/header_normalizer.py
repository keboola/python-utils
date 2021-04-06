import string
import re
from keboola.utils.char_encoder import CharEncoder
from enum import Enum
from typing import List, Tuple

PERMITTED_CHARS = string.digits + string.ascii_letters + '_'
PERMITTED_CHARS_KEY = "permitted_chars"
WHITESPACE_SUB_KEY = "whitespace_sub"
NON_PERMITTED_SUB_KEY = "non_permitted_sub"
ENCODE_DELIM_KEY = "encode_delim"
ENCODER_KEY = "encoder"
REPLACE_DICT_KEY = "replace_dict"

DEFAULT_WHITESPACE_SUB = "_"
DEFAULT_NON_PERMITTED_SUB = ""
DEFAULT_ENCODE_DELIM = "_"
DEFAULT_ENCODER = "unicode"


class HeaderNormalizer:
    """
    A class used to normalize headers

    ...

    Attributes
    ----------
    permitted_chars : str
        all characters that are permitted to be in a header concatenated together in one string
    whitespace_sub : str
        character to substitute a whitespace
    """

    def __init__(self, **params):
        """
        Keyword Arguments
        ----------
        permitted_chars : str
            all characters that are permitted to be in a header concatenated together in one string
        whitespace_sub : str
            character to substitute a whitespace
        """
        self.permitted_chars = PERMITTED_CHARS
        if PERMITTED_CHARS_KEY in params:
            self.permitted_chars = params[PERMITTED_CHARS_KEY]

        self.whitespace_sub = DEFAULT_WHITESPACE_SUB
        if WHITESPACE_SUB_KEY in params:
            self.whitespace_sub = params[WHITESPACE_SUB_KEY]
        self.check_chars_permitted(self.whitespace_sub, self.permitted_chars)

    @staticmethod
    def check_chars_permitted(in_string: str, permitted_chars: str):
        """ Checks whether characters of a string are within a permitted characters string

            Parameters
            ----------
            in_string : str
                A string of characters to check
            permitted_chars : str
                A string of characters of permitted characters

            Raises
            -------
            ValueError
                If string contains characters that are not permitted
        """
        for char in in_string:
            if char not in permitted_chars:
                raise ValueError(f"Substitute: '{in_string}' not in permitted characters")

    @staticmethod
    def replace_whitespace(in_string: str, substitute: str) -> str:
        """Replaces whitespaces with a substitute character

            Parameters
            ----------
            in_string : str
                A string whose whitespaces should be replaced by a substitute character
            substitute : str
                A character to replace whitespaces

            Returns
            -------
            in_string : str
                A string with replaced whitespaces by a substitute character
        """
        in_string = substitute.join(in_string.split())
        return in_string

    def normalize_headers(self, header: List[str]) -> List[str]:
        """Normalizes a list of headers

        Function normalizes using the initialized normalizer function.
        It also checks for empty headers and adds a name to them so they do not remain empty

        Parameters
        ----------
        header : List[str]
            A list of headers

        Returns
        -------
        normalized_headers : List[str]
            A list of normalized headers
        """
        normalized_headers = []
        empty_header_id = 1

        for h in header:
            h = self.normalizer(h)
            h, empty_header_id = self._check_empty_header(h, empty_header_id)
            normalized_headers.append(h)
        return normalized_headers

    @staticmethod
    def _check_empty_header(header: str, empty_header_id: int) -> Tuple[str, int]:
        """Checks if header is empty and fills it in

        Headers are checked if the string is empty, and if it is a new name is given.
        If the header contains more than 0 characters it will be returned.
        Each new name is appended a number, this number is increased and return as well if the
        header is empty.

        Parameters
        ----------
        header : str
            A string containing a header
        empty_header_id : int
            An integer containg a number to be appended to the new name of an empty header

        Returns
        -------
        header : str
            The new name of an empty header
        empty_header_id : int
            An integer holding the id of the next empty header string
        """
        if not header:
            header = "empty_header_" + str(empty_header_id)
            empty_header_id += 1
        return header, empty_header_id


class DefaultHeaderNormalizer(HeaderNormalizer):
    """
    A class used to normalize headers using a substitute character

    ...

    Attributes
    ----------
    permitted_chars : str
        all characters that are permitted to be in a header concatenated together in one string
    non_permitted_sub : str
        substitute character for a non permitted character
    whitespace_sub : str
        character to substitute a whitespace
    """
    def __init__(self, **params):
        """
        Keyword Arguments
        ----------
        permitted_chars : str
            all characters that are permitted to be in a header concatenated together in one string
        non_permitted_sub : str
            substitute character for a non permitted character
        whitespace_sub : str
            character to substitute a whitespace
        """
        HeaderNormalizer.__init__(self, **params)

        self.non_permitted_sub = DEFAULT_NON_PERMITTED_SUB
        if NON_PERMITTED_SUB_KEY in params:
            self.check_chars_permitted(params[NON_PERMITTED_SUB_KEY], self.permitted_chars)
            self.non_permitted_sub = params[NON_PERMITTED_SUB_KEY]

        self.normalizer = self.normalize_header_with_sub

    def normalize_header_with_sub(self, header: str) -> str:
        """Normalizes a header using a substitute character

            Parameters
            ----------
            header : str
                A string containing a header

            Returns
            -------
            header : str
                A string containing the normalized header
        """
        header = self.replace_whitespace(header, self.whitespace_sub)
        header = self.replace_not_permitted(header, self.permitted_chars, self.non_permitted_sub)
        return header

    @staticmethod
    def replace_not_permitted(in_string: str, permitted_chars: str, substitute: str) -> str:
        """Replaces not permitted characters in a string with a substitute character

            Parameters
            ----------
            in_string : str
                A string in which not permitted characters should be replaced
            permitted_chars : str
                A string containing characters allowed in the output string
            substitute : str
                A character to replace not permitted characters

            Returns
            -------
            in_string : str
                A string with only permitted characters
        """
        in_string = re.sub("[^" + permitted_chars + "]", substitute, in_string)
        return in_string


class EncoderHeaderNormalizer(HeaderNormalizer):
    """
    A class used to normalize headers using a character encoder

    ...

    Attributes
    ----------
    permitted_chars : str
        all characters that are permitted to be in a header concatenated together in one string
    non_permitted_encoder : str
        type of encoding to be used for encoding non-permitted characters
    encode_delim : str
            character to put before and after an encoded character
    whitespace_sub : str
        character to substitute a whitespace
    """
    def __init__(self, **params):
        """
        Keyword Arguments
        ----------
        permitted_chars : str
            all characters that are permitted to be in a header concatenated together in one string
        non_permitted_encoder : str
            type of encoding to be used for encoding non-permitted characters
        encode_delim : str
            character to put before and after an encoded character
        whitespace_sub : str
            character to substitute a whitespace
        """
        HeaderNormalizer.__init__(self, **params)

        self.encode_delim = DEFAULT_ENCODE_DELIM
        if ENCODE_DELIM_KEY in params:
            self.check_chars_permitted(params[ENCODE_DELIM_KEY], self.permitted_chars)
            self.encode_delim = params[ENCODE_DELIM_KEY]
        self.encoder = DEFAULT_ENCODER
        if ENCODER_KEY in params:
            self.encoder = params[ENCODER_KEY]
        self.normalizer = self.normalize_header_with_encoder

    def normalize_header_with_encoder(self, header: str) -> str:
        """Normalizes a header using an encoder

            The encoded character is wrapped with a specific character.
            For example a unicoded # with a encode_delim _ will result in _35_

            Parameters
            ----------
            header : str
                A string containing a header

            Returns
            -------
            header : str
                A string containing the normalized header
        """
        char_encoder = CharEncoder(self.encoder)
        header = self.replace_whitespace(header, self.whitespace_sub)
        header = self.encode_non_permitted_chars(header, char_encoder, self.permitted_chars, self.encode_delim)
        return header

    @staticmethod
    def encode_non_permitted_chars(in_string: str, char_encoder: CharEncoder, permitted_chars: str,
                                   encode_delim: str) -> str:
        """Encodes not permitted characters in a string with an encoder

            Parameters
            ----------
            in_string : str
                A string in which not permitted characters should be encoded
            char_encoder : CharEncoder
                A function that encodes a string with an encoder
            permitted_chars : str
                A string containing characters allowed in the output string
            encode_delim : str
                A character to wrap the encoded character

            Returns
            -------
            in_string : str
                A string containing encoded not permitted characters
        """
        in_string = list(in_string)
        for i, char in enumerate(in_string):
            if char not in permitted_chars:
                in_string[i] = encode_delim + str(char_encoder.encode_char(char)) + encode_delim
        return "".join(in_string)


class DictHeaderNormalizer(HeaderNormalizer):
    """"
    A class used to normalize headers using a dictionary to replace characters

    ...

    Attributes
    ----------
    permitted_chars : str
        all characters that are permitted to be in a header concatenated together in one string
    whitespace_sub : str
        character to substitute a whitespace
    replace_dict : dict
        dictionary where keys are characters to be substituted by their specific values
    """
    def __init__(self, **params):
        """
        Keyword Arguments
        ----------
        permitted_chars : str
            all characters that are permitted to be in a header concatenated together in one string
        whitespace_sub : str
            character to substitute a whitespace
        replace_dict : dict
            dictionary where keys are characters to be substituted by their specific values
        """
        HeaderNormalizer.__init__(self, **params)

        self.check_dict_permitted(params[REPLACE_DICT_KEY], self.permitted_chars)
        self.replace_dict = params[REPLACE_DICT_KEY]
        self.normalizer = self.normalize_header_with_dict

    def normalize_header_with_dict(self, header: str) -> str:
        """Normalizes a header using a dictionary

            The dictionary contains a key representing the character to be replaced and a value which
            is used to replace the key character

            Parameters
            ----------
            header : str
                A string containing a header

            Returns
            -------
            header : str
                A string containing the normalized header
        """
        header = self.replace_chars_using_dict(header, self.replace_dict)
        header = self.replace_whitespace(header, self.whitespace_sub)
        return header

    @staticmethod
    def replace_chars_using_dict(in_string: str, replace_dict: dict) -> str:
        """Replaces characters in a string using a dictionary

            The dictionary contains a key representing the character to be replaced and a value which
            is used to replace the key character

            Parameters
            ----------
            in_string : str
                A string containing characters to be replaced using a dictionary
            replace_dict : dict
                A dictionary where keys are characters to be substituted by their specific values

            Returns
            -------
            in_string : str
                A string which has had characters replaced using a dictionary
        """
        for key in replace_dict:
            in_string = in_string.replace(key, replace_dict[key])
        return in_string

    def check_dict_permitted(self, in_dict: dict, permitted_chars: str):
        """ Checks whether characters of strings in a dictionary are within a permitted characters string

            Parameters
            ----------
            in_dict : dict
                A dictionary of strings to check

            permitted_chars : str
                A string of characters of permitted characters
        """
        for key in in_dict:
            self.check_chars_permitted(in_dict[key], permitted_chars)


class Strategies(Enum):
    """"
        Enumerator for header normalization strategies

        ...

        Strategies
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


def get_normalizer(strategy: Strategies, **params) -> HeaderNormalizer:
    """ Factory method to initialize a header normalizer with various strategies

        Parameters
        ----------
        strategy : Strategies
            A strategy type
    """
    if strategy == "DEFAULT":
        return DefaultHeaderNormalizer(**params)

    elif strategy == "ENCODER":
        return EncoderHeaderNormalizer(**params)

    elif strategy == "DICT":
        return DictHeaderNormalizer(**params)
    else:
        raise ValueError(f"Strategy '{strategy}' is not supported")
