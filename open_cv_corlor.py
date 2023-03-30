import cv2
import numpy as np
import json

image = cv2.imread("test.jpg",cv2.IMREAD_COLOR)
image_black_white = cv2.imread("test.jpg",cv2.IMREAD_GRAYSCALE)
b, g, r = cv2.split(image)

w = 600
h = 700
point = (w,h)

height, width, channel = image.shape
zero1 = np.zeros((height, width, 2), dtype=np.uint8)
image_red = cv2.merge((g, g, r))
image_blue = cv2.merge((g, r, zero1))

image_black_white = cv2.resize(image_black_white, point,interpolation= cv2.INTER_LINEAR)
image_red = cv2.resize(image_red, point, interpolation= cv2.INTER_LINEAR)
image_blue = cv2.resize(image_blue, point, interpolation= cv2.INTER_LINEAR)
image = cv2.resize(image, point, interpolation= cv2.INTER_LINEAR)
cv2.imshow('original',image)
cv2.waitKey()
cv2.imshow("gray",image_black_white)
cv2.waitKey()
cv2.imshow('red',image_red)
cv2.waitKey()
cv2.imshow('blue',image_blue)
cv2.waitKey()
cv2.destroyAllWindows()
