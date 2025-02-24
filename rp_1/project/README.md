Demo 2 MAS

This PoC runs 3 agents simulating a Telemetry Agent, the MLFO and the SO. The Telemetry Agent receives 
telemetry and based on a threshold raises a warning to the MLFO that conveys it to the SO.

The agent exposes two endpoints:
* /process: It provides the main functionality of the agent, this endpoint should be modified to provide the desired functionality.
* /health: Used to check if the agent runs, returns a 200 ok if so.

Requirements:

* Docker and Docker-Compose (usually included)

How to run it:

* Install the Docker Engine: https://docs.docker.com/engine/install/
* Run $ docker compose up -d --build