import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QLabel, QPushButton

app = QApplication(sys.argv)


@Slot()
def say_hello():
    print("Button clicked, Hello!")

button = QPushButton("click me")
button.clicked.connect(say_hello)
button.show()

label = QLabel("Hello, World!")
label.show()
app.exec()