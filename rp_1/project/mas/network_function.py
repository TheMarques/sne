from fastapi import Request
from base import Base

class NetworkFunction(Base):
    def __init__(self, fn_number, **kwargs):
        self.fn_number = fn_number
        super().__init__(**kwargs)

    def register_routes(self):
        self.register_health_check()

        @self.app.post("/process")
        async def process_request(request: Request):
            incoming_data = await request.json()
            self.logger.info("NetworkFunction %s processing data: %s", self.fn_number, incoming_data)
            cluster_name = self.app.state.config.get("cluster_name", "unknown")
            return {
                "status": f"Processed by NetworkFunction {self.fn_number}",
                "received": incoming_data,
                "region": cluster_name
            }
