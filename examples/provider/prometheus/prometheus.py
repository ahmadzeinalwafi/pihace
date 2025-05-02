from pihace.healthcheck import HealthCheck
from pihace.providers.prometheus import PrometheusProvider
from pihace.plugins.http import HTTP

hc = HealthCheck(name="myapp", version="1.0.0")

hc.register("HTTP D", HTTP(url="https://example.com"))
hc.register("HTTP E", HTTP(url="https://asdasdjnladojanbdbaiu.com"))

exporter = PrometheusProvider(healthcheck=hc)
exporter.serve(port=5001)