from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QTabWidget, QWidget, QVBoxLayout, QTextEdit

class SETabs(QWidget):
    tab_was_changed = Signal(int)
    def __init__(self, se_names):
        super().__init__()
        self.se_names = se_names
        self.title = QLabel("Conteúdo Principal")
        self.title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        """)
        main_layout = QVBoxLayout()
        # Criar o widget de abas
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;""")
        self.create_tabs()
        # Adicionar tab_widget ao layout principal
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)
        self.tab_widget.currentChanged.connect(self.on_change_tab)

    def create_tabs(self):
        for sename in self.se_names:
            aba = QWidget()
            editor = QTextEdit()
            editor.setStyleSheet("""
            QTextEdit {
                font-size: 16px;
                color: #2c3e50;
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
            }
        """)
            layout = QVBoxLayout()
            layout.addWidget(editor)
            aba.setLayout(layout)
            self.tab_widget.addTab(aba, sename)
    
    def on_change_tab(self, index):
        self.tab_was_changed.emit(index)

    # Métodos úteis para capturar o editor
    def get_current_editor(self):
        """Retorna o editor da aba atual"""
        current_widget = self.tab_widget.currentWidget()
        return current_widget.findChild(QTextEdit)
    
    def get_editor_by_index(self, index):
        """Retorna o editor de uma aba específica"""
        widget = self.tab_widget.widget(index)
        if widget:
            return widget.findChild(QTextEdit)
        return None
    
    def get_current_tab_name(self):
        """Retorna o nome da aba atual"""
        return self.tab_widget.tabText(self.tab_widget.currentIndex())

    #metodo para capturar o titulo
    def get_title(self):
        return self.title