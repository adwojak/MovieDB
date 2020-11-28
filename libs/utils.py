from re import compile as re_compile, Pattern
from typing import Dict


def _to_snake_case(camel_case_key: str, pattern: Pattern) -> str:
    return pattern.sub('_', camel_case_key).lower()


def to_snake_case(values: dict, keys_for_manual_override: Dict) -> dict:
    pattern = re_compile(r'(?<!^)(?=[A-Z])')
    new_dict = {}
    for key, value in values.items():
        if key in keys_for_manual_override.keys():
            new_dict[keys_for_manual_override[key]] = value
            continue
        if isinstance(value, dict):
            new_dict[_to_snake_case(key, pattern)] = to_snake_case(value, keys_for_manual_override)
        elif isinstance(value, list):
            new_dict[_to_snake_case(key, pattern)] = [to_snake_case(item, keys_for_manual_override) for item in value]
        else:
            new_dict[_to_snake_case(key, pattern)] = value
    return new_dict
