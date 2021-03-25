from typing import List


def comma_separated_values_to_list(csv_string: str) -> List:
    cols = []
    if csv_string:
        cols = [p.strip() for p in csv_string.split(",")]
    return cols
