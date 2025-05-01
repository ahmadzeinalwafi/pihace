# -*- coding: utf-8 -*-
"""pihace.plugins.mongodb: MongoDB health check plugin using the PyMongo client."""

from pymongo import MongoClient
from pymongo.errors import PyMongoError

class MongoDB():
    """
    A checker class for performing health checks on a MongoDB instance.

    Attributes:
        dsn (str): The Data Source Name (DSN) or connection string for MongoDB.
    """
    def __init__(self, dsn):
        """
        Initialize the MongoDB checker with a DSN.

        Args:
            dsn (str): The Data Source Name (DSN) for the MongoDB instance.
        """
        self.dsn = dsn

    def __call__(self):
        """
        Perform a health check on the MongoDB instance.

        Returns:
            bool: True if the MongoDB connection is successful and server info can be fetched.
            tuple: (False, error message) if the health check fails or an exception occurs.
        """
        try:
            client = MongoClient(self.dsn, serverSelectionTimeoutMS=2000)
            client.server_info()
            return True
        except PyMongoError as e:
            return (False, str(e))
        except Exception:
            return (False, "pihace: log are unavailable")
