from fastapi import Request

from base import Base

class SMO(Base):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def register_routes(self):
        self.register_health_check()

        @self.app.post("/process")
        async def process(request: Request):
            incoming_data = await request.json()
            self.logger.info("SMO processing %s", incoming_data)
            incoming_data = await request.json()
            print(incoming_data)
            return {
                "status": "Anomaly detected",
                "service": self.app.state.config.get("role")
            }
