from matplotlib import pyplot as plt
from PIL import Image, ImageOps
import numpy as np
from GaussianBlur import gaussian_blur
### przykład użycia

# wczytaj obraz
img = Image.open("test.jpg")
# zamień na numpy array
img = np.asarray(img)
print(type(img))
# użyj funkcji gaussian_blur
blur_kernel_size = 150
img = gaussian_blur(img, kernel_size=blur_kernel_size)

# zmień spowrotem tablice na obraz i go pokaż
pillow_image = Image.fromarray(img)
pillow_image.show()