"""
Get alphanumerical encoding of characters using different strategies.

"""

from typing import Union

from .helpers import ValidatingEnum


class SupportedEncoder(ValidatingEnum):
    unicode = "unicode"
    utf8 = "utf8"


class CharEncoder:
    """
    A class used to encode characters

    ...

    Attributes
    ----------
    encoder : fnc
        a function used to encode a character with a specific strategy

    """

    def __init__(self, encode_type: Union[SupportedEncoder, str]):
        """
        Parameters
        ----------
        encode_type: str
            A string symbolizing a encoding strategy
        """

        self.encoder = self._get_encoder(encode_type)

    def encode_char(self, character):
        """encodes a character using an encoder function

        Parameters
        ----------
        character : str
            character to be encoded

        Returns
        -------
        an encoded character
        """
        return self.encoder(character)

    @staticmethod
    def _get_encoder(encode_type: Union[SupportedEncoder, str]):
        try:
            _type = SupportedEncoder.get_by_name(encode_type)
            if _type == SupportedEncoder.unicode:
                return ord
            elif _type == SupportedEncoder.utf8:
                return CharEncoder.encode_utf8
        except TypeError:
            raise ValueError(f"Encoder type : {encode_type} not supported")

    @staticmethod
    def encode_utf8(character):
        """encodes a character with utf8 encoding

        Parameters
        ----------
        character : str
            character to be encoded

        Returns
        -------
        an encoded character with utf8
        """
        return character.encode('utf8')
