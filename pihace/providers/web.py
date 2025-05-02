# -*- coding: utf-8 -*-
"""pihace.providers.web: FastAPI-based HTTP provider for exposing health check endpoints."""

from pihace.healthcheck import HealthCheck
from fastapi import FastAPI
from fastapi.responses import JSONResponse

class WebProvider:
    """
    A FastAPI-based HTTP server provider for serving health check endpoints.

    Attributes:
        healthcheck (HealthCheck): An instance of the HealthCheck class.
        app (FastAPI): The FastAPI application instance.
    """
    def __init__(self, healthcheck: HealthCheck, host: str = '0.0.0.0', port: int = 8000):
        """
        Initialize the WebProvider with a HealthCheck instance.

        Args:
            host (str): The host IP address to bind the server.
            port (int): The port to expose the server.
            healthcheck (HealthCheck): A configured HealthCheck object.
        """
        self.healthcheck = healthcheck
        self.app = FastAPI()
        self._setup_routes()
        self.host = host
        self.port = port

    def _setup_routes(self):
        """
        Internal method to define HTTP routes for the FastAPI app.

        Routes:
            GET /healthcheck - Executes and returns health check results.
            GET / - Returns a simple status message.
        """
        @self.app.get("/healthcheck")
        async def health_check():
            """Endpoint for performing a full health check."""
            result = await self.healthcheck._check_async()
            return JSONResponse(content=result)
        
        @self.app.get("/")
        async def status():
            """Endpoint for checking server status."""
            return JSONResponse(content={'status': 'ok', 'message': 'pihace web server is running'})

    def serve(self):
        """
        Run the FastAPI app using Uvicorn.
        """
        import uvicorn
        uvicorn.run(self.app, host=self.host, port=self.port)