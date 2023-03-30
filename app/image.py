from fastapi import APIRouter

image_post = APIRouter()

@image_post.get('/generated')
async def get_image():
    return