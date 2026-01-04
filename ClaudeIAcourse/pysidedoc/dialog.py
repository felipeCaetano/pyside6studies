import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("My form")
        self.edit = QLineEdit("Write your name here")
        self.button = QPushButton("Show greetings")
        self.button.clicked.connect(self.show_greetings)
        layout = QVBoxLayout(self)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

    @Slot()
    def show_greetings(self):
        print(f"Hello, {self.edit.text()}")
        

if __name__ == "__main__":
    app = QApplication()
    form = Form()
    form.show()
    sys.exit(app.exec())
