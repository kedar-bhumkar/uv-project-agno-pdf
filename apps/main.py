from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apps.settings import api_settings
from apps.routes.v1_router import v1_router

def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title=api_settings.title,
        description=api_settings.description,
        version=api_settings.version,
        docs_url="/docs" if api_settings.docs_enabled else None,
        redoc_url="/redoc" if api_settings.docs_enabled else None,
        openapi_url="/openapi.json" if api_settings.docs_enabled else None,
    )

    app.include_router(v1_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
   
    return app

# Create and expose the FastAPI app instance
app = create_app()

# This is important for uvicorn to find the app
__all__ = ["app"]