import numpy as np
from numpy.fft import fft2, ifft2
from numba import njit


def padding(arr, xd, yd):
    """
    :param arr: The array to be zero padded
    :param xd: The desired x dimension
    :param yd: the desired y dimension
    :return: A zero padded array with original content in the middle and of size == (xd,yd)

    """
    h = arr.shape[0]
    w = arr.shape[1]
    a = (xd - h) // 2
    aa = xd - a - h
    b = (yd - w) // 2
    bb = yd - b - w
    return np.pad(arr, pad_width=((a, aa), (b, bb)), mode='constant')


@njit
def dnorm(x, mu, sd):
    """

    :param x: the variable of the density function
    :param mu: the mu parameter
    :param sd: sigma/ standard deviation
    :return: result of the unm density function
    """
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)


# using fft for 2d convolutions due to speed increase

def fft_convolution(f1, f2):
    f1 = f1 / 255
    f2 = padding(f2, f1.shape[0], f1.shape[1])

    f1 = fft2(f1)
    f2 = fft2(np.flipud(np.fliplr(f2)))

    i, j = f1.shape
    cc = np.real(ifft2(f1 * f2))
    cc = np.roll(cc, -i // 2 + 1, axis=0)
    cc = np.roll(cc, -j // 2 + 1, axis=1)
    return cc


def _create_kernel(kernel_size):
    """
    :param kernel_size: size of the convolution kernel
    :return: the kernel
    """
    kernel_1d = np.linspace(-(kernel_size // 2), kernel_size // 2, kernel_size)
    # The square root of the kernel size seems to work well as the sigma
    sigma = np.sqrt(kernel_size)

    for i in range(kernel_size):
        kernel_1d[i] = dnorm(kernel_1d[i], 0, sigma)

    # Outer product of own transposition(Auto-correlation matrix)
    kernel = np.outer(kernel_1d.T, kernel_1d.T)

    kernel = np.divide(kernel, kernel.max())
    return kernel


def gaussian_blur(img, kernel_size):
    """
    :param img: 2d ndarray containing the image to be blurred
    :param kernel_size: The size of the convolution kernel
    :return: 2d ndarray containing the blurred image
    """
    kernel = _create_kernel(kernel_size)

    img_rgb = np.asarray(np.split(img, 3, axis=-1)).squeeze()
    rgb = [img_rgb[0], img_rgb[1], img_rgb[2]]
    for i in range(3):
        rgb[i] = fft_convolution(rgb[i], kernel)

    for i in range(3):
        rgb[i] = np.multiply(rgb[i], np.divide(255.0, rgb[i].max()))
    final_image = np.moveaxis(np.asarray(rgb), 0, -1).astype(np.uint8)

    return final_image
