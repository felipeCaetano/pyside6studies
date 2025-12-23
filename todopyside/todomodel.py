import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

tick = QtGui.QImage('tick.png')

class TodoModel(QtCore.QAbstractListModel):
    def __init__(self, todos=None):
        super().__init__()
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            status, text = self.todos[index.row()]
            return text
        if role ==Qt.DecorationRole:
            status, _ = self.todos[index.row()]
            if status:
                return QtGui.QColor('green')

    def rowCount(self, index):
        return len(self.todos)
