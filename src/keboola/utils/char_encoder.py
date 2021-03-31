class CharEncoder:
    """
    A class used to encode characters

    ...

    Attributes
    ----------
    encoder : fnc
        a function used to encode a character with a specific strategy

    """

    def __init__(self, encode_type: str):
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
    def _get_encoder(encode_type):
        """encodes a character using an encoder function

            Parameters
            ----------
            encode_type : str
                type of encoding function to be returned

            Returns
            -------
            an encoder function
        """
        if encode_type == "unicode":
            return ord
        elif encode_type == "utf8":
            return _encode_utf8
        else:
            raise ValueError(f"Encoder type : {encode_type} not supported")


def _encode_utf8(character):
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
