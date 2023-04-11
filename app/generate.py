from fastapi import APIRouter, status, UploadFile, File, Form
import subprocess as sub
from googletrans import Translator
from typing import IO
import os
import time

a = time.strftime("%Y-%m-%d-%H-%M-%S")
translator = Translator()

prompt = APIRouter()


async def save_img2img_img(file: IO):
    path = './input/img2img'
    content = file.read()
    filename = f"{str(a)}.png"
    with open(os.path.join(path, filename), "w+b") as fp:
        fp.write(content)
    return f'{path}/{filename}'


async def save_base_img(file: IO):
    path = './input/inpaint/base_image'
    content = file.read()
    filename = f"{str(a)}.png"
    with open(os.path.join(path, filename), "w+b") as fp:
        fp.write(content)
    return f'{path}/{filename}'


async def save_mask_img(file: IO):
    path = './input/inpaint/mask_image'
    content = file.read()
    filename = f"{str(a)}.png"
    with open(os.path.join(path, filename), "w+b") as fp:
        fp.write(content)
    return f'{path}/{filename}'


@prompt.post('/img2img/keyword', status_code=status.HTTP_200_OK)
async def get_prompt_img2img(keyword: str = Form(), W: int = Form(), H: int = Form(),
                            steps: int = Form(), format: str = Form(),
                            samples: int = Form(), base_img: UploadFile = File()):
    
    base_path = save_img2img_img(base_img.file)

    cmd = ['python', './optimizedSD/img2img.py', '--prompt', f'{keyword}', '--W', 
            f'{W}', '--H', f'{H}', '--ddim_steps', f'{steps}', '--format', 
            f'{format}', '--n_samples', f'{samples}', '--init-img', f'{base_path}', '--turbo']
    sub.run(cmd)

    return


@prompt.post('/inpaint/keyword', status_code=status.HTTP_200_OK)
async def get_prompt(base_img: UploadFile = File(),mask_img: UploadFile = File(), keyword: str = translator.translate(Form(), dest='en').text,
                     steps: int = Form(), style : str = Form()):
    
    base_path = await save_base_img(base_img.file)
    mask_path = await save_mask_img(mask_img.file)

    cmd = ['python', './optimizedSD/inpaint.py']
    sub.run(cmd)
    return
