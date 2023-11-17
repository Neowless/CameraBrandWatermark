from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2
import urllib
import requests


def google_key():
    fo = open("../GoogleMapAPIKey/key.txt", "r")
    key = fo.read(39)
    return(key)


def google_static_map(latitude,longitude,pixel,zoom):
    key = google_key()
    center = str(latitude) + "," + str(longitude)
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    url = (url + "center=" + center + "&zoom=" +
           str(zoom) + "&size=" + str(pixel) + "x" + str(pixel) + "&format=jpg&scale=2&key=" + key + "&map_id=8d90c5094c59ea2f" )
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    arr = cv2.imdecode(arr, -1)
    map = Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_BGR2RGBA))
    return(map)


def google_city_country(latitude,longitude):
    key = google_key()
    center = str(latitude) + "," + str(longitude)
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
    url = (url + center + "&key=" + key)
    try:
        response = requests.get(url,timeout=5)
        json_data = response.json()
        city = json_data["results"][0]["address_components"][3]["long_name"]
        country = json_data["results"][0]["address_components"][4]["long_name"]
        return(city + ", " + country)
    except:
        return("")
    # response = requests.get(url)
    # json_data = response.json()
    # adress = json_data["results"][00]["formatted_address"]
    # adress = adress.replace(",", "-")
    # return(adress)


def google_address(latitude,longitude):
    key = google_key()
    center = str(latitude) + "," + str(longitude)
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
    url = (url + center + "&key=" + key)
    try:
        response = requests.get(url)
        json_data = response.json()

        number = len(json_data["results"])
        counter = 0
        adress_list = []
        while counter < number:
            adress_list += [json_data["results"][counter]["formatted_address"]]
            counter += 1
        return(adress_list)
    except:
        return("")


def google_elevation(latitude,longitude):
    key = google_key()
    center = str(latitude) + "," + str(longitude)
    url = "https://maps.googleapis.com/maps/api/elevation/json?locations="
    url = (url + center + "&key=" + key)
    try:
        response = requests.get(url,timeout=5)
        json_data = response.json()
        elevation = json_data["results"][0]["elevation"]
        return(elevation)
    except:
        return(0)


#https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&key=AIzaSyBsVTSl9_9chsjPDEPd_xziG2V02AfH5II
