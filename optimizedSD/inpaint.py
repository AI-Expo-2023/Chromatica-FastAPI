from io import BytesIO
from torch import autocast
from PIL import Image
import torch
from diffusers import StableDiffusionInpaintPipeline
import cv2 as cv
import time
import os

a = time.strftime("%Y-%m-%d-%H-%M-%S")
path = './output/inpaint'
filename = f"{str(a)}.png"

def main(style, base_path, mask_path, prompt):
    with open(base_path, 'rb') as f:
        init_data = f.read()

    with open(mask_path, 'rb') as f:
        mask_data = f.read()


    init = Image.open(BytesIO(init_data))
    mask = Image.open(BytesIO(mask_data))

    device = "cuda"
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        revision="fp16", 
        torch_dtype=torch.float16
    ).to(device)

    with autocast("cuda"):
        image = pipe(prompt=prompt, image=init, mask_image=mask, strength=0.75).images[0]

    content = image
    content.save(f"{path}/{filename}","PNG")

    if style == 'original':
        pass

    elif style == 'black':
        content = cv.imread(f"{path}/{filename}", cv.IMREAD_GRAYSCALE)
        cv.imshow('black', content)
        
        cv.imwrite(f'{path}/{filename}', content)

    elif style == 'ruddy':
        content = cv.imread(f"{path}/{filename}", cv.IMREAD_COLOR)
        b, g, r = cv.split(content)
        image_ruddy = cv.merge((r, g, b))

        cv.imwrite(f"{path}/{filename}", image_ruddy)

    elif style == 'blue':
        content = cv.imread(f"{path}/{filename}", cv.IMREAD_COLOR)
        b, g, r = cv.split(content)
        image_blue = cv.merge((b, b, r))

        cv.imwrite(f"{path}/{filename}", image_blue)

    return f"{path}/{filename}"