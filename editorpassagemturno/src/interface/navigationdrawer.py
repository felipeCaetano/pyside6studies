from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
import qtawesome as qta

from editorpassagemturno.src.interface.expandedbutton import ExpandableButton


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
        self.is_expanded = True

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

        # layout.addStretch()

    def add_menu_buttons(self, buttons_data: list):
        text, icon_name, color, slot = buttons_data
        btn = QPushButton(text)
        btn.setStyleSheet(
            """QPushButton {
                    background-color: transparent;
                    color: white;
                    text-align: left;
                    padding: 15px 20px;
                    border: none;
                    font-size: 14px;
                }
                QPushButton:hover { background-color: #34495e;}
                QPushButton:pressed {background-color: #1abc9c;}
                """)
        try:
            btn.setIcon(qta.icon(icon_name, color=color))
            btn.setIconSize(QSize(24, 24))
        except Exception:
            btn.setIconSize(QSize(24, 24))
            btn.setIcon(qta.icon('mdi6.square-rounded', color=color))
        btn.clicked.connect(lambda: slot(text))
        self.layout().addWidget(btn)

    def add_expandeble_buttons(self, buttons_data: list):
        text, icon, subbuttons, slots, main_slot = buttons_data
        btn = ExpandableButton(icon, text, slot=main_slot)
        for index, subbutton in enumerate(subbuttons):
            sbu_text, sbu_icon = subbutton
            btn.add_sub_button(sbu_icon, sbu_text, slots[index])
        self.layout().addWidget(btn)

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
