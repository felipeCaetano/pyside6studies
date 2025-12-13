import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt


class MinhaJanela(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minha primeira Janela Pyside6")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.label = QLabel("Clique no botão abaixo:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        botao = QPushButton("Clique em mim!")
        botao.clicked.connect(self.on_click)
        layout.addWidget(botao)

        self.click_count = 0
    
    def on_click(self):
        self.click_count += 1
        self.label.setText(f"Você clicou {self.click_count} vezes!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = MinhaJanela()
    janela.show()
    sys.exit(app.exec())