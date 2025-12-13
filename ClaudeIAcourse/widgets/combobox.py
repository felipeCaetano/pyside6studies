import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        layout = QVBoxLayout()

        combobox = QComboBox()
        combobox.addItems(["BGI", "JRM", "RCD"])

        # The default signal from currentIndexChanged sends the index
        combobox.currentIndexChanged.connect(self.index_changed)

        # The same signal can send a text string
        combobox.currentTextChanged.connect(self.text_changed)

        layout.addWidget(combobox)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def index_changed(self, index):  # index is an int starting from 0
        print(index)

    def text_changed(self, text):  # text is a str
        print(text)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()