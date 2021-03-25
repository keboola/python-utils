import string
from typing import List

PERMITTED_CHARS = string.digits + string.ascii_letters + '_'


def normalize_header(header: List[str], permitted_chars: str = PERMITTED_CHARS) -> List[str]:
    normalized = []

    for h in header:
        new_header = "".join(char for char in h if char in permitted_chars)
        normalized.append(new_header)
    return normalized


