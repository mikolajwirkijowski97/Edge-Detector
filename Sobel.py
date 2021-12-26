import numpy as np
from mathTools import fft_convolution, normalize
from scipy import signal


def sobel(img):
    """
    :param img: single channel 2d img as an ndarray
    :return: resulting image as an ndarray
    """
    threshold = 1
    # the mask to be applied over the image
    sobel_operator = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])

    result_a = signal.convolve2d(img, sobel_operator)

    result_b = signal.convolve2d(img, np.flip(sobel_operator.T, axis=0))

    result = np.sqrt(np.square(result_a) + np.square(result_b))
    return result

# TODO Implement some nice way to make it work on 3 color channels and then slap Canny on to that sobel
