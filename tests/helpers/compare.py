def flatten(data: dict) -> dict:

    def _flatten(data: dict, path: str = "") -> dict:
        result = {}
        for key, value in data.items():
            if isinstance(value, dict):
                result.update(_flatten(value, path + key + "."))
            else:
                result[path + key] = value
        return result

    return _flatten(data)


def compare_dict_keys(dict_1: dict, dict_2: dict, flatten_dicts: bool = True) -> bool:
    """Compare keys of two dictionaries.

    Args:
        dict_1: Dictionary 1.
        dict_2: Dictionary 2.
        flatten_dicts: Flatten nested dictionaries.

    Returns:
        True if keys are equal, False otherwise.
    """
    if flatten_dicts:
        dict_1 = flatten(dict_1)
        dict_2 = flatten(dict_2)
    return set(dict_1.keys()) == set(dict_2.keys())


def compare_dict_values(dict_1: dict, dict_2: dict, flatten_dicts: bool = True) -> bool:
    """Compare values of two dictionaries.

    Args:
        dict_1: Dictionary 1.
        dict_2: Dictionary 2.
        flatten_dicts: Flatten nested dictionaries.

    Returns:
        True if values are equal, False otherwise.
    """
    if flatten_dicts:
        dict_1 = flatten(dict_1)
        dict_2 = flatten(dict_2)
    return set(dict_1.values()) == set(dict_2.values())
