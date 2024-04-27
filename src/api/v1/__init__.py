from fastapi import APIRouter

from src.api.v1.locate_router import router as locate_router

router = APIRouter(prefix="/v1")
router.include_router(locate_router)
