"""Utility helper functions."""


def ensure_list(value):
    """
    Ensure the value is a list.

    Args:
        value: Input value

    Returns:
        List containing the value, or the value itself if already a list
    """
    if isinstance(value, list):
        return value
    return [value]
