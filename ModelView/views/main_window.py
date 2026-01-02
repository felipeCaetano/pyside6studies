from PySide6.QtWidgets import QMainWindow, QStackedWidget
from task_view import TaskView
from about_view import AboutView


class MainView(QMainWindow):
    def __init__(self, TaskModel):
        super().__init__()
        self.model = TaskModel
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.stack.setCurrentIndex(0)
        self.task_view = TaskView(self.model)
        self.about_view = AboutView()
        self.stack.addWidget(self.task_view)
        self.stack.addWidget(self.about_view)
