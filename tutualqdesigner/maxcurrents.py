import sys
from datetime import datetime

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton
from MaxUI import Ui_MainWindow
from LoginUI import Ui_Dialog
from FormUI import Ui_FormDialog


class FormDialog(QDialog, Ui_FormDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Insira os campos")
        self.populate_comboboxes()

    def _gerar_ultimos_12_meses(self):
        """ Gera lista dos 12 meses do ano em vigor."""
        meses_ano = {
            '1': '-Janeiro',
            '2': '-Fevereiro',
            '3': '-Março',
            '4': '-Abril',
            '5': '-Maio',
            '6': '-Junho',
            '7': '-Julho',
            '8': '-Agosto',
            '9': '-Setembro',
            '10': '-Outubro',
            '11': '-Novembro',
            '12': '-Dezembro',
        }
        data = datetime.now()
        
        meses = []
        for i, mes in meses_ano.items():
            meses.append(
                f"{data.year}/{int(i):02d}{mes}"
            )
        return meses

    def populate_comboboxes(self):
        self.comboBox.addItems(self._gerar_ultimos_12_meses())
        self.comboBox_2.addItems([
            "Corrente Elétrica", 
        "Potência Ativa",
        "Potência Reativa",
        "Tensão Elétrica",
        "Frequência Elétrica",
        "LTC",
        "Vazão",
        "Cota Montante",
        "Cota Jusante"]
        )


class LoginDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Login")
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.validate_and_accept)
        self.label_4.clear()  # Limpar mensagem de erro
    
    def validate_and_accept(self):
        email = self.lineEdit.text().strip()
        senha = self.lineEdit_2.text().strip()
        
        if not email or not senha:
            self.label_4.setText("Preencher todos os campos")
            self.label_4.setStyleSheet("color: red;  font-size:12pt; font-weight:700;")
            return  # Dialog NÃO fecha
        
        # Validação passou
        self.label_4.clear()
        self.accept()  # Dialog fecha com sucesso


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Correntes Máximas")
        self.dlg_login = LoginDialog(self)
        self.actionConectar.triggered.connect(self.open_login_dialog)
        self.actionFormul_rio.triggered.connect(self.open_form_dialog)
        self.actionSair.triggered.connect(self.close)
    
    def open_login_dialog(self):
        dialog = LoginDialog(self)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            # Aqui você pode acessar os dados do dialog antes dele ser destruído
            email = dialog.lineEdit.text().strip()
            senha = dialog.lineEdit_2.text().strip()
            self.connect(email, senha)
    
    def connect(self, email, senha):
        print(f"Estabelecendo conexão com: {email}")
        # Aqui você implementa a lógica de conexão
            

    def open_form_dialog(self):
        dialog = FormDialog(self)
        result = dialog.exec()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("Correntes Máximas")
    app.setOrganizationName("Axia")
    app.setApplicationVersion("1.0.0")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
    