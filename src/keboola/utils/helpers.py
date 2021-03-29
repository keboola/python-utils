from typing import List


def comma_separated_values_to_list(csv_string: str) -> List:
    '''
    Coverts a string with comma separated values to a list of these values
    Args:
        csv_string : string containing comma separated values

    Returns: separated_list of parsed elements from the input

    '''
    if not isinstance(csv_string, str):
        raise TypeError("input must be a string")
    parsed_list = []
    if csv_string:
        parsed_list = [p.strip() for p in csv_string.split(",")]
    return parsed_list
