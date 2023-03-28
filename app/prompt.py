from fastapi import APIRouter
from pydantic import BaseModel
from typing import Union
import json


class GenerateImage(BaseModel):
    keyword: str
    W: Union[int, None] = None
    H: Union[int, None] = None
    steps: Union[int, None] = None
    format: Union[str, None]
    samples: Union[int, None] = None

prompt = APIRouter()

@prompt.post('/txt2img/keyword')
async def get_prompt(image: GenerateImage):
    return image

@prompt.post('/img2img/keyword')
async def get_prompt(image: GenerateImage):
    return image


@prompt.post('/inpaint/keyword')
async def get_prompt(image: GenerateImage):
    return image

