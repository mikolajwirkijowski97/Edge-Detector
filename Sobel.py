import numpy as np
from mathTools import fft_convolution, normalize
from scipy import signal


def sobel(img):
    """

    Performs the basic sobel algorithm

    :param img: single channel 2d img as an ndarray
    :return: resulting image as an ndarray and gradient direction for the canny filtering operation
    """
    threshold = 1
    # the mask to be applied over the image
    sobel_operator = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]).astype(np.float32)

    result_a = fft_convolution(img, sobel_operator)

    result_b = fft_convolution(img, np.flip(sobel_operator.T, axis=0))

    result = np.sqrt(np.square(result_a) + np.square(result_b))

    gradient_direction = np.rad2deg(np.arctan2(result_a, result_b)) + 180
    return result, gradient_direction
