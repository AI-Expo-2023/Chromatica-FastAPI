from io import BytesIO
from torch import autocast
from PIL import Image
import torch
from diffusers import StableDiffusionInpaintPipeline
import cv2 as cv

a = 'black'

init_path = './input/dog1.png'
mask_path = './input/dog2.png'

prompt = "a kungfu panda sitting on a bench"

with open(init_path, 'rb') as f:
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

image.save("cat_on_bench.png")

if a == 'original':
    pass
elif a == 'black':
    imageb_w = cv.imread("./cat_on_bench.png", cv.IMREAD_GRAYSCALE)
    cv.imshow('black', imageb_w)
    
    cv.imwrite('output/inpaint/grayImage.png', imageb_w)

elif a == 'ruddy':
    image1 = cv.imread("./cat_on_bench.png", cv.IMREAD_COLOR)
    b, g, r = cv.split(image1)
    image_ruddy = cv.merge((r, g, b))

    cv.imwrite('output/inpaint/ruddyImage.png', image_ruddy)

elif a == 'blue':
    image1 = cv.imread("./cat_on_bench.png", cv.IMREAD_COLOR)
    b, g, r = cv.split(image1)
    image_blue = cv.merge((b, b, r))

    cv.imwrite('output/inpaint/blueImage.png', image_blue)
