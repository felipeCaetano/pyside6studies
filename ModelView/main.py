import sys
from PySide6.QtWidgets import QApplication
from model import TaskModel
from view import MainView
from repository import TaskRepository


app = QApplication(sys.argv)
repo = TaskRepository()
model = TaskModel(repo)
view = MainView(model)

view.button.clicked.connect(lambda: model.addTask(view.input.text()))
view.show()
sys.exit(app.exec())