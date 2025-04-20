from pymongo import MongoClient
from pymongo.errors import PyMongoError
from ..base_checker import BaseChecker

class MongoDB(BaseChecker):
    def __init__(self, dsn):
        self.dsn = dsn

    def check(self):
        try:
            client = MongoClient(self.dsn, serverSelectionTimeoutMS=2000)
            client.server_info()
            return True
        except PyMongoError as e:
            return (False, str(e))
        except Exception:
            return (False, "pihace: log are unavailable")
