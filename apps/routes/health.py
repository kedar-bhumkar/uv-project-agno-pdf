from fastapi import APIRouter


health_router = APIRouter(tags=["Health"])


@health_router.get("/health")
def health_check():
    return {"status": "ok"}



@health_router.post("/ready")
def ready_check():
    return {"status": "Yes"}

