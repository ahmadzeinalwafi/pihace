from ..healthcheck import HealthCheck
from fastapi import FastAPI
from fastapi.responses import JSONResponse

class WebProvider:
    def __init__(self, healthcheck: HealthCheck):
        self.healthcheck = healthcheck
        self.app = FastAPI()
        self._setup_routes()

    def _setup_routes(self):
        @self.app.get("/health")
        async def health_check():
            return JSONResponse(content=self.healthcheck.check())

    def serve(self, host: str = '0.0.0.0', port: int = 8000):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)