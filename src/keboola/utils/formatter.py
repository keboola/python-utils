from typing import List


def comma_separated_values_to_list(csv_string: str) -> List:
    if not isinstance(csv_string, str):
        raise TypeError("input must be a string")
    cols = []
    if csv_string:
        cols = [p.strip() for p in csv_string.split(",")]
    return cols
