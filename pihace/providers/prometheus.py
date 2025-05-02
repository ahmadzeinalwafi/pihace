# -*- coding: utf-8 -*-
"""pihace.providers.prometheus: Exposes health check results as Prometheus metrics."""

from fastapi import FastAPI
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from ..healthcheck import HealthCheck
import uvicorn

class PrometheusProvider:
    """
    PrometheusProvider exposes health check metrics for Prometheus scraping.
    """

    def __init__(self, healthcheck: HealthCheck):
        """
        Initialize the provider with a HealthCheck instance.

        :param healthcheck: A HealthCheck object containing registered checkers.
        """
        self.healthcheck = healthcheck
        self.app = FastAPI()
        self._setup_routes()

        # Core metric
        self.status_metric = Gauge("pihace_status", "Overall health status (1=healthy, 0=unhealthy)", ["component"])
        self.duration_metric = Gauge("pihace_duration_seconds", "Time taken for the health check", ["component"])
        self.failure_count_metric = Gauge("pihace_failure_count", "Number of failed checks", ["component"])

        # Per-service metrics
        self.service_metrics = Gauge("pihace_service_status", "Service health status (1=ok, 0=fail)", ["service"])

        # Optional system-level metrics
        self.system_metrics = {
            "cpu_usage": Gauge("pihace_system_cpu_usage", "CPU usage percentage"),
            "memory_usage": Gauge("pihace_system_memory_usage", "Memory usage percentage"),
            "memory_available": Gauge("pihace_system_memory_available_mb", "Available memory in MB"),
            "disk_usage": Gauge("pihace_system_disk_usage", "Disk usage percentage"),
            "disk_available": Gauge("pihace_system_disk_available_gb", "Available disk in GB"),
        }

    def _normalize_name(self, name: str) -> str:
        """
        Helper function to normalize service names for Prometheus metrics.
        Replaces spaces with underscores and converts to lowercase.
        """
        return name.strip().replace(" ", "_").lower()

    def _setup_routes(self):
        """
        Prometheus-compatible metrics endpoint.
        """
        @self.app.get("/metrics")
        async def metrics():
            results = await self.healthcheck._check_async()
            component_name = self._normalize_name(self.healthcheck.component_name or "pihace")

            # Map status to binary
            status = results["status"]
            status_value = 1 if status == "Available" else 0
            self.status_metric.labels(component=component_name).set(status_value)

            self.duration_metric.labels(component=component_name).set(results["duration"])
            failure_count = len(results["failure"] or {})
            self.failure_count_metric.labels(component=component_name).set(failure_count)

            # Set per-service metrics
            for svc, msg in (results["failure"] or {}).items():
                self.service_metrics.labels(service=self._normalize_name(svc)).set(0)
            for svc in self.healthcheck.checkers.keys():
                if svc not in (results["failure"] or {}):
                    self.service_metrics.labels(service=self._normalize_name(svc)).set(1)

            # System info metrics
            system = results.get("system") or {}
            if system:
                try:
                    self.system_metrics["cpu_usage"].set(float(system["cpu_usage"].strip("%")))
                    self.system_metrics["memory_usage"].set(float(system["memory_usage"].strip("%")))
                    self.system_metrics["memory_available"].set(float(system["memory_available"].strip(" MB")))
                    self.system_metrics["disk_usage"].set(float(system["disk_usage"].strip("%")))
                    self.system_metrics["disk_available"].set(float(system["disk_available"].strip(" GB")))
                except Exception:
                    pass  # Ignore format issues in system metrics

            return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

    def serve(self, host: str = "0.0.0.0", port: int = 9090):
        """
        Serve the metrics endpoint using Uvicorn.

        :param host: Host address to bind.
        :param port: Port to serve on.
        """
        uvicorn.run(self.app, host=host, port=port)
