from dataclasses import dataclass

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt


@dataclass
class Task:
    id: int
    title: str
    done: bool


class TaskModel(QAbstractListModel):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository
        self._tasks = self.repository.fetch_all()

    def rowCount(self, parent=None):
        return len(self._tasks)

    def data(self, index, role):
        if not index.isValid():
            return None

        task = self._tasks[index.row()]

        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return task.title

        if role == Qt.CheckStateRole:
            result = Qt.CheckState.Checked if task.done \
                else Qt.CheckState.Unchecked
            return result

    def addTask(self, title):
        task_id = self.repository.add(title)
        self.beginInsertRows(QModelIndex(), len(self._tasks), len(self._tasks))
        self._tasks.append(Task(task_id, title, False))
        self.endInsertRows()

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return (
                Qt.ItemIsEnabled
                | Qt.ItemIsSelectable
                | Qt.ItemIsUserCheckable
                | Qt.ItemIsEditable
        )

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        task = self._tasks[index.row()]

        if role == Qt.EditRole:
            if not isinstance(value, str):
                return False
            task.title = value

        elif role == Qt.CheckStateRole:
            if not isinstance(value, int):
                return False
            task.done = (value == Qt.Checked.value)
        return False
