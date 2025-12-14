import sys
from PySide6.QtWidgets import QApplication, QPushButton


app = QApplication(sys.argv)

window = QPushButton("Clique me")
window.show()

app.exec()