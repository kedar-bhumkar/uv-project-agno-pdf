from fastapi import APIRouter
from .agents import agents_router
from .health import health_router


v1_router = APIRouter(prefix="/v1", tags=["v1"])
v1_router.include_router(health_router)
v1_router.include_router(agents_router)


