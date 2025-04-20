from pihace.healthcheck import HealthCheck
from pihace.checkers.mysql import MySQL
from pihace.checkers.mongodb import MongoDB
from pihace.checkers.influxdb import InfluxDB

hc = HealthCheck(with_system=True, name="example-api", version="v0.1.0")

hc.register("MySQL A", MySQL(dsn="mysql://root:root@localhost:3306/testdb"))
hc.register("MongoDB B", MongoDB(dsn="mongodb://localhost:27017"))
hc.register("InfluxDB C", InfluxDB(url="http://localhost:8086", token="admintoken", org="myorg"))

print(hc.check())
