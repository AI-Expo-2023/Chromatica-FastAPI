from fastapi import APIRouter, status
from pydantic import BaseModel
import subprocess as sub

class GenerateImage(BaseModel):
    keyword: str
    W: int
    H: int
    steps: int
    format: str
    samples: int


prompt = APIRouter()

# @prompt.post('/txt2img/keyword', status_code=status.HTTP_200_OK)
# async def get_prompt_txt2img(image: GenerateImage):
#     cmd = ['python', './optimizedSD/txt2img.py', '--prompt', f'{image.keyword}', '--W', 
#            f'{image.W}', '--H', f'{image.H}', '--ddim_steps', f'{image.steps}', '--format', f'{image.format}', '--n_samples', f'{image.samples}']
#     sub.run(cmd)
#     return image.keyword


@prompt.post('/img2img/keyword', status_code=status.HTTP_200_OK)
async def get_prompt_img2img(image: GenerateImage):
    # TODO
    # mysql db e seo image gat go o gi
    # and save image
    cmd = ['python', './optimizedSD/img2img.py', '--prompt', f'{image.keyword}', '--W', 
            f'{image.W}', '--H', f'{image.H}', '--ddim_steps', f'{image.steps}', '--format', f'{image.format}', '--n_samples', f'{image.samples}', '--init-img', f'./input/input1.png', '--turbo']
    sub.run(cmd)
    return image.keyword


@prompt.post('/inpaint/keyword', status_code=status.HTTP_200_OK)
async def get_prompt(image: GenerateImage):
    cmd = ['python', './optimizedSD/img2img.py', '--prompt', f'{image.keyword}', '--W', 
            f'{image.W}', '--H', f'{image.H}', '--ddim_steps', f'{image.steps}', '--format', f'{image.format}', '--n_samples', f'{image.samples}', '--init-img', f'path']
    sub.run(cmd)
    return image.keyword

