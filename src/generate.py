from fastapi import APIRouter, status, UploadFile, File, Form
from pydantic import BaseModel
from googletrans import Translator
import subprocess as sub
import os
import uuid


# class GenerateImage(BaseModel):
#     keyword: str
#     W: int
#     H: int
#     steps: int
#     format: str
#     samples: int

translator = Translator()
prompt = APIRouter()

# @prompt.post('/txt2img/keyword', status_code=status.HTTP_200_OK)
# async def get_prompt_txt2img(image: GenerateImage):
#     cmd = ['python', './optimizedSD/txt2img.py', '--prompt', f'{image.keyword}', '--W', 
#            f'{image.W}', '--H', f'{image.H}', '--ddim_steps', f'{image.steps}', '--format', f'{image.format}', '--n_samples', f'{image.samples}']
#     sub.run(cmd)
#     return image.keyword


@prompt.post('/img2img/keyword', status_code=status.HTTP_200_OK)
async def get_prompt_img2img(keyword: str = translator.translate(Form(), dest='en').text, W: int = Form(), H: int = Form(),
                            steps: int = Form(), format: str = Form(),
                            samples: int = Form(), base_img: UploadFile = File()):

    # 번역
    #translated_keyword = translator.translate(keyword, dest='en').text

    content = base_img.file.read()
    filename = f"{str(uuid.uuid4())}.png"

    with open(os.path.join('./input/img2img', filename), "w+b") as fp:
        fp.write(content)

    # cmd = ['python', './optimizedSD/img2img.py', '--prompt', f'{image.keyword}', '--W', 
    #         f'{image.W}', '--H', f'{image.H}', '--ddim_steps', f'{image.steps}', '--format', 
    #         f'{image.format}', '--n_samples', f'{image.samples}', '--init-img', f'./input/input1.png', '--turbo']
    # sub.run(cmd)

    return


@prompt.post('/inpaint/keyword', status_code=status.HTTP_200_OK)
async def get_prompt(base_img: UploadFile = File(),mask_img: UploadFile = File(), keyword: str = translator.translate(Form(), dest='en').text,
                     steps: int = Form(), style : str = Form()):
    
    content = base_img.file.read()
    filename = f"{str(uuid.uuid4())}.png"

    with open(os.path.join('./input/inpaint', filename), "w+b") as fp:
        fp.write(content)

    return