import json
import sys
import uvicorn

from agent import Agent
from mlfo import MLFO
from smo import SMO
from network_function import NetworkFunction


def select_application(role, **kwargs):
    """
    Instantiate and return the appropriate application based on the role.
    Additional keyword arguments (like config_path) are passed to the constructor.
    """
    match role:
        case "agent":
            app_instance = Agent(**kwargs)
        case "network-function":
            app_instance = NetworkFunction(1, **kwargs)
        case "network-function-2":
            app_instance = NetworkFunction(2, **kwargs)
        case "mlfo":
            app_instance = MLFO(**kwargs)
        case "smo":
            app_instance = SMO(**kwargs)
        case _:
            raise Exception(f"Invalid role: {role}")
    return app_instance


if __name__ == "__main__":
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    with open(config_file, "r") as f:
        config = json.load(f)
    app_instance = select_application(config.get("role"), config_path=config_file)
    uvicorn.run(
        app_instance.app,
        host=app_instance.app.state.config.get("host", "127.0.0.1"),
        port=app_instance.app.state.config.get("port", 80)
    )
