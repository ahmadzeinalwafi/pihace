# -*- coding: utf-8 -*-
"""pihace.plugins.http: HTTP plugin for checking http service."""
import requests

class HTTP:
    """
    A checker class for performing HTTP GET requests to a given URL.

    Attributes:
        url (str): The URL to be checked.
        timeout (int): The timeout for the HTTP request in seconds (default: 5).
    """

    def __init__(self, url: str, timeout: int = 5):
        """
        Initialize the HTTP checker with a URL and timeout.

        Args:
            url (str): The URL to check.
            timeout (int): The timeout for the HTTP request in seconds (default: 5).
        """
        self.url = url
        self.timeout = timeout

    def __call__(self):
        """
        Perform an HTTP GET request to the provided URL and return the result.

        Returns:
            bool: True if the request was successful (status code 200).
            tuple: (False, error message) if the request failed.
        """
        try:
            response = requests.get(self.url, timeout=self.timeout)
            if response.ok:
                return True
            return False, f"Status code: {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)
