from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,QGraphicsScene, QGraphicsView,
                               QFileDialog,QGraphicsPixmapItem,QGraphicsRectItem,QGraphicsTextItem,QLineEdit)
from PySide6.QtGui import (QPixmap, QColor, QBrush, QPainter, QPen, QPalette, QTransform, QFont, QFontDatabase
,QFontMetrics,QImageReader,QIcon)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile ,Qt, QResource,QDir
from sys import platform
import subprocess
import re
import os
import math
import requests
import json
from MathTool import *
from ImageProcessingTool import *
from StrProcessingTool import *

from CoordinateTransform import *
from GoogleMapAPI import *
from dominent_colour import *
from Rendering import *

from PIL import Image, ImageFont, ImageDraw

image_data = None
PhotoPixmap = None
PhotoItem = None
BottomBorderItem = None
TopBorderItem = None
LeftBorderItem = None
RightBorderItem = None
exif = None
myFont = None
text_item_1 = None
text_item_2 = None
text_item_3 = None
text_item_4 = None
TestRectItem = None
exif_s = None
scene = None
tt_Rect = None
text1_content = "Lens Model"
text2_content = "Camera Make and Model"
image_scale = 1

# Resolution of Target Image
image_x = 0
image_y = 0

# Position and Size of the Bottom Border
Bottom_Border_Pos = [0,0]
Bottom_Border_Size = [0,0]
ImagePos = [0,0]

font_weights = ["Thin", "ExtraLight", "Light", "Normal", "Medium", "DemiBold", "Bold", "ExtraBold", "Black"]

CoordinateStr = ""
addressStr =""
TextItems = ["Camera Make and Model", "Camera Make", "Camera Model",
             "Lens Make and Model", "Lens Make", "Lens Model", "Parameters",
             "Date and Time", "Coordinates", "Coordinates (DMS)", "Address", "Elevation", "User Content 1",
             "User Content 2", "User Content 3", "User Content 4","None"]
config = None

UserContext = ["","","",""]


class Stats(QMainWindow):
    def __init__(self):
        # Load the UI File
        super().__init__()
        qfile_stats = QFile("UI/Test.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui = QUiLoader().load(qfile_stats)

        # Set the limitation of the memory allocation
        QImageReader.setAllocationLimit(0)
        Image.MAX_IMAGE_PIXELS = 933120000

        # Check the System Appearance
        is_dark_mode = self.check_appearance()
        if is_dark_mode:
            self.ui.preview.setStyleSheet("background-color: rgba(255, 255, 255, 0);border-color: rgba(193,193,193, 255)"
                                          ";border-width : 3px;border-style: solid;")
        else:
            self.ui.preview.setStyleSheet("background-color: rgba(255, 255, 255, 0);border-color: rgba(102,102,102, 255)"
                                          ";border-width : 3px;border-style: solid;")

        # Load the default config file
        self.load_json_file('defaultConfig.json')

        # Load the font and weight from resources\fonts
        folder_path = "resources/fonts"
        file_names = os.listdir(folder_path)
        ttf_files = [file_name for file_name in file_names if file_name.endswith(".ttf")]
        ttf_files = sorted(ttf_files, key=lambda x: x[0])
        counter = 0
        for ttf_file in ttf_files:
            ttf_file = os.path.splitext(ttf_file)[0]
            self.ui.Font_Selection.addItem(ttf_file)
            sysFont = QFont()
            id = QFontDatabase.addApplicationFont(os.path.dirname(__file__) + "/resources/fonts/"+ttf_file+".ttf")
            familyStr = QFontDatabase.applicationFontFamilies(id)[0]
            sysFont.setFamily(familyStr)
            self.ui.Font_Selection.setItemData(counter, sysFont, role=Qt.FontRole)
            counter += 1
        for font_weight in font_weights:
            self.ui.Font_Weight.addItem(font_weight)

        # Initialize the Border Ratio Text
        self.ui.Border_Ratio_Text.setText(validate_ratio_json(config["BorderRatio"]))
        self.ui.Border_Ratio_Equal_Text.setText(validate_euqla_ratio_json(config["BorderRatioEqual"]))
        if config["EqualBorder"]:
            self.ui.Border_Ratio_Text.setReadOnly(True)
            self.ui.Border_Ratio_Equal_Text.setReadOnly(False)
            self.ui.BorderRatioType.setCheckState(Qt.Checked)
        else:
            self.ui.Border_Ratio_Text.setReadOnly(False)
            self.ui.Border_Ratio_Equal_Text.setReadOnly(True)
            self.ui.BorderRatioType.setCheckState(Qt.Unchecked)

        # Initialized the Font and Weight
        FontName = FontFamilyName2FileName(config["Font"])
        self.ui.Font_Selection.setCurrentText(FontName)
        self.ui.Font_Weight.setCurrentText(config["FontWeight"])

        # Initialize the Text Items Combobox
        self.ui.Text1_Content.addItems(TextItems)
        self.ui.Text1_Content.setCurrentText(config["Arrangement"]["TextContent_1"])
        self.ui.Text2_Content.addItems(TextItems)
        self.ui.Text2_Content.setCurrentText(config["Arrangement"]["TextContent_2"])
        self.ui.Text3_Content.addItems(TextItems)
        self.ui.Text3_Content.setCurrentText(config["Arrangement"]["TextContent_3"])
        self.ui.Text4_Content.addItems(TextItems)
        self.ui.Text4_Content.setCurrentText(config["Arrangement"]["TextContent_4"])
        self.ui.Text1_Content.currentTextChanged.connect(self.Change_Text1_Content)
        self.ui.Text2_Content.currentTextChanged.connect(self.Change_Text2_Content)
        self.ui.Text3_Content.currentTextChanged.connect(self.Change_Text3_Content)
        self.ui.Text4_Content.currentTextChanged.connect(self.Change_Text4_Content)

        # Initialize the Text Colour Text Box
        self.ui.Background_Colour.setMaxLength(17)
        self.ui.Text1_Colour.setMaxLength(17)
        self.ui.Text2_Colour.setMaxLength(17)
        self.ui.Text3_Colour.setMaxLength(17)
        self.ui.Text4_Colour.setMaxLength(17)
        self.ui.Background_Colour.setText(RGBA2String(config["BackgroundColour"]))
        self.ui.Text1_Colour.setText(RGBA2String(config["TextColour"]["TextColour_1"]))
        self.ui.Text2_Colour.setText(RGBA2String(config["TextColour"]["TextColour_2"]))
        self.ui.Text3_Colour.setText(RGBA2String(config["TextColour"]["TextColour_3"]))
        self.ui.Text4_Colour.setText(RGBA2String(config["TextColour"]["TextColour_4"]))
        self.ui.Background_Colour.textChanged.connect(self.Background_Colour_Change)
        self.ui.Text1_Colour.textChanged.connect(self.Change_Text1_Colour)
        self.ui.Text2_Colour.textChanged.connect(self.Change_Text2_Colour)
        self.ui.Text3_Colour.textChanged.connect(self.Change_Text3_Colour)
        self.ui.Text4_Colour.textChanged.connect(self.Change_Text4_Colour)




        # Initialize the Arrangement Text Box
        self.ui.Arrangement_1.setText(RGBA2String(config["Arrangement"]["Arrangement_1"]))
        self.ui.Arrangement_2.setText(RGBA2String(config["Arrangement"]["Arrangement_2"]))
        self.ui.Arrangement_1.textChanged.connect(self.Arrangement_1_Change)
        self.ui.Arrangement_2.textChanged.connect(self.Arrangement_2_Change)

        # Initialize the User Defined Text
        self.ui.UserDefinedText_1.setText(config["UserDefinedText"]["Text_1"])
        self.ui.UserDefinedText_2.setText(config["UserDefinedText"]["Text_2"])
        self.ui.UserDefinedText_3.setText(config["UserDefinedText"]["Text_3"])
        self.ui.UserDefinedText_4.setText(config["UserDefinedText"]["Text_4"])
        self.ui.UserDefinedText_1.textChanged.connect(self.UserDefinedTextChange)
        self.ui.UserDefinedText_2.textChanged.connect(self.UserDefinedTextChange)
        self.ui.UserDefinedText_3.textChanged.connect(self.UserDefinedTextChange)
        self.ui.UserDefinedText_4.textChanged.connect(self.UserDefinedTextChange)



        self.ui.Font_Selection.currentTextChanged.connect(self.Change_Font)


        self.ui.CameraMake_Text.textChanged.connect(self.Change_Exif)
        self.ui.CameraModel_Text.textChanged.connect(self.Change_Exif)
        self.ui.LensMake_Text.textChanged.connect(self.Change_Exif)
        self.ui.LensModel_Text.textChanged.connect(self.Change_Exif)
        self.ui.DateTime_Text.textChanged.connect(self.Change_Exif)
        self.ui.Latitude_Text.textChanged.connect(self.Change_Exif)
        self.ui.Longitude_Text.textChanged.connect(self.Change_Exif)
        self.ui.CoordinateStr_Text.textChanged.connect(self.Change_Exif)
        self.ui.Fetch_Google_Map_Data.clicked.connect(self.Fetch_Google_Map_Data)
        self.ui.Address_Modification.textChanged.connect(self.Change_Exif)
        self.ui.AddressList.currentTextChanged.connect(self.AddressSelection)
        self.ui.Elevation_Text.textChanged.connect(self.Change_Exif)
        self.ui.Font_Weight.currentTextChanged.connect(self.Bottom_Border_Render)
        self.ui.Load_Image.clicked.connect(self.SelectFile)
        self.ui.Border_Ratio_Text.textChanged.connect(self.Border_Ratio_Change)
        self.ui.BorderRatioType.stateChanged.connect(self.Border_Ratio_Equal_Change)
        self.ui.Border_Ratio_Equal_Text.textChanged.connect(self.Border_Ratio_Equal_Change)


    def UserDefinedTextChange(self):
        global config
        config["UserDefinedText"]["Text_1"] = self.ui.UserDefinedText_1.text()
        config["UserDefinedText"]["Text_2"] = self.ui.UserDefinedText_2.text()
        config["UserDefinedText"]["Text_3"] = self.ui.UserDefinedText_3.text()
        config["UserDefinedText"]["Text_4"] = self.ui.UserDefinedText_4.text()
        self.Bottom_Border_Render()

    def Background_Colour_Selection_Change(self):
        bgColour = self.ui.Background_Colour_Selection.currentText()
        str_values_list = bgColour.split(',')
        int_values_list = [int(value) for value in str_values_list]
        config["BackgroundColour"] = int_values_list
        self.ui.Background_Colour.setText(bgColour)



    def Border_Ratio_Equal_Change(self):
        global  config,image_x,image_y
        config["EqualBorder"] = self.ui.BorderRatioType.isChecked()
        if config["EqualBorder"]:
            self.ui.Border_Ratio_Text.setReadOnly(True)
            self.ui.Border_Ratio_Equal_Text.setReadOnly(False)
            BorderRatioStr = self.ui.Border_Ratio_Equal_Text.text()
            BorderRatioList = check_equal_ratio_string(BorderRatioStr)
            if BorderRatioList:
                config["BorderRatioEqual"] = BorderRatioList
                config["BorderRatio"] = [BorderRatioList[0],BorderRatioList[0]/image_x*image_y,
                                         BorderRatioList[0]/image_x*image_y,BorderRatioList[1]]
                self.ui.Border_Ratio_Text.setText(validate_ratio_json(config["BorderRatio"]))

        else:
            self.ui.Border_Ratio_Text.setReadOnly(False)
            self.ui.Border_Ratio_Equal_Text.setReadOnly(True)
            self.ui.Border_Ratio_Text.textChanged.connect(self.Border_Ratio_Change)


    def Border_Ratio_Change(self):
        global config
        BorderRatioStr = self.ui.Border_Ratio_Text.text()
        BorderRatioList = check_ratio_string(BorderRatioStr)
        if BorderRatioList:
            config["BorderRatio"] = BorderRatioList
            self.Bottom_Border_Render()

    def load_json_file(self,file_path):
        global config
        with open(file_path) as file:
            config = json.load(file)

    def InitializeBorders(self):
        global config,ImagePos,Bottom_Border_Pos,Bottom_Border_Size, image_x, image_y, image_scale, \
            BottomBorderItem, TopBorderItem, LeftBorderItem, RightBorderItem,scene, TestRectItem

        BottomBorderItem = QGraphicsRectItem(0, 0, 360, 150)
        TopBorderItem = QGraphicsRectItem(0, 0, 360, 150)
        border_colour = config["BackgroundColour"]
        border_brush = QBrush(QColor(border_colour[0], border_colour[1], border_colour[2], border_colour[3]))
        border_pen = QPen(QColor(0, 0, 0, 0))

        BottomBorderItem.setBrush(border_brush)
        BottomBorderItem.setPen(border_pen)
        Bottom_Border_Pos = [ImagePos[0], ImagePos[1] + image_y * image_scale]
        Bottom_Border_Size = [image_x * image_scale, image_y * image_scale * config["BorderRatio"][3]/100 *
                              config["MaximumBorderRatio"][3] / 100]
        BottomBorderItem.setRect(Bottom_Border_Pos[0], Bottom_Border_Pos[1], Bottom_Border_Size[0], Bottom_Border_Size[1])

        TopBorderItem.setBrush(border_brush)
        TopBorderItem.setPen(border_pen)
        Top_Border_Pos = [ImagePos[0], ImagePos[1] - image_y * image_scale * config["BorderRatio"][0]/100 *
                              config["MaximumBorderRatio"][0] / 100]
        Top_Border_Size = [image_x * image_scale, image_y * image_scale * config["BorderRatio"][0]/100 *
                              config["MaximumBorderRatio"][0] / 100]
        TopBorderItem.setRect(Top_Border_Pos[0], Top_Border_Pos[1], Top_Border_Size[0], Top_Border_Size[1])

        LeftBorderItem = QGraphicsRectItem(0, 0, 360, 150)
        LeftBorderItem.setBrush(border_brush)
        LeftBorderItem.setPen(border_pen)
        Left_Border_Pos = [ImagePos[0] - image_x * image_scale * config["BorderRatio"][1]/100 *
                                config["MaximumBorderRatio"][1] / 100, Top_Border_Pos[1]]
        Left_Border_Size = [image_x * image_scale * config["BorderRatio"][1]/100 * config["MaximumBorderRatio"][1] / 100,
                            image_y * image_scale+Top_Border_Size[1]+Bottom_Border_Size[1]]
        LeftBorderItem.setRect(Left_Border_Pos[0], Left_Border_Pos[1], Left_Border_Size[0], Left_Border_Size[1])

        RightBorderItem = QGraphicsRectItem(0, 0, 360, 150)
        RightBorderItem.setBrush(border_brush)
        RightBorderItem.setPen(border_pen)
        Right_Border_Pos = [ImagePos[0] + image_x * image_scale, Top_Border_Pos[1]]
        Right_Border_Size = [image_x * image_scale * config["BorderRatio"][2]/100 *
                                 config["MaximumBorderRatio"][2] / 100, Left_Border_Size[1]]
        RightBorderItem.setRect(Right_Border_Pos[0], Right_Border_Pos[1], Right_Border_Size[0], Right_Border_Size[1])


        scene.addItem(BottomBorderItem)
        scene.addItem(TopBorderItem)
        scene.addItem(LeftBorderItem)
        scene.addItem(RightBorderItem)



    def InitializeTextItems(self):
        global config,myFont,text_item_1,text_item_2, text_item_3, text_item_4, scene,Bottom_Border_Size,Bottom_Border_Pos
        myFont = QFont()
        myFont.setPointSize(Bottom_Border_Size[1] * 0.35)
        myFont.setFamily(config["Font"])
        TextColour_1 = config["TextColour"]["TextColour_1"]
        TextColour_2 = config["TextColour"]["TextColour_2"]
        TextColour_3 = config["TextColour"]["TextColour_3"]
        TextColour_4 = config["TextColour"]["TextColour_4"]

        text_item_1 = QGraphicsTextItem()
        text_item_1.setFont(myFont)
        text_item_1.setPlainText(self.Str2ImageData(config["Arrangement"]["TextContent_1"]))
        text_item_1.setDefaultTextColor(QColor(TextColour_1[0], TextColour_1[1], TextColour_1[2], TextColour_1[3]))

        text_item_2 = QGraphicsTextItem()
        text_item_2.setFont(myFont)
        text_item_2.setPlainText(self.Str2ImageData(config["Arrangement"]["TextContent_2"]))
        text_item_2.setDefaultTextColor(QColor(TextColour_2[0], TextColour_2[1], TextColour_2[2], TextColour_2[3]))

        text_item_3 = QGraphicsTextItem()
        text_item_3.setFont(myFont)
        text_item_3.setPlainText(self.Str2ImageData(config["Arrangement"]["TextContent_3"]))
        text_item_3.setDefaultTextColor(QColor(TextColour_3[0], TextColour_3[1], TextColour_3[2], TextColour_3[3]))

        text_item_4 = QGraphicsTextItem()
        text_item_4.setFont(myFont)
        text_item_4.setPlainText(self.Str2ImageData(config["Arrangement"]["TextContent_4"]))
        text_item_4.setDefaultTextColor(QColor(TextColour_4[0], TextColour_4[1], TextColour_4[2], TextColour_4[3]))

        Arrangement_1 = config["Arrangement"]["Arrangement_1"]
        Arrangement_1_sum = sum(Arrangement_1)
        fontsize_1 = Bottom_Border_Size[1] * Arrangement_1[1] / Arrangement_1_sum
        fontsize_2 = Bottom_Border_Size[1] * Arrangement_1[3] / Arrangement_1_sum
        text_item_1.setPos(Bottom_Border_Pos[0], Bottom_Border_Pos[1] +
                           Bottom_Border_Size[1] * Arrangement_1[0]/Arrangement_1_sum-fontsize_1*0.18)
        text_item_2.setPos(Bottom_Border_Pos[0],
                           Bottom_Border_Pos[1] + Bottom_Border_Size[1] * (Arrangement_1[0]+Arrangement_1[1]+
                                                            Arrangement_1[2])/Arrangement_1_sum-fontsize_2*0.18)

        Arrangement_2 = config["Arrangement"]["Arrangement_2"]
        Arrangement_2_sum = sum(Arrangement_2)
        fontsize_3 = Bottom_Border_Size[1] * Arrangement_2[1] / Arrangement_2_sum
        fontsize_4 = Bottom_Border_Size[1] * Arrangement_2[3] / Arrangement_2_sum
        text_item_3.setPos(Bottom_Border_Pos[0]+Bottom_Border_Size[0]-text_item_3.boundingRect().width(), Bottom_Border_Pos[1] +
                           Bottom_Border_Size[1] * Arrangement_2[0]/Arrangement_2_sum-fontsize_3*0.18)
        text_item_4.setPos(Bottom_Border_Pos[0]+Bottom_Border_Size[0]-text_item_4.boundingRect().width(),
                           Bottom_Border_Pos[1] + Bottom_Border_Size[1] * (Arrangement_2[0]+Arrangement_2[1]+
                                                            Arrangement_2[2])/Arrangement_2_sum-fontsize_4*0.18)

        scene.addItem(text_item_1)
        scene.addItem(text_item_2)
        scene.addItem(text_item_3)
        scene.addItem(text_item_4)


    def AddressSelection(self):
        global exif_s
        exif_s["AddressStr"] = self.ui.AddressList.currentText()
        self.ui.Address_Modification.setText(exif_s["AddressStr"])


    def Fetch_Google_Map_Data(self):
        global exif_s
        exif_s["Elevation"] = google_elevation(exif_s["Latitude"],exif_s["Longitude"])
        exif_s["AddressList"] = google_address(exif_s["Latitude"],exif_s["Longitude"])
        self.ui.AddressList.addItems(exif_s["AddressList"])
        self.ui.Elevation_Text.setText(str(exif_s["Elevation"]))

    def Change_Exif(self):
        global exif_s
        exif_s["Make"] = self.ui.CameraMake_Text.text()
        exif_s["Model"] = self.ui.CameraModel_Text.text()
        exif_s["LensMake"] = self.ui.LensMake_Text.text()
        exif_s["LensModel"] = self.ui.LensModel_Text.text()
        exif_s["DateTime"] = self.ui.DateTime_Text.text()
        if valid_coordinate(self.ui.Latitude_Text.text()):
            exif_s["Latitude"] = float(self.ui.Latitude_Text.text())
        if valid_coordinate(self.ui.Longitude_Text.text()):
            exif_s["Longitude"] = float(self.ui.Longitude_Text.text())
        if validate_elevation(self.ui.Elevation_Text.text()):
            exif_s["Elevation"] = float(self.ui.Elevation_Text.text())
        exif_s["CoordinateStr"] = self.ui.CoordinateStr_Text.text()
        exif_s["AddressStr"] = self.ui.Address_Modification.text()
        self.Bottom_Border_Render()

    def Change_Font(self):
        global config
        cacheFont = QFont()
        chacheId = QFontDatabase.addApplicationFont(os.path.dirname(__file__) + "/resources/fonts/" +
                                              self.ui.Font_Selection.currentText() + ".ttf")
        config["Font"] = QFontDatabase.applicationFontFamilies(chacheId)[0]
        cacheFont.setFamily(config["Font"])
        cacheFont.setWeight(QFont.Thin)
        self.ui.Font_Weight.setItemData(0, cacheFont, role=Qt.FontRole)
        cacheFont.setWeight(QFont.ExtraLight)
        self.ui.Font_Weight.setItemData(1, cacheFont, role=Qt.FontRole)
        cacheFont.setWeight(QFont.Light)
        self.ui.Font_Weight.setItemData(2, cacheFont, role=Qt.FontRole)
        cacheFont.setWeight(QFont.Normal)
        self.ui.Font_Weight.setItemData(3, cacheFont, role=Qt.FontRole)
        cacheFont.setWeight(QFont.Medium)
        self.ui.Font_Weight.setItemData(4, cacheFont, role=Qt.FontRole)
        cacheFont.setWeight(QFont.DemiBold)
        self.ui.Font_Weight.setItemData(5, cacheFont, role=Qt.FontRole)
        cacheFont.setWeight(QFont.Bold)
        self.ui.Font_Weight.setItemData(6, cacheFont, role=Qt.FontRole)
        cacheFont.setWeight(QFont.ExtraBold)
        self.ui.Font_Weight.setItemData(7, cacheFont, role=Qt.FontRole)
        cacheFont.setWeight(QFont.Black)
        self.ui.Font_Weight.setItemData(8, cacheFont, role=Qt.FontRole)

        self.Bottom_Border_Render()



    def Str2ImageData(self,value):
        global exif_s

        if exif_s["ExposureTimeDenominator"]==1:
            cases = {
                "Camera Make and Model": exif_s["Make"] + " " + exif_s["Model"],
                "Camera Make": exif_s["Make"],
                "Camera Model": exif_s["Model"],
                "Lens Make and Model": exif_s["LensMake"] + " " + exif_s["LensModel"],
                "Lens Make": exif_s["LensMake"],
                "Lens Model": exif_s["LensModel"],
                "Parameters": str(exif_s["35mmFocalLength"]) + "mm  f/" + str(exif_s["Aperture"]) + "  " +
                              str(exif_s["ExposureTimeNumerator"]) + "s  ISO" + str(exif_s["ISO"]),
                "Date and Time": exif_s["DateTime"],
                "Coordinates": "{:.5f}".format(exif_s["Latitude"]) + "," + "{:.5f}".format(exif_s["Longitude"]),
                "Coordinates (DMS)": exif_s["CoordinateStr"],
                "Address": exif_s["AddressStr"],
                "Elevation": "{:.1f}".format(exif_s["Elevation"]) + "m",
                "User Content 1": config["UserDefinedText"]["Text_1"],
                "User Content 2": config["UserDefinedText"]["Text_2"],
                "User Content 3": config["UserDefinedText"]["Text_3"],
                "User Content 4": config["UserDefinedText"]["Text_4"],
                "None": ""
            }
        else:
            cases = {
                "Camera Make and Model": exif_s["Make"] + " " + exif_s["Model"],
                "Camera Make": exif_s["Make"],
                "Camera Model": exif_s["Model"],
                "Lens Make and Model": exif_s["LensMake"] + " " + exif_s["LensModel"],
                "Lens Make": exif_s["LensMake"],
                "Lens Model": exif_s["LensModel"],
                "Parameters": str(exif_s["35mmFocalLength"]) + "mm f/" + str(exif_s["Aperture"]) + " " + \
                              str(exif_s["ExposureTimeNumerator"]) + "/" +
                              str(exif_s["ExposureTimeDenominator"]) + "s ISO" + str(exif_s["ISO"]),
                "Date and Time": exif_s["DateTime"],
                "Coordinates": "{:.5f}".format(exif_s["Latitude"]) + "," + "{:.5f}".format(exif_s["Longitude"]),
                "Coordinates (DMS)": exif_s["CoordinateStr"],
                "Address": exif_s["AddressStr"],
                "Elevation": "{:.1f}".format(exif_s["Elevation"]) + "m",
                "User Content 1": config["UserDefinedText"]["Text_1"],
                "User Content 2": config["UserDefinedText"]["Text_2"],
                "User Content 3": config["UserDefinedText"]["Text_3"],
                "User Content 4": config["UserDefinedText"]["Text_4"],
                "None": ""
            }



        Text = cases.get(value, 'Variable not found')
        return Text

    def Arrangement_1_Change(self):
        global config
        string = self.ui.Arrangement_1.text()
        Arrangement_1 = validate_float_string_5(string)
        if Arrangement_1:
            config["Arrangement"]["Arrangement_1"] = Arrangement_1
            self.Bottom_Border_Render()

    def Arrangement_2_Change(self):
        global config
        string = self.ui.Arrangement_2.text()
        Arrangement_2 = validate_float_string_5(string)
        if Arrangement_2:
            config["Arrangement"]["Arrangement_2"] = Arrangement_2
            self.Bottom_Border_Render()

    def Change_Text1_Content(self):
        global text1_content,text_item_1
        text1_content = self.ui.Text1_Content.currentText()
        text_item_1.setPlainText(self.Str2ImageData(text1_content))
        self.Bottom_Border_Render()

    def Change_Text2_Content(self):
        global text2_content,text_item_2
        text2_content = self.ui.Text2_Content.currentText()
        text_item_2.setPlainText(self.Str2ImageData(text2_content))
        self.Bottom_Border_Render()

    def Change_Text3_Content(self):
        global text3_content,text_item_3
        text3_content = self.ui.Text3_Content.currentText()
        text_item_3.setPlainText(self.Str2ImageData(text3_content))
        self.Bottom_Border_Render()

    def Change_Text4_Content(self):
        global text4_content,text_item_4
        text4_content = self.ui.Text4_Content.currentText()
        text_item_4.setPlainText(self.Str2ImageData(text4_content))
        self.Bottom_Border_Render()





    def Background_Colour_Change(self):
        global BottomBorderItem
        colour = self.ui.Background_Colour.text()
        integers = self.validate_string_4int(colour)
        if integers:
            a, b, c, d = integers
            BottomBorderItem.setBrush(QBrush(QColor(a, b, c, d)))
            LeftBorderItem.setBrush(QBrush(QColor(a, b, c, d)))
            RightBorderItem.setBrush(QBrush(QColor(a, b, c, d)))
            TopBorderItem.setBrush(QBrush(QColor(a, b, c, d)))


    def Change_Text1_Colour(self):
        global text_item_1
        colour = self.ui.Text1_Colour.text()
        integers = self.validate_string_4int(colour)
        if integers:
            a, b, c, d = integers
            text_item_1.setDefaultTextColor(QColor(a, b, c, d))


    def Change_Text2_Colour(self):
        global text_item_2
        colour = self.ui.Text2_Colour.text()
        integers = self.validate_string_4int(colour)
        if integers:
            a, b, c, d = integers
            text_item_2.setDefaultTextColor(QColor(a, b, c, d))

    def Change_Text3_Colour(self):
        global text_item_3
        colour = self.ui.Text3_Colour.text()
        integers = self.validate_string_4int(colour)
        if integers:
            a, b, c, d = integers
            text_item_3.setDefaultTextColor(QColor(a, b, c, d))


    def Change_Text4_Colour(self):
        global text_item_4
        colour = self.ui.Text4_Colour.text()
        integers = self.validate_string_4int(colour)
        if integers:
            a, b, c, d = integers
            text_item_4.setDefaultTextColor(QColor(a, b, c, d))



    def validate_string_4int(self, string):
        try:
            a, b, c, d = map(int, string.split(","))
            return a, b, c, d
        except ValueError:
            return None


    def Render_Image(self):
        global PhotoPixmap, BottomBorderItem, PhotoItem, text_item_1, exif,Bottom_Border_Pos,myFont,text_item_2,\
            Bottom_Border_Size,scene,tt_Rect, ImagePos, image_x, image_y, image_scale, config,exif_s

        scene = QGraphicsScene()

        # Rotate the Photo tp Correct Position
        if exif_s["Rotation"]== 3:
            PhotoPixmap = PhotoPixmap.transformed(QTransform().rotate(180))
        elif exif_s["Rotation"] == 6:
            PhotoPixmap = PhotoPixmap.transformed(QTransform().rotate(90))
        elif exif_s["Rotation"] == 8:
            PhotoPixmap = PhotoPixmap.transformed(QTransform().rotate(270))

        # Set the Photo to Correct Scale
        image_x = PhotoPixmap.width()
        image_y = PhotoPixmap.height()
        image_scale = 500 / max(image_x, image_y)
        PhotoItem = QGraphicsPixmapItem(PhotoPixmap)
        PhotoItem.setScale(image_scale)

        # Set the Photo to Correct Position
        if image_x > image_y:
            ImagePos = [50, 50 + (500 - image_y * image_scale) / 2]
        else:
            ImagePos = [50 + (500 - image_x * image_scale) / 2, 25]
        PhotoItem.setPos(ImagePos[0], ImagePos[1])

        #Initialize the Transparent Rectangle Mask
        transparent_Rect = QGraphicsRectItem(0, 0, 600, 600)
        trans_brush = QBrush(QColor(0, 0, 0, 0))
        trans_pen = QPen(QColor(0, 0, 0, 0))
        transparent_Rect.setBrush(trans_brush)
        transparent_Rect.setPen(trans_pen)

        self.InitializeBorders()
        self.InitializeTextItems()

        scene.addItem(PhotoItem)
        scene.addItem(transparent_Rect)

        self.ui.preview.setScene(scene)
        self.ui.preview.setRenderHint(QPainter.SmoothPixmapTransform)


        chacheId = QFontDatabase.addApplicationFont(os.path.dirname(__file__) + "/resources/fonts/" +
                                              self.ui.Font_Selection.currentText() + ".ttf")
        config["Font"] = QFontDatabase.applicationFontFamilies(chacheId)[0]

        self.Border_Ratio_Equal_Change()

        self.Bottom_Border_Render()


    def Bottom_Border_Render(self):
        global PhotoItem, BottomBorderItem, TopBorderItem, LeftBorderItem, RightBorderItem, \
            text_item_1, text_item_2, text_item_3, text_item_4, Bottom_Border_Pos, myFont, Bottom_Border_Size, \
             scene, tt_Rect, config, TestRectItem
        image_x = PhotoPixmap.width()
        image_y = PhotoPixmap.height()
        image_scale = 500 / max(image_x, image_y)

        Bottom_Border_Pos = [ImagePos[0], ImagePos[1] + image_y * image_scale]
        Bottom_Border_Size = [image_x * image_scale, image_y * image_scale * config["BorderRatio"][3] / 100 *
                              config["MaximumBorderRatio"][3] / 100]
        BottomBorderItem.setRect(Bottom_Border_Pos[0], Bottom_Border_Pos[1], Bottom_Border_Size[0],
                                 Bottom_Border_Size[1])

        Top_Border_Pos = [ImagePos[0], ImagePos[1] - image_y * image_scale * config["BorderRatio"][0]/100 *
                              config["MaximumBorderRatio"][0] / 100]
        Top_Border_Size = [image_x * image_scale, image_y * image_scale * config["BorderRatio"][0]/100 *
                              config["MaximumBorderRatio"][0] / 100]
        TopBorderItem.setRect(Top_Border_Pos[0], Top_Border_Pos[1], Top_Border_Size[0], Top_Border_Size[1])

        Left_Border_Pos = [ImagePos[0] - image_x * image_scale * config["BorderRatio"][1]/100 *
                                config["MaximumBorderRatio"][1] / 100, Top_Border_Pos[1]]
        Left_Border_Size = [image_x * image_scale * config["BorderRatio"][1]/100 * config["MaximumBorderRatio"][1] / 100,
                            image_y * image_scale+Top_Border_Size[1]+Bottom_Border_Size[1]]
        LeftBorderItem.setRect(Left_Border_Pos[0], Left_Border_Pos[1], Left_Border_Size[0], Left_Border_Size[1])

        Right_Border_Pos = [ImagePos[0] + image_x * image_scale, Top_Border_Pos[1]]
        Right_Border_Size = [image_x * image_scale * config["BorderRatio"][2]/100 *
                                 config["MaximumBorderRatio"][2] / 100, Left_Border_Size[1]]
        RightBorderItem.setRect(Right_Border_Pos[0], Right_Border_Pos[1], Right_Border_Size[0], Right_Border_Size[1])

        Arrangement_1 = config["Arrangement"]["Arrangement_1"]
        Arrangement_1_sum = sum(Arrangement_1)
        Arrangement_2 = config["Arrangement"]["Arrangement_2"]
        Arrangement_2_sum = sum(Arrangement_2)
        config["FontWeight"] = self.ui.Font_Weight.currentText()

        myFont.setFamily(config["Font"])
        if config["FontWeight"] == "Thin":
            myFont.setWeight(QFont.Thin)
        elif config["FontWeight"] == "ExtraLight":
            myFont.setWeight(QFont.ExtraLight)
        elif config["FontWeight"] == "Light":
            myFont.setWeight(QFont.Light)
        elif config["FontWeight"] == "Normal":
            myFont.setWeight(QFont.Normal)
        elif config["FontWeight"] == "Medium":
            myFont.setWeight(QFont.Medium)
        elif config["FontWeight"] == "DemiBold":
            myFont.setWeight(QFont.DemiBold)
        elif config["FontWeight"] == "Bold":
            myFont.setWeight(QFont.Bold)
        elif config["FontWeight"] == "ExtraBold":
            myFont.setWeight(QFont.ExtraBold)
        elif config["FontWeight"] == "Black":
            myFont.setWeight(QFont.Black)

        fontsize_1 = Bottom_Border_Size[1] * Arrangement_1[1] / Arrangement_1_sum
        if fontsize_1 <= 0:
            fontsize_1 = 1
        myFont.setPointSize(fontsize_1)
        text_item_1.setFont(myFont)

        fontsize_2 = Bottom_Border_Size[1] * Arrangement_1[3] / Arrangement_1_sum
        if fontsize_2 <= 0:
            fontsize_2 = 1
        myFont.setPointSize(fontsize_2)
        text_item_2.setFont(myFont)

        fontsize_3 = Bottom_Border_Size[1] * Arrangement_2[1] / Arrangement_2_sum
        if fontsize_3 <= 0:
            fontsize_3 = 1
        myFont.setPointSize(fontsize_3)
        text_item_3.setFont(myFont)

        fontsize_4 = Bottom_Border_Size[1] * Arrangement_2[3] / Arrangement_2_sum
        if fontsize_4 <= 0:
            fontsize_4 = 1
        myFont.setPointSize(fontsize_4)
        text_item_4.setFont(myFont)


        text_item_1.setPos(Bottom_Border_Pos[0], Bottom_Border_Pos[1] +Bottom_Border_Size[1] * Arrangement_1[0] /
                           Arrangement_1_sum - fontsize_1 * 0.18)
        text_item_2.setPos(Bottom_Border_Pos[0],
                           Bottom_Border_Pos[1] + Bottom_Border_Size[1] * (Arrangement_1[0] + Arrangement_1[1] +
                                                            Arrangement_1[2]) / Arrangement_1_sum - fontsize_2 * 0.18)

        text_item_3.setPos(Bottom_Border_Pos[0]+Bottom_Border_Size[0]-text_item_3.boundingRect().width(), Bottom_Border_Pos[1] +
                             Bottom_Border_Size[1] * Arrangement_2[0]/Arrangement_2_sum-fontsize_3*0.18)
        text_item_4.setPos(Bottom_Border_Pos[0]+Bottom_Border_Size[0]-text_item_4.boundingRect().width(),
                            Bottom_Border_Pos[1] + Bottom_Border_Size[1] * (Arrangement_2[0]+Arrangement_2[1]+
                                                                Arrangement_2[2])/Arrangement_2_sum-fontsize_4*0.18)

        text1_content = self.ui.Text1_Content.currentText()
        text_item_1.setPlainText(self.Str2ImageData(text1_content))
        text2_content = self.ui.Text2_Content.currentText()
        text_item_2.setPlainText(self.Str2ImageData(text2_content))





    def SelectFile(self):
        global PhotoPixmap, exif, exif_s
        file_filter = "Image Files (*.JPG *.jpg *.jpeg *.JPEG *.png *.PNG *.tiff *.TIFF);"
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "Open File", "", file_filter)
        PhotoPixmap = QPixmap(image_path)
        tt = PhotoPixmap
        Photo_Copy = Image.open(image_path)
        try:
            exif = Photo_Copy._getexif()
        except KeyError:
            pass

        Latitude = 0
        Longitude = 0
        CoordinateStr = ""

        try:
            Latitude, Longitude,CoordinateStr = coordinate_transform(exif[34853])
        except KeyError:
            pass

        exif_s = {
            "Rotation": 0,
            "Make": "",
            "Model": "",
            "DateTime": "",
            "ExposureTime": "",
            "Aperture": "",
            "ISO": "",
            "FocalLength": "",
            "LensMake": "",
            "LensModel": "",
            "XResolution": "",
            "35mmFocalLength": "",
            "Latitude": Latitude,
            "Longitude": Longitude,
            "CoordinateStr": CoordinateStr,
            "AddressStr": "",
            "AddressList": [],
            "Elevation": 0
        }
        try:
            exif_s["Rotation"] = exif[274]
        except KeyError:
            pass
        try:
            exif_s["Make"] = exif[271]
            exif_s["Model"] = exif[272]
            exif_s["DateTime"] = exif[36867]
            exif_s["ExposureTimeDenominator"] = exif[33434].denominator
            exif_s["ExposureTimeNumerator"] = exif[33434].numerator
            exif_s["Aperture"] = exif[33437]
            exif_s["ISO"] = exif[34855]
            exif_s["FocalLength"] = exif[37386]
            exif_s["LensMake"] = exif[42035]
            exif_s["LensModel"] = exif[42036]
            exif_s["XResolution"] = exif[282]
            exif_s["35mmFocalLength"] = exif[41989]
        except KeyError:
            pass


        self.ui.CameraMake_Text.textChanged.disconnect(self.Change_Exif)
        self.ui.CameraModel_Text.textChanged.disconnect(self.Change_Exif)
        self.ui.LensMake_Text.textChanged.disconnect(self.Change_Exif)
        self.ui.LensModel_Text.textChanged.disconnect(self.Change_Exif)
        self.ui.DateTime_Text.textChanged.disconnect(self.Change_Exif)
        self.ui.Latitude_Text.textChanged.disconnect(self.Change_Exif)
        self.ui.Longitude_Text.textChanged.disconnect(self.Change_Exif)
        self.ui.CoordinateStr_Text.textChanged.disconnect(self.Change_Exif)
        self.ui.Address_Modification.textChanged.disconnect(self.Change_Exif)
        self.ui.CameraMake_Text.setText(exif_s["Make"])
        self.ui.CameraModel_Text.setText(exif_s["Model"])
        self.ui.LensMake_Text.setText(exif_s["LensMake"])
        self.ui.LensModel_Text.setText(exif_s["LensModel"])
        self.ui.DateTime_Text.setText(exif_s["DateTime"])
        self.ui.Latitude_Text.setText(str(exif_s["Latitude"]))
        self.ui.Longitude_Text.setText(str(exif_s["Longitude"]))
        self.ui.CoordinateStr_Text.setText(exif_s["CoordinateStr"])
        self.ui.CameraMake_Text.textChanged.connect(self.Change_Exif)
        self.ui.CameraModel_Text.textChanged.connect(self.Change_Exif)
        self.ui.LensMake_Text.textChanged.connect(self.Change_Exif)
        self.ui.LensModel_Text.textChanged.connect(self.Change_Exif)
        self.ui.DateTime_Text.textChanged.connect(self.Change_Exif)
        self.ui.Latitude_Text.textChanged.connect(self.Change_Exif)
        self.ui.Longitude_Text.textChanged.connect(self.Change_Exif)
        self.ui.CoordinateStr_Text.textChanged.connect(self.Change_Exif)
        self.ui.Address_Modification.textChanged.connect(self.Change_Exif)

        colour_list = dominent_colour(image_path, 8, False)
        for row in colour_list:
            row.append(255)
        sorted_matrix = sorted(colour_list, key=lambda row: sum(row), reverse=False)
        string_list = [','.join(map(str, row)) for row in sorted_matrix]
        self.ui.Background_Colour_Selection.addItems(string_list)
        counter = self.ui.Background_Colour_Selection.count()

        for i in range(counter):
            pixmap = QPixmap(20, 20)
            rgba_values = list(map(int, self.ui.Background_Colour_Selection.itemText(i).split(',')))
            qcolor = QColor(*rgba_values)
            pixmap.fill(qcolor)
            self.ui.Background_Colour_Selection.setItemIcon(i, QIcon(pixmap))

        # Initialize the suggesting colour combo box
        self.ui.Background_Colour_Selection.currentTextChanged.connect(self.Background_Colour_Selection_Change)




        self.Render_Image()



    def check_appearance(self):
        """Checks DARK/LIGHT mode of macos."""
        cmd = 'defaults read -g AppleInterfaceStyle'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        return bool(p.communicate()[0])



app = QApplication([])
stats = Stats()
stats.ui.show()

app.exec()