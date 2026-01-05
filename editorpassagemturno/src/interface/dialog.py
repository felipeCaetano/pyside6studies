from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QLabel, QVBoxLayout,
                               QTextEdit)


class PasteDialog(QDialog):
    text_entry = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Colar Passagem de Turno:")
        qbtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(qbtn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        self.text = QTextEdit()
        self.text.setPlaceholderText('Cole sua passagem aqui...')
        self.setGeometry(200, 300, 500, 300)
        layout.addWidget(self.text)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def accept(self, /):
        self.text_entry.emit(self.text.toPlainText())
