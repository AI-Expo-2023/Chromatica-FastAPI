from fastapi import APIRouter, status, File, Form
from pydantic import BaseModel
from fastapi.responses import FileResponse
import subprocess as sub
from googletrans import Translator
from PIL import Image
from io import BytesIO
import os, time, base64
from optimizedSD import inpaint#, img2img
from urllib import request

translator = Translator()

prompt = APIRouter()
b = ['output/img2img/2023-04-14-17-11-57/522ab281-88e9-452b-b17a-5c1f5f47578a.png', 'output/img2img/2023-04-14-17-11-57/ffb9c4dc-e6af-4df1-a618-6636cda76bb4.png']

async def save_img2img_img(file):
    a = time.strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{str(a)}.png"
    path = './input/img2img'
    content_byte = str.encode(file)
    content = base64.b64decode(content_byte)
    with open(os.path.join(path, filename), "w+b") as fp:
        fp.write(content)
    return f'{path}/{filename}'


async def save_base_img(file):
    a = time.strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{str(a)}.png"
    path = './input/inpaint/mask_image'
    content_byte = str.encode(file)
    content = base64.b64decode(content_byte)
    with open(os.path.join(path, filename), "w+b") as fp:
        fp.write(content)
    return f'{path}/{filename}'


async def save_mask_img(file):
    a = time.strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{str(a)}.png"
    path = './input/inpaint/mask_image'
    content_byte = str.encode(file)
    content = base64.b64decode(content_byte)
    with open(os.path.join(path, filename), "w+b") as fp:
        fp.write(content)
    return f'{path}/{filename}'


@prompt.post('/img2img/keyword', status_code=status.HTTP_200_OK)
async def get_prompt_img2img(keyword: str = Form(), W: str = Form(), H: str = Form(),
                            steps: str = Form(), format: str = Form(),
                            samples: str = Form(), base_img: str = Form()):
    
    #TODO
    # 코드 돌리고 나온 이미지 경로 리스트 b 변수에 저장
    #global b

    prompt = translator.translate(keyword, dest='en').text
    base_path = await save_img2img_img(base_img)

    cmd = ['python', './optimizedSD/img2img.py', '--prompt', f'{prompt}', '--W', 
            f'{int(W)}', '--H', f'{int(H)}', '--ddim_steps', f'{int(steps)}', '--format', 
            f'{format}', '--n_samples', f'{int(samples)}', '--init-img', f'{base_path}', '--turbo']
    sub.run(cmd)

    #b = img2img.image_list
    
    return 'http://0.0.0.0:3333/generated_img2img'


@prompt.post('/inpaint/keyword', status_code=status.HTTP_200_OK)
async def get_prompt(base_img: str = Form(), mask_img: str = Form(), 
                     keyword: str = Form(), steps: str = Form(), style : str = Form()):
    global inpainted_image
    # base_img = image url
    # python request lib


    prompt = translator.translate(keyword, dest='en').text
    with request.urlopen(base_img) as img:
        base_img = base64.b64encode(img.read()).decode('utf-8')

    base_path = await save_base_img(base_img)
    mask_path = await save_mask_img(mask_img)

    inpainted_image = inpaint.main(style=style, base_path=base_path, mask_path=mask_path, prompt=prompt)
    
    return 'http://192.168.0.113:3333/generated_inpaint'

# 이미지 경로

# TODO
# 사용자별 사진 구분 기능 추가
@prompt.get('/generated_img2img/{id}')
async def get_image_inpainted(id : int):
    try:
        if b[id-1] == '':
            return
        else:
            return FileResponse(b[id-1])
    except:
        return
    

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