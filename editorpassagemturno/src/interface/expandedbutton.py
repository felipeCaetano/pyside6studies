from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class ExpandableButton(QWidget):
    """Botão que pode expandir para revelar sub-botões"""

    def __init__(self, icon, text, parent=None, slot=None):
        super().__init__(parent)
        self.is_expanded = False
        self.sub_buttons = []

        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Botão principal
        self.main_button = QPushButton(f"{text}  ▼")
        self.main_button.setIcon(icon)
        self.main_button.setStyleSheet("""
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
        self.main_button.clicked.connect(lambda: self.toggle(slot))
        self.main_layout.addWidget(self.main_button)

        # Container para sub-botões
        self.sub_container = QWidget()
        self.sub_container.setMaximumHeight(0)  # Começa escondido
        self.sub_container.setStyleSheet("background-color: #1a252f;")

        self.sub_layout = QVBoxLayout(self.sub_container)
        self.sub_layout.setContentsMargins(0, 0, 0, 0)
        self.sub_layout.setSpacing(0)

        self.main_layout.addWidget(self.sub_container)

    def add_sub_button(self, icon, text, callback=None):
        """Adiciona um sub-botão"""
        btn = QPushButton(f"{text}")
        btn.setIcon(icon)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #bdc3c7;
                text-align: left;
                padding: 12px 20px;
                padding-left: 40px;
                border: none;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2c3e50;
                color: white;
            }
            QPushButton:pressed {
                background-color: #16a085;
            }
        """)

        if callback:
            btn.clicked.connect(lambda: callback(text))

        self.sub_layout.addWidget(btn)
        self.sub_buttons.append(btn)
        return btn

    def toggle(self, slot):
        """Expande/colapsa os sub-botões com animação"""

        # Atualiza o ícone da seta
        current_text = self.main_button.text()
        if self.is_expanded:
            # Colapsar
            new_text = current_text.replace("▲", "▼")
            end_height = 0
        else:
            # Expandir
            new_text = current_text.replace("▼", "▲")
            # Calcula a altura necessária
            end_height = sum(
                btn.sizeHint().height() for btn in self.sub_buttons)

        self.main_button.setText(new_text)

        # Animação suave
        self.animation = QPropertyAnimation(self.sub_container,
                                            b"maximumHeight")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.setStartValue(self.sub_container.maximumHeight())
        self.animation.setEndValue(end_height)
        self.animation.start()

        self.is_expanded = not self.is_expanded

        if slot:
            self.main_button.clicked.connect(lambda: slot(current_text[:-3]))