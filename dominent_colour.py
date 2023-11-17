import cv2
import numpy as np
def dominent_colour(imagepath,colour_number,EDGE):
    image = cv2.imread(imagepath)
    # Determine the shorter side length
    height, width = image.shape[:2]
    short_side = min(height, width)
    # Calculate the scaling factor
    scale_factor = 200 / short_side
    # Resize the image
    img = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)

    img = cv2.bilateralFilter(img, 1, 0.2, 2)

    TopPixelArray = img[0, :]
    LeftPixelArray = img[:, 0]
    BottomPixelArray = img[-1, :]
    RightPixelArray = img[:, -1]

    EdgePixelArray = np.vstack((TopPixelArray, LeftPixelArray, BottomPixelArray, RightPixelArray))

    height, width, _ = np.shape(img)
    # print(height, width)

    if EDGE == True:
        data = EdgePixelArray
    else:
        data = np.reshape(img, (height * width, 3))
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(data, colour_number, None, criteria, 10, flags)

    centers = [row[::-1] for row in centers]

    centers = [[int(element) for element in row] for row in centers]
    return centers




