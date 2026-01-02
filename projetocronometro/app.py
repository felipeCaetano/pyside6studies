from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication


class Cronometro:
    def __init__(self):
        carregador = QUiLoader()
        self.ui = carregador.load('./interfaces/interface.ui')
        self.ui.setWindowTitle("Pymodoro Timer")
        self.ui.setWindowIcon(QIcon('.interfaces/imagens/cronometro.png'))


if __name__ == '__main__':
    app = QApplication()
    window = Cronometro()
    window.ui.show()
    app.exec()