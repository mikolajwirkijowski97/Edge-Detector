import numpy as np
from mathTools import dnorm, fft_convolution


def _create_kernel(kernel_size):
    """
    :param kernel_size: size of the convolution kernel
    :return: the gaussian distribution kernel
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


def gaussian_blur(img, kernel_size=15):
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
        rgb[i] = np.multiply(rgb[i], np.divide(1, rgb[i].max()))

    final_image = np.moveaxis(np.asarray(rgb), 0, -1).astype(np.float32)

    return final_image
