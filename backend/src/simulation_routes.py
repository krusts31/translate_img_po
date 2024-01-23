from .jwt_verify import token_auth_scheme, get_user_id_from_token
from fastapi import Depends, Response, Request, HTTPException
from .docker import update_container_db, get_docker_client
from .models import PlantObject, Simulation, Plant
from fastapi.security import HTTPBearer
from functools import wraps
from loguru import logger
import uuid

async def run_simulation(
    request: Request,
    response: Response,
    docker_client=Depends(get_docker_client)
):
    if len(container_ids) > 1:
        """
        if this happens something went horibly wrong with update_conatiner_db
        """
        logger.error(f"more then 1 simulatino for user is not yet supported")
        raise HTTPException(
            status_code=500, detail="To many simulation running for 1 user"
        )
    if container_ids and not simulation.re_run:
        raise HTTPException(
            status_code=400, detail="Simulation is already running!"
        )
    if container_ids and simulation.re_run:
        container_id = container_ids[0]
        docker_client.stop_simulation(container_id)
    container_id = docker_client.start_simulation(user_id, plant.config_id)
    return {"status": "200", "session_id": session_id}

async def stop_simulation(
    request: Request,
    response: Response,
    docker_client=Depends(get_docker_client),
):
    if not container_ids:
        return {"body": "nothing to stop"}
    container_id = container_ids[0]
    docker_client.stop_simulation(container_id)
    return {"status": "200"}
