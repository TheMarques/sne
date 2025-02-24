import requests
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import Request
from kubernetes import client, config

from base import Base


class MLFO(Base):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, lifespan=self.lifespan)

    def register_routes(self):
        self.register_health_check()

        @self.app.post("/process")
        async def process(request: Request):
            incoming_data = await request.json()
            print(incoming_data)
            if not hasattr(self.app.state, "agents_alive"):
                self.app.state.agents_alive = {}
            self.update_active_agents()
            target_url = self.app.state.config.get("target_url")
            response = requests.post(target_url, json=incoming_data)
            response_data = response.json()
            return {
                "status": "Processed by MLFO",
                "tracked_agents": list(self.app.state.agents_alive.keys()),
                "response_data": response_data
            }

    @asynccontextmanager
    async def lifespan(self):
        config.load_incluster_config()
        if not hasattr(self.app.state, "config"):
            raise Exception("Configuration not loaded. Ensure app.state.config is set before startup.")
        self.app.state.agents_alive = {}
        self.app.state.last_query_time = None
        self.logger.info("MLFO role detected. Initializing agent tracking.")
        yield
        self.logger.info("Shutting down FastAPI app...")

    def update_active_agents(self):
        """
        Queries the Kubernetes API to update the list of active agent pods.
        """
        current_time = datetime.utcnow()
        cache_duration = self.app.state.config.get("cache_duration", 10)  # Cache results for 10 seconds
        if self.app.state.last_query_time and (current_time - self.app.state.last_query_time).total_seconds() < cache_duration:
            return
        self.app.state.last_query_time = current_time
        config.load_incluster_config()
        v1 = client.CoreV1Api()
        pods = v1.list_namespaced_pod(namespace="desire6g", label_selector="role=agent").items
        self.logger.info(f"Found pods: {pods}")
        for pod in pods:
            if pod.status.conditions:
                for condition in pod.status.conditions:
                    if condition.type == "Ready" and condition.status == "True":
                        self.app.state.agents_alive[pod.metadata.name] = current_time
        inactivity_threshold = self.app.state.config.get("inactivity_threshold", 300)  # 5 minutes
        inactive_agents = [
            agent for agent, last_active in self.app.state.agents_alive.items()
            if (current_time - last_active).total_seconds() > inactivity_threshold
        ]
        for agent in inactive_agents:
            del self.app.state.agents_alive[agent]
