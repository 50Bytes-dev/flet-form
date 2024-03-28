from typing import Any


def required(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, set, tuple, dict)):
        return bool(value)
    return True
