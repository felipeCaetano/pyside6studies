import sys

import qtawesome as qta
from PySide6.QtCore import Qt, Slot, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QLabel, QFileDialog,
                               QTextEdit, QDialog, QMessageBox)

from editorpassagemturno.src.interface.navigationdrawer import NavigationDrawer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de Passagem de Turno")
        self.setGeometry(100, 100, 1000, 600)
        self.menu = self.menuBar()
        self.create_menubar()
        self.status_bar = self.statusBar()
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = NavigationDrawer()
        main_layout.addWidget(self.sidebar)

        # Área de conteúdo
        content_area = QWidget()
        content_area.setStyleSheet("background-color: #ecf0f1;")
        content_layout = QVBoxLayout(content_area)

        toggle_btn = QPushButton("☰")
        toggle_btn.setFixedSize(100, 40)
        toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        toggle_btn.clicked.connect(self.sidebar.toggle)
        content_layout.addWidget(toggle_btn,
                                 alignment=Qt.AlignLeft | Qt.AlignTop)

        #sidebar text, icon_name, color, slot
        btn_conf = ["Configuração",
                    qta.icon(
                        "ri.list-check",
                        options=[{'scale_factor': 1.5}]),
                    [
                        ('Serviços Auxiliares',
                         qta.icon(
                             'mdi6.generator-stationary',
                             options=[{'scale_factor': 1.5}]
                         )),
                        ('Comunicação',
                         qta.icon('mdi.phone-in-talk',
                             options=[{'scale_factor': 1.5}]
                                  )),
                        ('Atenção',
                         qta.icon('ph.circle-wavy-warning',
                             options=[{'scale_factor': 1.5}]
                                  ))
                    ],
                    [self.show_config, self.show_config, self.show_config],
                    self.show_config
                    ]
        self.sidebar.add_expandeble_buttons(btn_conf)
        btn_nct = [
            "NCT", "ph.thermometer-hot-light", "orange",  self.show_config]
        self.sidebar.add_menu_buttons(btn_nct)
        btn_obs = [
            "Observações", 'fa5s.exclamation-triangle', 'yellow',
            self.show_config]
        self.sidebar.add_menu_buttons(btn_obs)
        btn_inter = [
            'Intervenções',
            qta.icon('ri.tools-fill'),
            [('Em Andamento',
              qta.icon(
                  'ei.hourglass',
                  options=[{'scale_factor': 1.5}]
              )),
             ('Suspensas',
              qta.icon(
                  'mdi6.timer-pause',
                  options=[{'scale_factor': 1.5}]
              )),
             ('Entregues',
              qta.icon(
                  'mdi6.file-document-check-outline',
                  options=[{'scale_factor': 1.5}]
              )),
             ('Devolvidas',
              qta.icon(
                  'mdi6.file-document-remove-outline',
                  options=[{'scale_factor': 1.5}]
              )),
             ],
            [self.show_config,self.show_config,self.show_config,
             self.show_config],
            self.show_config
        ]
        self.sidebar.add_expandeble_buttons(btn_inter)
        btn_ocur = [
            'Ocorrências', 'msc.report', 'white', self.show_config
        ]
        self.sidebar.add_menu_buttons(btn_ocur)
        btn_notas = [
            'Notas', 'mdi6.clipboard-alert-outline', 'yellow', self.show_config
        ]
        self.sidebar.add_menu_buttons(btn_notas)
        btn_act = [
            'Ações Operacionais', 'msc.github-action', 'white', self.show_config
        ]
        self.sidebar.add_menu_buttons(btn_act)
        btn_oth = [
            'Outras Ações', '', 'black', self.show_config
        ]
        self.sidebar.add_menu_buttons(btn_oth)
        self.sidebar.layout().addStretch()
        # Conteúdo principal
        self.title = QLabel("Conteúdo Principal")
        self.title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
            padding: 20px;
        """)
        content_layout.addWidget(self.title, alignment=Qt.AlignLeft)

        # Editor
        self.editor = QTextEdit(
            "Tela inicial - exibirá o conteúdo da passagem de turno")
        self.editor.setStyleSheet("""
            QTextEdit {
                font-size: 16px;
                color: #2c3e50;
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        self.editor.document().contentsChanged.connect(
            self.document_was_modified)
        content_layout.addWidget(self.editor)

        main_layout.addWidget(content_area, stretch=1)
        self.status_bar.showMessage("Pronto", 2000)

    def create_menubar(self):
        menu_file = self.menu.addMenu("&Arquivo")

        open_action = QAction("Abrir", menu_file)
        open_action.setShortcut("Ctrl+O")
        open_action.setIcon(
            qta.icon(
                "mdi6.folder-open",
                options=[{'scale_factor': 1.5}]
            )
        )
        open_action.triggered.connect(self.open)
        menu_file.addAction(open_action)

        save_action = QAction("Salvar", menu_file)
        save_action.setShortcut("Ctrl+S")
        save_action.setIcon(
            qta.icon(
                "mdi6.content-save-outline",
                options=[{'scale_factor': 1.5}]
            )
        )
        save_action.triggered.connect(self.save)
        menu_file.addAction(save_action)

        paste_action = QAction("Colar", menu_file)
        paste_action.setShortcut("Ctrl+V")
        paste_action.setIcon(
            qta.icon(
                "mdi6.content-paste",
                options=[{'scale_factor': 1.5}]
            )
        )
        paste_action.triggered.connect(self.paste)
        menu_file.addAction(paste_action)

        menu_file.addSeparator()

        export_action = QAction("Exportar", menu_file)
        export_action.setShortcut("Ctrl+E")
        export_action.setIcon(
            qta.icon(
                'mdi6.file-export',
                options=[{'scale_factor': 1.5}]
            )
        )
        export_action.triggered.connect(self.export_file)
        menu_file.addAction(export_action)

        print_action = QAction("Imprimir", menu_file)
        print_action.setShortcut("Ctrl+E")
        print_action.setIcon(
            qta.icon(
                'mdi6.printer-outline',
                options=[{'scale_factor': 1.5}]
            )
        )
        print_action.triggered.connect(self.print)
        menu_file.addAction(print_action)

        exit = QAction("Sair", self)
        exit.setShortcut("Ctrl+Q")
        exit.setIcon(
            qta.icon(
                "mdi6.exit-to-app",
            options=[{'scale_factor': 1.5}]
            )
        )
        menu_file.addSeparator()
        menu_file.addAction(exit)
        exit.triggered.connect(self.close)

    @Slot()
    def close(self, /):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Sair")
        dlg.setText("Deseja sair?\n\nSeu trabalho poderá ser perdido")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Warning)
        response = dlg.exec()
        if response == QMessageBox.Yes:
            super().close()
        else:
            return

    @Slot()
    def document_was_modified(self):
        self.setWindowModified(self.editor.document().isModified())

    @Slot()
    def export_file(self):
        ...

    @Slot()
    def open(self):
        file, filtro = QFileDialog.getOpenFileName(self, "Abrir Arquivo")

    @Slot()
    def paste(self):
        ...

    @Slot()
    def print(self):
        ...

    @Slot()
    def save(self):
        ...

    @Slot()
    def show_config(self, value):
        if value in ["Comunicação", "Atenção", "Serviços Auxiliares"]:
            self.title.setText(f"Configuração - {value}")
        elif value in ["Em Andamento", "Suspensas", "Entregues", "Devolvidas"]:
            self.title.setText(f"Intervenções {value}")
        else:
            self.title.setText(f"{value}")
        self.sidebar.toggle()

    @Slot()
    def show_aux_config(self, value):
        self.title.setText(f"Configuração - {value}")
        self.sidebar.toggle()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
