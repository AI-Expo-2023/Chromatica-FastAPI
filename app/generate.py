from fastapi import APIRouter, status, Form, HTTPException
from fastapi.responses import FileResponse
import subprocess as sub
from googletrans import Translator
import os, time, base64, time
from optimizedSD import inpaint
import sqlite3

# 디비에서 저장된 이미지 경로 조회
conn = sqlite3.connect('./database/ImageURL.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()

translator = Translator()
prompt = APIRouter()

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
    path = './input/inpaint/base_image'
   
    content_byte = str.encode(file)
    content = base64.b64decode(content_byte)
    
    with open(os.path.join(path, filename), 'w+b') as fp:
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
    
    id_list = [0, 0, 0, 0]

    prompt = translator.translate(keyword, dest='en').text
    base_path = await save_img2img_img(base_img)

    cmd = ['python', './optimizedSD/img2img.py', '--prompt', f'{prompt}', '--W', 
            f'{int(W)}', '--H', f'{int(H)}', '--ddim_steps', f'{int(steps)}', '--format', 
            f'{format}', '--n_samples', f'{int(samples)}', '--init-img', f'{base_path}', '--turbo']
    sub.run(cmd)

    for i in range(int(samples)):
        path = str(c.execute(f'SELECT path FROM images WHERE id = (SELECT (MAX(id) - {i}) from images)').fetchall())
        id_list[i] = str(c.execute(f'SELECT id from images where path=(?)', (path.replace("['", "").replace("']", ""),)).fetchall())
        id_list[i] = id_list[i].replace('[', '').replace(']', '')
    
    return [f'http://192.168.0.113:3333/generated_img2img/{int(id_list[0])}', f'http://192.168.0.113:3333/generated_img2img/{int(id_list[1])}',
            f'http://192.168.0.113:3333/generated_img2img/{int(id_list[2])}', f'http://192.168.0.113:3333/generated_img2img/{int(id_list[3])}']


@prompt.post('/inpaint/keyword', status_code=status.HTTP_200_OK)
async def get_prompt(base_img: str = Form(), mask_img: str = Form(), 
                     keyword: str = Form(), steps: str = Form(), style : str = Form(), W: str = Form(), H: str = Form()):
    
    global b
    global inpaint_id
    prompt = translator.translate(keyword, dest='en').text

    base_path = await save_base_img(base_img)
    mask_path = await save_mask_img(mask_img)

    inpaint.main(style=style, base_path=base_path, mask_path=mask_path, prompt=prompt, W=W, H=H)

    b = str(c.execute(f'SELECT path FROM images WHERE id = (SELECT MAX(id) from images)').fetchall())
    inpaint_id = str(c.execute(f'SELECT id from images where path=(?)', (b.replace("['", "").replace("']", ""),)).fetchall())
    inpaint_id = inpaint_id.replace('[', '').replace(']', '')

    return f'http://192.168.0.113:3333/generated_inpaint/{int(inpaint_id)}'


@prompt.get('/generated_img2img/{id}')
async def get_image_img2img(id : int):
    try:
        if id == 0:
            raise HTTPException(status_code=404, detail="Image not found")
        else:
            a = c.execute(f'SELECT path FROM images WHERE id = (SELECT {id} from images)').fetchall()
            return FileResponse(str(a).replace("[", '').replace(']', '').replace("'", ""))
    except:
        raise HTTPException(status_code=404, detail="Image not found")


@prompt.get('/generated_inpaint/{id}')
async def get_image_inpainted(id : int):
    a = c.execute(f'SELECT path FROM images WHERE id = (SELECT {id} from images)').fetchall()
    return FileResponse(str(a).replace("[", '').replace(']', '').replace("'", ""))
