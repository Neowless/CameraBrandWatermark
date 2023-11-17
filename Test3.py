from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QPixmap,QImageReader
app = QApplication([])
QImageReader.setAllocationLimit(0)
# Load the image
image_path = "qianli-zhang-x2d-xcd-28p-1-full-size.jpg"
pixmap = QPixmap(image_path)
# Create a QLabel and set the pixmap
label = QLabel()
label.setPixmap(pixmap)
# Show the label
label.show()
app.exec()