from fastapi import APIRouter, status, UploadFile, File, Form
from fastapi.responses import FileResponse
import subprocess as sub
from googletrans import Translator
from typing import IO
import os
import time
# from optimizedSD import inpaint

# a = time.strftime("%Y-%m-%d-%H-%M-%S")
# filename = f"{str(a)}.png"
# translator = Translator()

prompt = APIRouter()


# async def save_img2img_img(file: IO):
#     path = './input/img2img'
#     content = file.read()
#     with open(os.path.join(path, filename), "w+b") as fp:
#         fp.write(content)
#     return f'{path}/{filename}'


# async def save_base_img(file: IO):
#     path = './input/inpaint/base_image'
#     content = file.read()
#     with open(os.path.join(path, filename), "w+b") as fp:
#         fp.write(content)
#     return f'{path}/{filename}'


# async def save_mask_img(file: IO):
#     path = './input/inpaint/mask_image'
#     content = file.read()
#     with open(os.path.join(path, filename), "w+b") as fp:
#         fp.write(content)
#     return f'{path}/{filename}'


# @prompt.post('/img2img/keyword', status_code=status.HTTP_200_OK)
# async def get_prompt_img2img(keyword: str = Form(), W: str = Form(), H: str = Form(),
#                             steps: str = Form(), format: str = Form(),
#                             samples: str = Form(), base_img: UploadFile = File()):
#     global b
#     base_path = save_img2img_img(base_img.file)

#     cmd = ['python', './optimizedSD/img2img.py', '--prompt', f'{keyword}', '--W', 
#             f'{int(W)}', '--H', f'{int(H)}', '--ddim_steps', f'{int(steps)}', '--format', 
#             f'{format}', '--n_samples', f'{int(samples)}', '--init-img', f'{base_path}', '--turbo']
#     b = sub.run(cmd)

#     return {"message" : "이미지 생성 성공"}


# @prompt.post('/inpaint/keyword', status_code=status.HTTP_200_OK)
# async def get_prompt(base_img: UploadFile = File(), mask_img: UploadFile = File(), keyword: str = Form(),
#                      steps: str = Form(), style : str = Form()):
#     global c

#     prompt = translator.translate(keyword, dest='en').text

#     base_path = await save_base_img(base_img.file)
#     mask_path = await save_mask_img(mask_img.file)

#     c = inpaint.main(style=style, base_path=base_path, mask_path=mask_path, prompt=prompt)
    
#     return {"message" : "이미지 수정 성공"}

b = ['./input/inpaint/base_image/2023-04-11-18-36-20.png', 
     './input/inpaint/base_image/2023-04-11-18-36-20.png', 
     './input/inpaint/base_image/2023-04-11-18-36-20.png', 
     './input/inpaint/base_image/2023-04-11-18-36-20.png']

@prompt.get('/generated_img2img/{id}')
async def get_image_inpainted(id : int):
    return FileResponse(b[id-1])


# @prompt.get('/generated_inpaint')
# async def get_image_img2img():
#     return FileResponse(c)