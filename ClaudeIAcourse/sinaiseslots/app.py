import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Correntes Máximas")
        self.button_is_checked = True
        button = QPushButton("Login")
        button.setCheckable(True)
        button.clicked.connect(self.on_login)
        button.setChecked(self.button_is_checked)
        self.setCentralWidget(button)

    def on_login(self, checked):
        print("clicou no login")
        self.button_is_checked = checked
        print(self.button_is_checked)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())