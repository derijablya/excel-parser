from fastapi.routing import APIRouter

import app.routes as routes

api_router = APIRouter()


for name, entity in routes.__dict__.items():
    if not name.startswith("__"):
        api_router.include_router(router=getattr(entity, "router"))
