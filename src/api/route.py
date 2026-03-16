from fastapi.routing import APIRouter
from src.api.endpoints_v1 import router as endpoints_v1

all_router= APIRouter()

all_router.include_router(endpoints_v1, prefix = "/v1")