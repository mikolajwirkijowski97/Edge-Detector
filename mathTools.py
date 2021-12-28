# using fft for 2d convolutions due to speed increase
from numpy.fft import fft2, ifft2
import numpy as np
from PIL import Image
from numba import jit


# normalize 0 to 1
def normalize(arr):
    return (arr - np.min(arr)) / np.ptp(arr)


def dnorm(x, mu, sd):
    """
    :param x: the variable of the density function
    :param mu: the mu parameter
    :param sd: sigma/ standard deviation
    :return: result of the unm density function
    """
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)


@jit(parallel=True)
def fft_convolution(f1, f2):
    """
    :param f1: 2d array to be convolved
    :param f2: convolution kernel
    :return: convolution result
    """

    # extending old dimensions from N to 2N according to convolution theory
    old_dx, old_dy = f1.shape[0], f1.shape[1]
    new_dx, new_dy = old_dx * 2, old_dy * 2
    f1 = padding(f1, new_dx, new_dy)
    f2 = padding(f2, new_dx, new_dy)

    # apply fourier transformation to f1(our image) and to the mirror image of f2(mirroring could be deleted
    # for use in gaussian blur as a minor optimisation)
    f1 = fft2(f1)
    f2 = fft2(np.flipud(np.fliplr(f2)))
    i, j = f1.shape
    # retrieve the real part of the product  of transformed matrices
    cc = np.real(ifft2(f1 * f2))
    # convolution theory magic ¯\_(ツ)_/¯
    cc = np.roll(cc, -i // 2 + 1, axis=0)
    cc = np.roll(cc, -j // 2 + 1, axis=1)
    # bring back old dimensions
    cc = cc[old_dx // 2:new_dx - old_dx // 2, old_dy // 2:new_dy - old_dy // 2]
    return cc


@jit(forceobj=True)
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


def arr_to_img(arr):
    """
    :param arr: 0-1 scaled array
    :return:
    """
    return Image.fromarray((arr * 255).astype(np.uint8))