from pihace.healthcheck import HealthCheck
from pihace.pusher.elasticsearch import ElasticSearchPusher
from pihace.plugins.http import HTTP
from pihace.plugins.elasticsearch import ElasticSearch

hc = HealthCheck(with_system=True, name="MyApp", version="1.0.0")
hc.register("HTTP D", HTTP(url="https://example.com"))

es_url = "http://localhost:9200"
hc.register("Elastic Search Cluster", ElasticSearch(es_url=es_url), timeout=5, retries=2)
logger = ElasticSearchPusher(es_url=es_url, healthcheck=hc)
logger.push()
