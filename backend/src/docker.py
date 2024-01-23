from fastapi import HTTPException, Request
from loguru import logger
import docker

def get_docker_client(request: Request):
    return request.app.state.docker_client

async def update_container_db(db, docker_client, user_id: str):
    """
    Synchronize the simulation statuses in the database with the
    running Docker containers.
    Not a route!
    """
    simulation_ids = await db.get_users_running_simulations(user_id)

    running_containers = docker_client.get_all_running_containers_from_docker()

    running_container_ids = [container.id for container in running_containers]

    """
    here we need to syncornize
    we just set the simulations that are in the DB to finished in they
    are not longer in running_container_ids
    """
    for simulation_id in simulation_ids:
        if simulation_id not in running_container_ids:
            await db.set_simulation_to_finished(simulation_id)


class DockerClient:
    def __init__(self):
        self.client = docker.DockerClient(base_url="unix://var/run/docker.sock")

    def get_all_running_containers_from_docker(self):
        return self.client.containers.list()

    def container_exists(self, name: str) -> bool:
        containers = self.client.containers.list()

        for container in containers:
            image_name = container.attrs["Config"]["Image"]
            if name in image_name:
                return True
        return False

    def resume_simulation(self, container_id: str):
        try:
            container = self.client.containers.get(container_id)
            container.unpause()
        except docker.errors.NotFound:
            logger.error(f"Container {container_id} not found.")
            raise HTTPException(status_code=500, detail="Container not found.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail="Error while stoping")

    def pause_simulation(self, container_id: str):
        try:
            container = self.client.containers.get(container_id)
            container.pause()
        except docker.errors.NotFound:
            logger.error(f"Container {container_id} not found.")
            raise HTTPException(status_code=500, detail="Container not found.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail="Error while stoping")

    def stop_simulation(self, container_id: str):
        try:
            container = self.client.containers.get(container_id)
            container.stop(timeout=0)
        except docker.errors.NotFound:
            logger.error(f"Container {container_id} not found.")
            raise HTTPException(status_code=500, detail="Container not found.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail="Error while stoping")

    def start_simulation(self, user_id: str, config_id: int):
        try:
            env_vars = {
                "SEND_MQTT": "True",
                "MQTT_FF_RATIO": "20",
                "MQTT_PARTIAL_LVL": "0",
                "RT_RATIO": 0.0005,
                "USER_ID": user_id,
                "SESSION_ID": user_id,
                "MQTT_HOST": "vernemq",
                "SHOW_PLOTS": "False",
                "CONFIG_ID": config_id,
            }
            print("ENV!!!", env_vars, flush=True)
            container = self.client.containers.run(
                "future-steel-simulator",
                detach=True,
                environment=env_vars,
                network_mode="future_steelmaking_net",
            )
            return container.id
        except Exception as e:
            logger.error(f"Docker error: {e}")
            raise HTTPException(status_code=500, detail="Failed to Start simulation")
