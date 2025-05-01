from ..healthcheck import HealthCheck
from fastapi import FastAPI
from fastapi.responses import JSONResponse

class WebProvider:
    def __init__(self, healthcheck: HealthCheck):
        self.healthcheck = healthcheck
        self.app = FastAPI()
        self._setup_routes()

    def _setup_routes(self):
        @self.app.get("/healthcheck")
        async def health_check():
            result = await self.healthcheck._check_async()
            return JSONResponse(content=result)
        
        @self.app.get("/")
        async def status():
            return JSONResponse(content={'status': 'ok', 'message': 'pihace web server is running'})

    def serve(self, host: str = '0.0.0.0', port: int = 8000):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)