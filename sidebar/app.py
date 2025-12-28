import sys

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QLabel, QFrame)


class NavigationDrawer(QFrame):
    """Sidebar que pode ser expandida/recolhida"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumWidth(250)
        self.setMinimumWidth(0)
        self.setStyleSheet("""
            NavigationDrawer {
                background-color: #2c3e50;
                border-right: 2px solid #34495e;
            }
        """)

        self.setup_ui()
        self.is_expanded = False

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QLabel("Menu")
        header.setStyleSheet("""
            QLabel {
                background-color: #34495e;
                color: white;
                padding: 20px;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        layout.addWidget(header)

        # Botões de navegação
        buttons_data = [("🏠", "Home"), ("📊", "Dashboard"),
            ("⚙️", "Configurações"), ("📁", "Arquivos"), ("👤", "Perfil"), ]

        for icon, text in buttons_data:
            btn = QPushButton(f"{icon}  {text}")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    text-align: left;
                    padding: 15px 20px;
                    border: none;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #34495e;
                }
                QPushButton:pressed {
                    background-color: #1abc9c;
                }
            """)
            layout.addWidget(btn)

        layout.addStretch()

    def toggle(self):
        """Anima a abertura/fechamento do drawer"""
        self.animation = QPropertyAnimation(self, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)

        if self.is_expanded:
            self.animation.setStartValue(250)
            self.animation.setEndValue(0)
        else:
            self.animation.setStartValue(0)
            self.animation.setEndValue(250)

        self.animation.start()
        self.is_expanded = not self.is_expanded


class NavigationRail(QFrame):
    """Sidebar compacta e sempre visível"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(80)
        self.setStyleSheet("""
            NavigationRail {
                background-color: #2c3e50;
                border-right: 2px solid #34495e;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(5)

        # Botões com ícones
        buttons_data = [("🏠", "Home"), ("📊", "Dashboard"), ("⚙️", "Config"),
            ("📁", "Files"), ("👤", "Profile"), ]

        for icon, tooltip in buttons_data:
            btn = QPushButton(icon)
            btn.setToolTip(tooltip)
            btn.setFixedSize(60, 60)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 24px;
                }
                QPushButton:hover {
                    background-color: #34495e;
                }
                QPushButton:pressed {
                    background-color: #1abc9c;
                }
            """)
            layout.addWidget(btn, alignment=Qt.AlignCenter)

        layout.addStretch()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Sidebar Demo")
        self.setGeometry(100, 100, 1000, 600)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Escolha o tipo de sidebar (comente/descomente conforme necessário)

        # Opção 1: Navigation Drawer (expansível)
        self.sidebar = NavigationDrawer()
        main_layout.addWidget(self.sidebar)

        # Opção 2: Navigation Rail (compacto)
        # self.sidebar = NavigationRail()
        # main_layout.addWidget(self.sidebar)

        # Área de conteúdo
        content_area = QWidget()
        content_area.setStyleSheet("background-color: #ecf0f1;")
        content_layout = QVBoxLayout(content_area)

        # Botão para toggle (apenas para NavigationDrawer)
        if isinstance(self.sidebar, NavigationDrawer):
            toggle_btn = QPushButton("☰ Menu")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
