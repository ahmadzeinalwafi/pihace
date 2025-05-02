from pihace.healthcheck import HealthCheck
from pihace.plugins.http import HTTP
from pihace.providers.web import WebProvider

if __name__ == "__main__":
    hc = HealthCheck(with_system=True, name="example-api", version="v0.1.0")
    hc.register("HTTP D", HTTP(url="https://example.com"))

    http = WebProvider(hc)
    http.serve()