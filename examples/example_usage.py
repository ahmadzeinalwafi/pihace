from pihace.healthcheck import HealthCheck
from pihace.plugins.mysql import MySQL
from pihace.plugins.mongodb import MongoDB
from pihace.plugins.influxdb import InfluxDB
from pihace.plugins.http import HTTP

if __name__ == "__main__":
    hc = HealthCheck(with_system=True, name="example-api", version="v0.1.0")

    hc.register("MySQL A", MySQL(dsn="mysql://root:root@localhost:3306/testdb"), timeout=5, retries=2)
    hc.register("MongoDB B", MongoDB(dsn="mongodb://localhost:27017"))
    hc.register("InfluxDB C", InfluxDB(url="http://localhost:8086", token="admintoken", org="myorg"))
    hc.register("HTTP D", HTTP(url="https://example.com"))

    print(hc.check(output="str"))
    print(hc.check(output="json", pretty=True))
    print(hc.check())