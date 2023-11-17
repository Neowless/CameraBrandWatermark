
def Rotate_Image (direction,image):
    if direction == 3:
        image = image.transformed(QTransform().rotate(180))
    elif direction == 6:
        image = image.transformed(QTransform().rotate(90))
    elif direction == 8:
        image = image.transformed(QTransform().rotate(270))
    return image