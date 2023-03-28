from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import subprocess as sub
import base64

class GenerateImage(BaseModel):
    keyword: str
    W: int
    H: int
    steps: int
    format: str
    samples: int
    base64_image: Optional[str] = None


class base64Request(BaseModel):
    base64_file : str


class base64Response(BaseModel):
    response_code : str


prompt = APIRouter()

@prompt.post('/txt2img/keyword')
async def get_prompt_txt2img(image: GenerateImage):
    cmd = ['python', './optimizedSD/txt2img.py', '--prompt', f'{image.keyword}', '--W', 
           f'{image.W}', '--H', f'{image.H}', '--ddim_steps', f'{image.steps}', '--format', f'{image.format}', '--n_samples', f'{image.samples}']
    sub.run(cmd)
    return image.keyword


@prompt.post('/img2img/keyword')
async def get_prompt_img2img(image: GenerateImage):
    cmd = ['python', './optimizedSD/img2img.py', '--prompt', f'{image.keyword}', '--W', 
            f'{image.W}', '--H', f'{image.H}', '--ddim_steps', f'{image.steps}', '--format', f'{image.format}', '--n_samples', f'{image.samples}', '--init-img', f'path']
    sub.run(cmd)
    return image.keyword


@prompt.post('/img2img/image', response_model=base64Request)
async def get_image_img2img(request: base64Request):
    file_content = request.base64_file
    base64_content = base64.encode(file_content)



    response = base64Response(
        response_code="200"
    ).dict()

    return response


@prompt.post('/inpaint/keyword')
async def get_prompt(image: GenerateImage):
    return image.keyword

