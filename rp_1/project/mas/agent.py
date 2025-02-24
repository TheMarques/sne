from fastapi import Request
import requests

from base import Base

class Agent(Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def register_routes(self):
        self.register_health_check()

        @self.app.post("/process")
        async def process(request: Request):
            incoming_data = await request.json()
            self.logger.info("Agent processing %s", incoming_data)
            if incoming_data.get("latency") > self.app.state.config.get("latency_threshold"):
                target_url = self.app.state.config.get("target_url")
                response = requests.post(target_url, json=self.app.state.config.get("message"))
                return response.json()
            return {
                "status": "No anomaly detected",
                "service": self.app.state.config.get("role")
            }
