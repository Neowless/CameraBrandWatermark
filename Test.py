import cv2
import numpy as np


import TEST_PIL.Image
import TEST_PIL.ExifTags

import urllib
import numpy as np

import requests

import io


filename = 'TEST.JPG'

img = PIL.Image.open(filename)
exif = img._getexif()

Coordinate = exif[34853]

if Coordinate[1] == "N":
    print("N")
    Latitude = Coordinate[2][0]+Coordinate[2][1]/60+Coordinate[2][2]/3600
else:
    print("S")
    Latitude = -Coordinate[2][0] + Coordinate[2][1]/60 + Coordinate[2][2] / 3600

if Coordinate[3] == "N":
    print("N")
    Longitude = Coordinate[4][0]+Coordinate[4][1]/60+Coordinate[4][2]/3600
else:
    print("S")
    Longitude = -Coordinate[4][0] + Coordinate[4][1] / 60 + Coordinate[4][2] / 3600

    Latitude = float(Latitude)
    Longitude = float(Longitude)

print(Latitude)
print(Longitude)



exif_s = {
    "Make":exif[271],
    "Model":exif[272],
    "DateTime":exif[36867],
    "ExposureTime":exif[33434],
    "Aperture":exif[33437],
    "ISO":exif[34855],
    "FocalLength":exif[37386],
    "LensMake":exif[42035],
    "LensModel":exif[42036],
    "XResolution":exif[282],
    "35mmFocalLength":exif[41989],
}


print(exif_s)



image = cv2.imread(filename)

imagesize = image.shape


image_x = imagesize[1]
image_y = imagesize[0]

print(image_x)

'''
---------Border1-------
Border2---IMG---Border3
---------Border4-------
'''


Border_Ratio = [0.05,0.05,0.05,0.15]
Border_Pixel = [int(image_y*Border_Ratio[0]),int(image_x*Border_Ratio[1]),int(image_x*Border_Ratio[2]),int(image_y*Border_Ratio[3])]

Frame_x = image_x+Border_Pixel[1]+Border_Pixel[2]
Frame_y = image_y+Border_Pixel[0]+Border_Pixel[3]


Border_1 = np.zeros([Border_Pixel[0],Frame_x,3],dtype=np.uint8)
Border_1.fill(255)

Border_2 = np.zeros([image_y,Border_Pixel[1],3],dtype=np.uint8)
Border_2.fill(255)

Border_3 = np.zeros([image_y,Border_Pixel[2],3],dtype=np.uint8)
Border_3.fill(255)

Border_4 = np.zeros([Border_Pixel[3],Frame_x,3],dtype=np.uint8)
Border_4.fill(255)


Frame = cv2.hconcat([Border_2,image,Border_3])

Frame = cv2.vconcat([Border_1,Frame,Border_4])

font = cv2.FONT_HERSHEY_SIMPLEX
org = (100,5500, )
font_scale = 20
color = (0, 0, 0)
thickness = 40
line_type = cv2.LINE_AA
# Put text on the image
cv2.putText(Frame, 'Hack Projects', org, font, font_scale, color, thickness, line_type)
# Display the image using OpenCV

cv2.imshow('3 Channel Window', Frame)

cv2.waitKey(0)
cv2.destroyAllWindows()

