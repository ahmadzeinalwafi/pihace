from influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError
import traceback

class InfluxDB:
    def __init__(self, url: str, token: str = "", org: str = ""):
        self.url = url
        self.token = token
        self.org = org

    def __call__(self):
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
