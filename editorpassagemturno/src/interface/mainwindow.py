import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QLabel)

from editorpassagemturno.src.interface.navigationdrawer import NavigationDrawer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de Passagem de Turno")
        self.setGeometry(100, 100, 1000, 600)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = NavigationDrawer()
        main_layout.addWidget(self.sidebar)

        # Área de conteúdo
        content_area = QWidget()
        content_area.setStyleSheet("background-color: #ecf0f1;")
        content_layout = QVBoxLayout(content_area)

        toggle_btn = QPushButton("☰")
        toggle_btn.setFixedSize(100, 40)
        toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        toggle_btn.clicked.connect(self.sidebar.toggle)
        content_layout.addWidget(toggle_btn,
                                 alignment=Qt.AlignLeft | Qt.AlignTop)

        #sidebar text, icon_name, color, slot
        btn_conf = ["Configuração", "ri.list-check", "black", self.show_config]
        self.sidebar.add_menu_buttons(btn_conf)
        btn_nct = ["NCT", "ph.thermometer-hot-light", "blue", self.show_config]
        self.sidebar.add_menu_buttons(btn_nct)
        btn_obs = [
            "Observações", 'fa5s.exclamation-triangle', 'yellow',
            self.show_config]
        self.sidebar.add_menu_buttons(btn_obs)
        # Conteúdo principal
        title = QLabel("Conteúdo Principal")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
            padding: 20px;
        """)
        content_layout.addWidget(title, alignment=Qt.AlignCenter)

        description = QLabel(
            "Troque entre NavigationDrawer e NavigationRail\nno código para ver as diferenças!")
        description.setStyleSheet("""
            font-size: 16px;
            color: #7f8c8d;
        """)
        description.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(description, alignment=Qt.AlignCenter)

        content_layout.addStretch()

        main_layout.addWidget(content_area, stretch=1)

    def show_config(self):
        print("mostra a configuração na tela")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
