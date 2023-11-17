from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2
import urllib
import requests
import textwrap

from GoogleMapAPI import *
from CoordinateTransform import *

Photo = Image.open("TEST.jpg").convert("RGBA")
Photo_Copy = Image.open("TEST.jpg")
exif = Photo_Copy._getexif()


image_x = Photo.size[0]
image_y = Photo.size[1]


Border_Ratio = [0.0,0.0,0.0,0.135]
Border_Pixel = [int(image_y*Border_Ratio[0]),int(image_x*Border_Ratio[1]),int(image_x*Border_Ratio[2]),int(image_y*Border_Ratio[3])]

Frame_x = image_x+Border_Pixel[1]+Border_Pixel[2]
Frame_y = image_y+Border_Pixel[0]+Border_Pixel[3]

Frame = Image.new("RGBA", (Frame_x, Frame_y), (255, 255, 255))

Latitude,Longitude,CoordinateStr = coordinate_transform(exif[34853])

#map= google_static_map(Latitude,Longitude,Border_Pixel[3],12)
city_country = google_adress(Latitude,Longitude)

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

fontsize_L = int(Border_Pixel[3]*0.3)
fontsize_M = int(Border_Pixel[3]*0.2)

myFont = ImageFont.truetype('SmileySans-Oblique.ttf', fontsize_L)
DateFont = ImageFont.truetype('SmileySans-Oblique.ttf', fontsize_M)

LensModel = ImageDraw.Draw(Frame)

LensModel.text((Border_Pixel[1]+Border_Pixel[3]/6, Frame_y-Border_Pixel[3]*0.9), exif_s["LensModel"], font=myFont, fill=(0, 0, 0))

Model = ImageDraw.Draw(Frame)

Model.text((Border_Pixel[1]+Border_Pixel[3]/6, Frame_y-Border_Pixel[3]*0.5), exif_s["Make"]+"  "+exif_s["Model"], font=myFont, fill=(160, 160, 160))

DateTime = ImageDraw.Draw(Frame)

DateTime.text((Frame_x-Border_Pixel[2]-Border_Pixel[3]/8, Frame_y-Border_Pixel[3]*0.5), exif_s["DateTime"],anchor="rs", font=DateFont, fill=(160, 160, 160))

City_Country = ImageDraw.Draw(Frame)

City_Country.text((Frame_x-Border_Pixel[2]-Border_Pixel[3]/8, Frame_y-Border_Pixel[3]*0.2), city_country,anchor="rs", font=DateFont, fill=(0, 0, 0))


Frame = Frame.resize((Frame_x,Frame_y), Image.Resampling.LANCZOS)

Frame.paste(Photo, (Border_Pixel[1], Border_Pixel[0]), Photo)

#Frame.paste(map, (Frame_x-Border_Pixel[3], Frame_y-2*Border_Pixel[3]), map)

numpy_image = cv2.cvtColor(np.array(Frame), cv2.COLOR_RGB2BGR)



cv2.imshow("Modified Image", numpy_image)
cv2.waitKey(0)
cv2.destroyAllWindows()