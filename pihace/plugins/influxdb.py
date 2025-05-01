# -*- coding: utf-8 -*-
"""pihace.plugin.influxdb: InfluxDB health check plugin using the InfluxDB client."""
from influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError
import traceback

class InfluxDB:
    """
    A checker class for performing health checks on an InfluxDB instance.

    Attributes:
        url (str): The URL of the InfluxDB instance.
        token (str): The authentication token for InfluxDB (default: empty string).
        org (str): The organization name for InfluxDB (default: empty string).
    """

    def __init__(self, url: str, token: str = "", org: str = ""):
        """
        Initialize the InfluxDB checker with a URL, token, and organization.

        Args:
            url (str): The URL of the InfluxDB instance.
            token (str): The authentication token for InfluxDB (default: empty string).
            org (str): The organization name for InfluxDB (default: empty string).
        """
        self.url = url
        self.token = token
        self.org = org

    def __call__(self):
        """
        Perform a health check on the InfluxDB instance.

        Returns:
            bool: True if the InfluxDB health status is 'pass'.
            tuple: (False, error message) if the health status is not 'pass' or an error occurs.
        """
        try:
            with InfluxDBClient(url=self.url, token=self.token, org=self.org) as client:
                health = client.health()
                if health.status == "pass":
                    return True
                else:
                    return (False, f"InfluxDB health status: {health.status}")
        except InfluxDBError as e:
            return (False, str(e))
        except Exception as e:
            return (False, traceback.format_exc())
