from matplotlib import pyplot as plt
from PIL import Image, ImageOps
import numpy as np
from GaussianBlur import gaussian_blur
from Sobel import sobel





### przykład użycia

# wczytaj obraz
img = Image.open("test.jpg")
# zamień na numpy array w skali 0-1
img = np.asarray(img) / 255
softer_image = gaussian_blur(img, 6)
arr_to_img(softer_image).show()

edge = sobel(np.asarray(np.split(softer_image, 3, axis=-1)).squeeze()[2])
arr_to_img(edge).show()

# zmień spowrotem tablice na obraz i go pokaż
