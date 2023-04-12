from fastapi import APIRouter, status, UploadFile, File, Form
from fastapi.responses import FileResponse
import subprocess as sub
from googletrans import Translator
from typing import IO
import os
import time
from optimizedSD import img2img, inpaint

a = time.strftime("%Y-%m-%d-%H-%M-%S")
filename = f"{str(a)}.png"
translator = Translator()

prompt = APIRouter()


async def save_img2img_img(file: IO):
    path = './input/img2img'
    content = file.read()
    with open(os.path.join(path, filename), "w+b") as fp:
        fp.write(content)
    return f'{path}/{filename}'


async def save_base_img(file: IO):
    path = './input/inpaint/base_image'
    content = file.read()
    with open(os.path.join(path, filename), "w+b") as fp:
        fp.write(content)
    return f'{path}/{filename}'


async def save_mask_img(file: IO):
    path = './input/inpaint/mask_image'
    content = file.read()
    with open(os.path.join(path, filename), "w+b") as fp:
        fp.write(content)
    return f'{path}/{filename}'


@prompt.post('/img2img/keyword', status_code=status.HTTP_200_OK)
async def get_prompt_img2img(keyword: str = Form(), W: str = Form(), H: str = Form(),
                            steps: str = Form(), format: str = Form(),
                            samples: str = Form(), base_img: UploadFile = File()):
    
    #TODO
    # 코드 돌리고 나온 이미지 경로 리스트 b 변수에 저장
    global b
    base_path = save_img2img_img(base_img.file)

    cmd = ['python', './optimizedSD/img2img.py', '--prompt', f'{keyword}', '--W', 
            f'{int(W)}', '--H', f'{int(H)}', '--ddim_steps', f'{int(steps)}', '--format', 
            f'{format}', '--n_samples', f'{int(samples)}', '--init-img', f'{base_path}', '--turbo']
    sub.run(cmd)

    b = img2img.image_list
    
    return 'http://0.0.0.0:3333/generated_img2img'


@prompt.post('/inpaint/keyword', status_code=status.HTTP_200_OK)
async def get_prompt(base_img: UploadFile = File(), mask_img: UploadFile = File(), keyword: str = Form(),
                     steps: str = Form(), style : str = Form()):
    global inpainted_image

    prompt = translator.translate(keyword, dest='en').text

    base_path = await save_base_img(base_img.file)
    mask_path = await save_mask_img(mask_img.file)

    inpainted_image = inpaint.main(style=style, base_path=base_path, mask_path=mask_path, prompt=prompt)
    
    return 'http://0.0.0.0:3333/generated_inpaint'

# 이미지 경로

# TODO
# 사용자별 사진 구분 기능 추가
@prompt.get('/generated_img2img/{id}')
async def get_image_inpainted(id : int):
    if b[id-1] == '':
        return
    else:
        return FileResponse(b[id-1])
    

@prompt.get('/generated_inpaint')
async def get_image_img2img():
    return FileResponse(inpainted_image)


@prompt.get('/generated_img2img')
async def get_image():
    url = ['http://0.0.0.0:3333/generated_img2img/1', 
           'http://0.0.0.0:3333/generated_img2img/2', 
           'http://0.0.0.0:3333/generated_img2img/3', 
           'http://0.0.0.0:3333/generated_img2img/4']
    return url