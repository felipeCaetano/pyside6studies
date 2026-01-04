from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListView, \
    QLineEdit


class MainView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.setWindowTitle("Tasks ")
        self.model = model
        self.view = QListView()
        self.view.setModel(self.model)
        self.view.setEditTriggers(
            QListView.DoubleClicked
        )
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter a task")
        self.button = QPushButton("Submit")

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        self.setLayout(layout)
