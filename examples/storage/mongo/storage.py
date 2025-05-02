from pihace.healthcheck import HealthCheck
from pihace.plugins.http import HTTP
from pihace.storage.mongodb import MongoStorage

hc = HealthCheck(with_system=True, name="MyApp", version="1.0.0")
hc.register("HTTP D", HTTP(url="https://example.com"))
result = hc.check()

storage = MongoStorage(dsn="mongodb://localhost:27017", database="myapp", collection="hc_logs")
storage.save(result)
