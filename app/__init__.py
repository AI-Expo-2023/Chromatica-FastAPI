from fastapi import APIRouter
from app import generate
from app import image

api_router = APIRouter()

api_router.include_router(generate.prompt)
api_router.include_router(image.image_post)