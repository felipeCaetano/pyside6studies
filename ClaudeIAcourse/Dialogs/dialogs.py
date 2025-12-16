import sys

from PySide6.QtWidgets import (QApplication, QDialog, QDialogButtonBox, QLabel,
 QMainWindow, QPushButton, QVBoxLayout)


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hello!")
        qbtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(qbtn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("Algo aconteceu! ok?")
        layout.addWidget(message)
        layout.addWidget(self.button_box)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        print("click", s)
        dlg = CustomDialog(self)
        if dlg.exec():
            print("Sucess!")
        else:
            print("Cancel")
        


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()