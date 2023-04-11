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

    with open(os.path.join(path, filename), "w+b") as fp:
        fp.write(content)

    if style == 'original':
        pass
    elif style == 'black':
        imageb_w = cv.imread("./cat_on_bench.png", cv.IMREAD_GRAYSCALE)
        cv.imshow('black', imageb_w)
        
        cv.imwrite(f'/output/inpaint/{filename}.png', imageb_w)

    elif style == 'ruddy':
        image1 = cv.imread("./cat_on_bench.png", cv.IMREAD_COLOR)
        b, g, r = cv.split(image1)
        image_ruddy = cv.merge((r, g, b))

        cv.imwrite(f"/output/inpaint/{filename}.png", image_ruddy)

    elif style == 'blue':
        image1 = cv.imread("./cat_on_bench.png", cv.IMREAD_COLOR)
        b, g, r = cv.split(image1)
        image_blue = cv.merge((b, b, r))

        cv.imwrite(f"/output/inpaint/{filename}.png", image_blue)