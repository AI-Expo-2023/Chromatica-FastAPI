from fastapi import APIRouter
from app import prompt

api_router = APIRouter()

api_router.include_router(prompt.prompt, prefix="/prompts")
