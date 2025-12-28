# repository.py
import sqlite3
from model import Task

class TaskRepository:
    def __init__(self, db_path="tasks.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                done INTEGER
            )
        """)

    def fetch_all(self):
        cur = self.conn.execute("SELECT id, title, done FROM tasks")
        return [
            Task(id, title, bool(done))
            for id, title, done in cur.fetchall()
        ]

    def add(self, title):
        cur = self.conn.execute(
            "INSERT INTO tasks (title, done) VALUES (?, 0)",
            (title,)
        )
        self.conn.commit()
        return cur.lastrowid
