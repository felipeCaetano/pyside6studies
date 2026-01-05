import logging
import sys

from PySide6.QtWidgets import QApplication

from domain.passagemturnoparser import PassagemTurnoParser
from interface.mainwindow import MainWindow

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


class MainApp(QApplication):
    passagem_turno = None
    current_field = None

    def __init__(self, *args):
        super().__init__(sys.argv)
        self.ui = MainWindow()
        self.ui.file_opened.connect(self.parse_file)
        self.ui.tab_changed.connect(self.load_fields)
        self.ui.sidebar_clicked.connect(self.load_fields)
        self._load_last_turn()

    def parse_file(self, file):
        ok = PassagemTurnoParser.parse_passagem_turno(file)
        if not ok:
            logging.error(f"Falha ao processar arquivo: {file}")
            self.ui.status_bar.showMessage("Falha ao processar arquivo", 2000)
        else:
            self.passagem_turno = PassagemTurnoParser.get_passagem_turno(
                'passagem_turno.json'
                )
            if self.passagem_turno:
                self.load_fields()
                self.ui.status_bar.showMessage("Pronto", 2000)
            else:
                self.ui.status_bar.showMessage("Erro", 2000)
    
    def load_fields(self, field=None):
        if field:
            self.current_field = field

        if self.passagem_turno:
            if self.current_field == "NOTAS":
                self.current_field = 'NM EMITIDAS'
            elif self.current_field == "AÇÕES OPERACIONAIS":
                self.current_field = "OUTRAS AÇÕES OPERACIONAIS"
            for index, se_name in enumerate(self.passagem_turno.keys(), -1):
                editor = self.ui.tabs.get_editor_by_index(index)
                if editor:
                    if (self.current_field == "OUTRAS INFORMAÇÕES" or
                            self.current_field == "OUTRAS AÇÕES OPERACIONAIS"):
                        se_name = '_global'
                        editor.setPlainText(
                            "\n".join(
                                self.passagem_turno[se_name][
                                    PassagemTurnoParser.get_sessao_map(
                                        self.current_field
                                    )
                                ]
                            )
                        )
                    else:
                        editor.setPlainText(
                            "\n".join(
                                self.passagem_turno[se_name][
                                    PassagemTurnoParser.get_sessao_map(
                                        self.current_field
                                    )
                            ]
                        )
                    )
        else:
            self.ui.status_bar("Pronto", 2000)
            return

    def _load_last_turn(self):
        self.passagem_turno = PassagemTurnoParser.get_passagem_turno(
                'passagem_turno.json'
            )
        if self.passagem_turno:
            self.load_fields()


if __name__ == "__main__":
    app = MainApp(sys.argv)
    app.ui.show()
    sys.exit(app.exec())
