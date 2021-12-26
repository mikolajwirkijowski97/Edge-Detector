import numpy as np
from numpy.fft import fft2, ifft2
from matplotlib import pyplot as plt
from PIL import Image, ImageOps
import sys
np.set_printoptions(threshold=sys.maxsize)

def padding(arr, xd, yd):
    h = arr.shape[0]
    w = arr.shape[1]
    a = (xd - h) // 2
    aa = xd - a - h
    b = (yd - w) // 2
    bb = yd - b - w
    return np.pad(arr, pad_width=((a, aa), (b, bb)), mode='constant')


# univariate normal distribution density
def dnorm(x, mu, sd):
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)


# using fft for 2d convolutions due to speed increase
def fft_convolution(f1, f2):
    print(f2)
    f2 = padding(f2, f1.shape[0], f1.shape[1])
    #print(f1)

    f1 = fft2(f1)

    f2 = fft2(np.flipud(np.fliplr(f2)))

    i, j = f1.shape
    cc = np.real(ifft2(f1 * f2))
    cc = np.roll(cc, -i / 2 + 1, axis=0)
    cc = np.roll(cc, -j / 2 + 1, axis=1)
    return cc


# create the kernel for gaussian blur convolutions
# basically creating a univariate normal distribution and transforming into 2d
# non-complicated doesnt call for much optimisation
def create_kernel(size):
    kernel_1d = np.linspace(-(size // 2), size // 2, size)
    sigma = np.sqrt(size)  # automatically set variance

    for i in range(size):
        kernel_1d[i] = dnorm(kernel_1d[i], 0, sigma)
    kernel = np.outer(kernel_1d.T, kernel_1d.transpose())

    kernel = np.divide(kernel, kernel.max())
    return kernel


def gaussian_blur(img, kernel_size):
    kernel = create_kernel(kernel_size)
    return np.asarray(fft_convolution(img, kernel))


img = Image.open("test.jpg")
img = ImageOps.grayscale(img)
data = np.asarray(img, dtype="int32")
plt.imread(gaussian_blur(np.asarray(img), 250))
plt.imshow()
