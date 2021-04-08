"""
General helper functions and classes that are relevant in Keboola Connection environment.


"""
from enum import Enum
from typing import List, Union


class ValidatingEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))

    @classmethod
    def validate_fields(cls, fields: List[Union[Enum, str]]):
        errors = []
        for f in fields:
            valid, error = cls.validate_field(f)
            if error:
                errors.append(error)
        if errors:
            raise ValueError(
                ', '.join(errors) + f'\n Supported {cls.__name__} values are: [{cls.list()}]')

    @classmethod
    def validate_field(cls, field: Union[Enum, str]):
        error = ''
        valid = True
        if isinstance(field, cls):
            pass
        elif isinstance(field, str):
            if field not in cls.list():
                error = f'"{field}" is not valid {cls.__name__} value!'
                valid = False
        else:
            error = f'"{field}" is not valid Enum {cls.__name__} type!'
            valid = False

        return valid, error

    @classmethod
    def get_by_name(cls, name: Union[Enum, str]):
        instance = None
        if isinstance(name, cls):
            instance = name
        elif isinstance(name, str) and name in cls.list():
            instance = cls.__get_instance_by_name(name)
        else:
            raise TypeError(f'"{name}" is not valid {cls.__name__} name or instance!')

        return instance

    @classmethod
    def __get_instance_by_name(cls, name: str):
        for inst in cls:
            if name == inst.name:
                return inst


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
