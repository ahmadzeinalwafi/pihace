# -*- coding: utf-8 -*-
"""pihace.utils: Utility functions for timestamping, status evaluation, and formatting."""

from datetime import datetime

def get_utc_timestamp() -> str:
    """
    Get the current UTC timestamp in ISO 8601 format.

    Returns:
        str: ISO-formatted UTC timestamp with 'Z' suffix (e.g., "2025-05-01T12:34:56.789123Z").
    """
    return datetime.utcnow().isoformat() + "Z"


def calculate_status(passed: int, total: int) -> str:
    """
    Calculate the health status based on passed and total checks.

    Args:
        passed (int): Number of successful checks.
        total (int): Total number of checks performed.

    Returns:
        str: One of "Available", "Partially Available", or "Unavailable".
    """
    if passed == total:
        return "Available"
    if passed == 0:
        return "Unavailable"
    return "Partially Available"


def format_rate(passed: int, total: int) -> str:
    """
    Format the health rate as a ratio string.

    Args:
        passed (int): Number of successful checks.
        total (int): Total number of checks.

    Returns:
        str: A string in the format "passed/total" (e.g., "3/5").
    """
    return f"{passed}/{total}"