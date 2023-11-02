import cv2
import numpy as np

import urllib
import numpy as np

import json

import requests

import io


fo = open("../GoogleMapAPIKey/key.txt", "r")

key = fo.read(39)

center = "51.514402,0.008026";

zoom = 15;

size = 400;



url = "https://maps.googleapis.com/maps/api/staticmap?"

url = (url + "center=" + center + "&zoom=" +
                   str(zoom) + "&size=" + str(size) + "x" + str(size) + "&format=jpg&key="+ key)


#response = requests.get(url)
#image_bytes = io.BytesIO(response.content)
#map = PIL.Image.open(image_bytes)

req = urllib.request.urlopen(url)
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
map = cv2.imdecode(arr, -1)

cv2.imshow("test",map)

cv2.waitKey(0)
cv2.destroyAllWindows()