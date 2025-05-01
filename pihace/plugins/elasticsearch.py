# -*- coding: utf-8 -*-
"""pihace.checkers.elasticsearch: Elasticsearch health check checker."""

from elasticsearch import Elasticsearch


class ElasticSearch:
    """Elasticsearch health checker for pihace."""
    
    def __init__(self, es_url: str):
        """
        Initialize the ElasticsearchChecker.
        
        :param es_url: Elasticsearch URL to connect to.
        :param timeout: Timeout in seconds for the health check request.
        """
        self.es_url = es_url
        self.es = Elasticsearch([self.es_url])

    def __call__(self):
        """
        Perform the health check for Elasticsearch cluster.
        
        :return: `True` if health status is green or yellow, otherwise a tuple with `False` and an error message.
        """
        try:
            # Perform the health check request
            health = self.es.cluster.health()
            
            # Check the status of the cluster
            if health["status"] in ["green", "yellow"]:
                return True
            return False, f"Elasticsearch health status: {health['status']}"

        except Exception as e:
            return False, f"pihace: log are unavailable - {str(e)}"