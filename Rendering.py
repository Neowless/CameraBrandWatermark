
def Render_Image(self):
    global pixmap, item, pixmap_item, text_item_1, exif ,Bottom_Border_Pos ,myFont ,text_item_2 ,Bottom_Border_Size ,scene,tt_Rect

    scene = QGraphicsScene()

    if exif[274] == 3:
        pixmap = pixmap.transformed(QTransform().rotate(180))
    elif exif[274] == 6:
        pixmap = pixmap.transformed(QTransform().rotate(90))
    elif exif[274] == 8:
        pixmap = pixmap.transformed(QTransform().rotate(270))
    image_x = pixmap.width()
    image_y = pixmap.height()
    image_scale = 500 / max(image_x, image_y)
    pixmap_item = QGraphicsPixmapItem(pixmap)
    pixmap_item.setScale(image_scale)

    if image_x > image_y:
        Image_Pos = [50, 50 + (500 - image_y * image_scale) / 2]
    else:
        Image_Pos = [50 + (500 - image_x * image_scale) / 2, 25]

    pixmap_item.setPos(Image_Pos[0],Image_Pos[1])

    item = QGraphicsRectItem(0, 0, 360, 150)
    brush = QBrush(QColor(255, 255, 255))
    border_pen = QPen(QColor(0, 0, 0, 0))
    item.setBrush(brush)
    item.setPen(border_pen)

    Bottom_Border_Pos = [Image_Pos[0], Image_Pos[1] + image_y * image_scale]

    Bottom_Border_Size = [image_x * image_scale, image_y * image_scale * 50 * 0.3 / 100]

    item.setRect(Bottom_Border_Pos[0], Bottom_Border_Pos[1],Bottom_Border_Size[0], Bottom_Border_Size[1])

    transparent_Rect = QGraphicsRectItem(0, 0, 600, 600)
    trans_brush = QBrush(QColor(0, 0, 0, 0))
    trans_pen = QPen(QColor(0, 0, 0, 0))
    transparent_Rect.setBrush(trans_brush)
    transparent_Rect.setPen(trans_pen)

    myFont = QFont()
    myFont.setPointSize(Bottom_Border_Size[1]*0.35)
    id = QFontDatabase.addApplicationFont(os.path.dirname(__file__) + "/resources/fonts/得意黑.ttf")
    familyStr = QFontDatabase.applicationFontFamilies(id)[0]
    myFont.setFamily(familyStr)

    text_item_1 = QGraphicsTextItem()
    text_item_1.setFont(myFont)
    text_item_1.setPlainText(exif_s["LensModel"])
    text_item_1.setDefaultTextColor(QColor(0, 0, 0, 255))
    text_item_1.setPos(Bottom_Border_Pos[0], Bottom_Border_Pos[1])

    text_item_2 = QGraphicsTextItem()
    text_item_2.setFont(myFont)
    text_item_2.setPlainText(exif_s["Make"]+" "+exif_s[ " Model"])
    text_item_2.setDefaultTextColor(QColor(160, 160, 160, 255))
    text_item_2.setPos(Bottom_Border_Pos[0], Bottom_Border_Pos[1]+Bottom_order_Size[1]*0.55)

    Arrangement_1_sum = sum(Arrangement_1)

    fontsize_1 = Bottom_Border_Size[1] * Arrangement_1[1] / Arrangement_1_sum

    fontsize_2 = Bottom_Border_Size[1] * Arrangement_1[3] / Arrangement_1_sum
    text_item_1.setPos(Bottom_Border_Pos[0], Bottom_Border_Pos[1] +
                       Bottom_Border_Size[1] * Arrangement_1[0]/Arrangement_1_sum-fontsize_1*0.18)
    text_item_2.setPos(Bottom_Border_Pos[0],
                       Bottom_Border_Pos[1] + Bottom_Border_Size[1] * (Arrangement_1[0]+Arrangement_1[1]+Arrangement_1[2])/Arragement_1_sum-fontsize_2*0.18)

    tt_Rect = QGraphicsRectItem(0,0,0,0)
    tt_brush = QBrush(QColor(0, 0, 0, 0))
    tt_pen = QPen(QColor(0, 0, 0, 255))
    tt_Rect.setBrush(tt_brush)
    tt_Rect.setPen(tt_pen)

    scene.addItem(tt_Rect)


    scene.addItem(pixmap_item)
    scene.addItem(item)
    scene.addItem(transparent_Rect)
    scene.addItem(text_item_1)
    scene.addItem(text_item_2)
    self.ui.preview.setScene(scene)
    self.ui.preview.setRenderHint(QPainter.SmoothPixmapTransform)
    self.ui.Bottom_Border_Slider.setEnabled(True)
    self.ui.Bottom_Border_SpinBox.setEnabled(True)