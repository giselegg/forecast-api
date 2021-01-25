from datetime import datetime
from fastapi import APIRouter

health_router = APIRouter(prefix="/health")


@health_router.get("")
def alive():
    return {"timestamp": datetime.now()}
