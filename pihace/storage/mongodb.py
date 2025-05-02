# -*- coding: utf-8 -*-
"""pihace.storage.mongodb: Store health check results into a MongoDB collection."""

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime
from pihace.healthcheck import HealthCheck
from time import sleep
import traceback

class MongoStorage:
    """MongoDB storage for health check results."""

    def __init__(self, healthcheck: HealthCheck, dsn: str, database: str = "pihace", collection: str = "health_logs"):
        """
        Initialize the MongoStorage instance.

        :param dsn: MongoDB connection URI.
        :param database: Database name to store logs in.
        :param collection: Collection name where health data will be inserted.
        """
        self.dsn = dsn
        self.database = database
        self.collection = collection
        self.healthcheck = healthcheck
        try:
            self.client = MongoClient(self.dsn, serverSelectionTimeoutMS=2000)
            self.db = self.client[self.database]
            self.col = self.db[self.collection]
        except PyMongoError as e:
            raise RuntimeError(f"Failed to connect to MongoDB: {str(e)}")

    def save(self) -> bool:
        """
        Save a health check result to the collection.

        :param data: Dictionary of the health check result.
        :return: True if saved successfully, False otherwise.
        """
        try:
            result = self.healthcheck.check(output="dict")
            result["logged_at"] = datetime.utcnow()
            self.col.insert_one(result)
            return True
        except PyMongoError as e:
            print(f"[MongoStorage] Mongo error: {e}")
            return False
        except Exception:
            print(f"[MongoStorage] Unknown error: {traceback.format_exc()}")
            return False

    def run_forever_in_loop(self, interval: int = 60) -> None:
        """
        Run the health check and save the result to MongoDB in a loop.

        :param healthcheck: HealthCheck instance to run.
        :param interval: Time in seconds between each health check.
        """
        print(f"Starting to save health check results to MongoDB every {interval} seconds...")
        while True:
            result = self.healthcheck.check(output="dict")
            self.save(result)
            sleep(interval)