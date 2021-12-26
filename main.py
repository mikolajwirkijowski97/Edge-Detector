from matplotlib import pyplot as plt
from PIL import Image, ImageOps
import numpy as np
from GaussianBlur import gaussian_blur
from Sobel import sobel
from mathTools import arr_to_img

# Load image using PIL
img = Image.open("test.jpg")
# Transform from uint8 to float
img = np.asarray(img) / 255

# Apply Gaussian blur
softer_image = gaussian_blur(img, 3)
arr_to_img(softer_image).show()

# Apply Sobel filter to currently single color channell of the image
edge = sobel(np.asarray(np.split(softer_image, 3, axis=-1)).squeeze()[2])

# Show result
arr_to_img(edge).show()

