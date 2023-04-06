from fastapi import APIRouter
from app import generate

api_router = APIRouter()

api_router.include_router(generate.prompt)