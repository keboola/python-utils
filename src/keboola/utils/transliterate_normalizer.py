from abc import ABC

from camel_tools.utils.charmap import CharMapper
from keboola.utils.header_normalizer import HeaderNormalizer, PERMITTED_CHARS, DEFAULT_WHITESPACE_SUB
from camel_tools.utils.transliterate import Transliterator


class TransliterateHeaderNormalizer(HeaderNormalizer, ABC):

    def __init__(self, transliterator_mapper: str, permitted_chars: str = PERMITTED_CHARS,
                 whitespace_sub: str = DEFAULT_WHITESPACE_SUB):
        super().__init__(permitted_chars=permitted_chars, whitespace_sub=whitespace_sub)
        self.transliterator_mapper = transliterator_mapper

    def _normalize_column_name(self, header: str) -> str:
        header = self._transliterate(header)
        return header

    def _transliterate(self, header: str) -> str:
        transliterator = Transliterator(CharMapper.builtin_mapper(self.transliterator_mapper))
        return transliterator.transliterate(header)
