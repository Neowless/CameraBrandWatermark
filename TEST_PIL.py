from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2
import urllib
import requests

Photo = Image.open("TEST.jpg").convert("RGBA")
Photo_Copy = Image.open("TEST.jpg")
exif = Photo_Copy._getexif()

image_x = Photo.size[0]
image_y = Photo.size[1]

print(image_x)

Border_Ratio = [0.01,0.01,0.01,0.15]
Border_Pixel = [int(image_y*Border_Ratio[0]),int(image_x*Border_Ratio[1]),int(image_x*Border_Ratio[2]),int(image_y*Border_Ratio[3])]

Frame_x = image_x+Border_Pixel[1]+Border_Pixel[2]
Frame_y = image_y+Border_Pixel[0]+Border_Pixel[3]

Frame = Image.new("RGBA", (Frame_x, Frame_y), (255, 255, 255));

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

fo = open("../GoogleMapAPIKey/key.txt", "r")

key = fo.read(39)

center = str(Latitude)+","+str(Longitude);

zoom = 15;

size = 400;



url = "https://maps.googleapis.com/maps/api/staticmap?"

url = (url + "center=" + center + "&zoom=" +
                   str(zoom) + "&size=" + str(size) + "x" + str(size) + "&format=jpg&key="+ key)


req = urllib.request.urlopen(url)

arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

arr = cv2.imdecode(arr, -1)

arr = Image.fromarray(cv2.cvtColor(arr,cv2.COLOR_BGR2RGBA))


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

myFont = ImageFont.truetype('SmileySans-Oblique.ttf', Border_Pixel[3]*0.3)
DateFont = ImageFont.truetype('SmileySans-Oblique.ttf', Border_Pixel[3]*0.2)

LensModel = ImageDraw.Draw(Frame)

LensModel.text((Border_Pixel[1]+Border_Pixel[3]/6, Frame_y-Border_Pixel[3]*0.9), exif_s["LensModel"], font=myFont, fill=(0, 0, 0))

Model = ImageDraw.Draw(Frame)

Model.text((Border_Pixel[1]+Border_Pixel[3]/6, Frame_y-Border_Pixel[3]*0.5), exif_s["Make"]+"  "+exif_s["Model"], font=myFont, fill=(160, 160, 160))

DateTime = ImageDraw.Draw(Frame)

DateTime.text((Frame_y-Border_Pixel[2]-1000, Frame_y-Border_Pixel[3]*0.5), exif_s["DateTime"], font=DateFont, fill=(160, 160, 160))


Frame = Frame.resize((Frame_x,Frame_y), Image.Resampling.LANCZOS)

Frame.paste(Photo, (Border_Pixel[1], Border_Pixel[0]), Photo)

Frame.paste(arr, (Border_Pixel[1], Border_Pixel[0]), arr)

numpy_image = cv2.cvtColor(np.array(Frame), cv2.COLOR_RGB2BGR)
# Display the image using OpenCV's imshow function
cv2.imshow("Modified Image", numpy_image)
cv2.waitKey(0)
cv2.destroyAllWindows()