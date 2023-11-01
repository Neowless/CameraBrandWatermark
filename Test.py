import cv2
import numpy as np

import PIL.Image
import PIL.ExifTags


img = PIL.Image.open('TEST.JPG')
exif = img._getexif()

Coordinate = exif[34853][2][1]

print(Coordinate)

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



image = cv2.imread('TEST4.jpg')

imagesize = image.shape


image_x = imagesize[1]
image_y = imagesize[0]

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



cv2.imshow('3 Channel Window', Frame)

cv2.waitKey(0)
cv2.destroyAllWindows()