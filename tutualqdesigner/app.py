import sys
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtUiTools import QUiLoader

loader = QUiLoader()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        btn = QPushButton("Abrir Dialog")
        btn.pressed.connect(self.launch_dialog)

        self.setCentralWidget(btn)

    def launch_dialog(self):
        dialog = loader.load("ui/dialog.ui", None)
        result = dialog.exec()
        if result:
            print("sucess")
        else:
            print('Cancelled.')


def mainwindow_setup(window):
    window.setWindowTitle("Main Window Title")


app = QApplication(sys.argv)
window = MainWindow()
mainwindow_setup(window)
window.show()
app.exec()