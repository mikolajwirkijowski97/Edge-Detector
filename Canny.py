import numpy as np
from Sobel import sobel
from GaussianBlur import gaussian_blur
from mathTools import arr_to_img, normalize
from PIL import Image, ImageOps

PI = 180


def non_max_suppresion(gradient_magnitude, gradient_direction):
    x, y = gradient_magnitude.shape
    out = np.zeros((x, y))
    for row in range(1, x - 1):
        for col in range(1, y - 1):
            direction = gradient_direction[row, col]
            if (0 <= direction < PI / 8) or (15 * PI / 8 <= direction <= 2 * PI):
                before_pixel = gradient_magnitude[row, col - 1]
                after_pixel = gradient_magnitude[row, col + 1]

            elif (PI / 8 <= direction < 3 * PI / 8) or (9 * PI / 8 <= direction < 11 * PI / 8):
                before_pixel = gradient_magnitude[row + 1, col - 1]
                after_pixel = gradient_magnitude[row - 1, col + 1]

            elif (3 * PI / 8 <= direction < 5 * PI / 8) or (11 * PI / 8 <= direction < 13 * PI / 8):
                before_pixel = gradient_magnitude[row - 1, col]
                after_pixel = gradient_magnitude[row + 1, col]

            else:
                before_pixel = gradient_magnitude[row - 1, col - 1]
                after_pixel = gradient_magnitude[row + 1, col + 1]

            if gradient_magnitude[row, col] >= before_pixel and gradient_magnitude[row, col] >= after_pixel:
                out[row, col] = gradient_magnitude[row, col]
    return out


def threshold(image, low, high, weak):
    output = np.zeros(image.shape)
    strong = 1

    strong_row, strong_col = np.where(image >= high)
    weak_row, weak_col = np.where((image <= high) & (image >= low))

    output[strong_row, strong_col] = strong
    output[weak_row, weak_col] = weak
    return output


def canny_edge_detection(img, low_mag, low, high):
    blurred = gaussian_blur(img, 9)

    split = np.asarray(np.split(blurred, 3, axis=-1)).squeeze()

    grad_mag_r, grad_dir_r = sobel(split[0])
    grad_mag_g, grad_dir_g = sobel(split[1])
    grad_mag_b, grad_dir_b = sobel(split[2])

    # combine all 3 channells

    # combined sobel gradient magnitude output
    combined_magnitude = np.divide(grad_mag_r + grad_mag_g + grad_mag_b, 2)
    # combined sobel gradient direction output
    combined_direction = np.divide(grad_dir_r + grad_dir_g + grad_dir_b, 3)

    # Non-max suppresion for the sobel output
    transformed_image = normalize(non_max_suppresion(combined_magnitude, combined_direction))

    # Threshold applied to delete useless edges
    threshed = threshold(transformed_image, low, high, weak=low_mag)

    return threshed
