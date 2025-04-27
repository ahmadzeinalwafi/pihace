from pymongo import MongoClient
from pymongo.errors import PyMongoError

class MongoDB():
    def __init__(self, dsn):
        self.dsn = dsn

    def __call__(self):
        try:
            client = MongoClient(self.dsn, serverSelectionTimeoutMS=2000)
            client.server_info()
            return True
        except PyMongoError as e:
            return (False, str(e))
        except Exception:
            return (False, "pihace: log are unavailable")
