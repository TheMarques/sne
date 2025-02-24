import logging
from json import load
from fastapi import FastAPI, Request

class Base:
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.app = FastAPI(**kwargs)
        config_path = kwargs.get('config_path')
        if config_path:
            self.app.state.config = self.load_config(config_path)
        self.register_routes()

    def load_config(self, file_path):
        with open(file_path, "r") as f:
            return load(f)

    def register_routes(self):
        self.register_health_check()
        self.register_process()

    def register_health_check(self):
        @self.app.get("/health")
        async def health_check():
            return {"status": "ok"}

    def register_process(self):
        @self.app.post("/process")
        async def process(request: Request):
            incoming_data = await request.json()
            self.logger.info("Base processing %s", incoming_data)
            return incoming_data
