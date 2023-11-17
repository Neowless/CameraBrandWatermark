import numpy as np
import cv2
from skimage.color import rgb2lab
from scipy.spatial import distance
def convert_to_yuv(raw_rgb):
    yuv = np.array([[0.299, 0.587, 0.114],
                    [-0.14713, -0.28886, 0.436],
                    [0.615, -0.51499, -0.10001]])
    yuv_result = np.dot(yuv, raw_rgb)
    return yuv_result


def yuv_to_rgb(YUV):
    Y = YUV[0]
    U = YUV[1]
    V = YUV[2]
    R = Y + 1.402 * (V - 128)
    G = Y - 0.344136 * (U - 128) - 0.714136 * (V - 128)
    B = Y + 1.772 * (U - 128)
    return [R, G, B]
# Define the YUV color values


def dominant_colors_new(pixel_array, threshold=0.1, n=1, num_threshold=0.2, filter_color=None, filter_threshold=0.5):
    pixel_array_lab = rgb2lab(pixel_array)
    pixel_list = pixel_array_lab.reshape(-1, 3)
    def color_distance(c1, c2):
        return distance.euclidean(c1, c2)
    buckets = []
    for pixel in pixel_list:
        found_bucket = False
        for bucket in buckets:
            if color_distance(pixel, bucket[0]) < threshold:
                bucket.append(pixel)
                found_bucket = True
                break
        if not found_bucket:
            buckets.append([pixel])
    if filter_color is not None:
        buckets = [bucket for bucket in buckets if color_distance(np.mean(bucket, axis=0), filter_color) > filter_threshold]
    buckets = sorted(buckets, key=lambda x: len(x), reverse=True)
    if len(buckets) == 0:
        return []
    output = [np.mean(buckets[0], axis=0)]
    previous = output[0]
    for i in range(n-1):
        if len(buckets) == 0:
            return output
        while color_distance(np.mean(buckets[0], axis=0), previous) < num_threshold:
            if len(buckets) != 0:
                buckets.pop(0)
            else:
                return output
        output.append(np.mean(buckets[0], axis=0))
        previous = output[-1]
    return output

image = cv2.imread('SSF.jpeg')
# Determine the shorter side length
height, width = image.shape[:2]
short_side = min(height, width)
# Calculate the scaling factor
scale_factor = 36 / short_side
# Resize the image
resized_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
# Apply the Bilateral Filter
filtered_image = cv2.bilateralFilter(resized_image, 1, 0.2, 2)

yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)

# Display the result
TopPixelArray = yuv_image[0,:]
LeftPixelArray = yuv_image[:,0]
BottomPixelArray = yuv_image[-1,:]
RightPixelArray = yuv_image[:,-1]

dc = dominant_colors_new(BottomPixelArray,threshold=0.1,n=1,num_threshold=0.2,filter_color=None,filter_threshold=0.5)


dc = dc[0]


dc = [value + 255 if value < 0 else value for value in dc]


dc = yuv_to_rgb(dc)

dc[0] = int(dc[0])
dc[1] = int(dc[1])
dc[2] = int(dc[2])

dc = [value - value if value < 0 else value for value in dc]

print(dc)

rgb_color = np.array([dc[2],dc[1],dc[0]], dtype=np.uint8)
# Convert YUV to RGB

colourimage = np.full((400,600,3), rgb_color, dtype=np.uint8)  # Image size: 400x600
# Display the image
cv2.imshow('Pure Color Image', colourimage)
cv2.waitKey(0)
cv2.imshow('Pure Color Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()