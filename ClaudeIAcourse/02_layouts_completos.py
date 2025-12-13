import sys

from PySide6.QtWidgets import(
    QApplication, QFormLayout, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMainWindow, QVBoxLayout, QWidget
    )


class LayoutsDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dominando Layouts")
        self.setGeometry(100, 100, 600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        main_layout.addWidget(QLabel("VBoxLayout: Empilha Widgets Verticalmente"))
        vbox_demo = QWidget()
        vbox = QVBoxLayout()
        vbox_demo.setLayout(vbox)
        vbox.addWidget(QPushButton("Botão 1"))
        vbox.addWidget(QPushButton("Botão 2"))
        vbox.addWidget(QPushButton("Botão 3"))
        main_layout.addWidget(vbox_demo)

        main_layout.addWidget(
            QLabel("HBoxLayout: Empilha Widgets Horizontalmente"))
        hbox_demo = QWidget()
        hbox = QHBoxLayout()
        hbox_demo.setLayout(hbox)
        hbox.addWidget(QPushButton("Botão 1"))
        hbox.addWidget(QPushButton("Botão 2"))
        hbox.addWidget(QPushButton("Botão 3"))
        main_layout.addWidget(hbox_demo)

        main_layout.addWidget(
            QLabel("GridLayout: Empilha como uma grade de linhas e colunas")
            )
        
        grid_demo = QWidget()
        grid = QGridLayout()
        grid_demo.setLayout(grid)
        # addWidget(widget, linha, coluna, span_linhas, span_colunas)
        grid.addWidget(QPushButton("1"), 0, 0)
        grid.addWidget(QPushButton("2"), 0, 1)
        grid.addWidget(QPushButton("3"), 0, 2)
        grid.addWidget(QPushButton("4"), 1, 0)
        grid.addWidget(QPushButton("5 (span 2 colunas)"), 1, 1, 1, 2)
        main_layout.addWidget(grid_demo)

        main_layout.addWidget(QLabel("FormLayout: perfeito para formulários"))
        form_demo = QWidget()
        form = QFormLayout()
        form_demo.setLayout(form)
        form.addRow("Nome:", QLineEdit())
        form.addRow("Email:", QLineEdit())
        form.addRow("Mensagem:", QLineEdit())
        main_layout.addWidget(form_demo)

        # Adiciona espaço elástico no final
        main_layout.addStretch()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = LayoutsDemo()
    janela.show()
    sys.exit(app.exec())