from PySide6.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QTextEdit
import sys

app = QApplication(sys.argv)

# Criar o widget de abas
tab_widget = QTabWidget()

# Criar editores de texto DIFERENTES para cada aba
editor1 = QTextEdit()
editor1.setPlaceholderText("Digite algo na primeira aba...")

editor2 = QTextEdit()
editor2.setPlaceholderText("Digite algo na segunda aba...")

editor3 = QTextEdit()
editor3.setPlaceholderText("Digite algo na terceira aba...")

# Criar widgets para cada aba
aba1 = QWidget()
layout1 = QVBoxLayout()
layout1.addWidget(editor1)
aba1.setLayout(layout1)

aba2 = QWidget()
layout2 = QVBoxLayout()
layout2.addWidget(editor2)
aba2.setLayout(layout2)

aba3 = QWidget()
layout3 = QVBoxLayout()
layout3.addWidget(editor3)
aba3.setLayout(layout3)

# Adicionar as abas ao QTabWidget
tab_widget.addTab(aba1, "Primeira")
tab_widget.addTab(aba2, "Segunda")
tab_widget.addTab(aba3, "Terceira")

# Função que é chamada quando a aba muda
def ao_trocar_aba(index):
    # Capturar o nome da aba atual
    nome_aba = tab_widget.tabText(index)
    
    # Pegar o editor da aba atual
    widget_aba = tab_widget.widget(index)
    editor_atual = widget_aba.findChild(QTextEdit)
    
    if editor_atual:
        editor_atual.setText(f"Você está na aba: {nome_aba}")

# Conectar o sinal de mudança de aba
tab_widget.currentChanged.connect(ao_trocar_aba)

tab_widget.setWindowTitle("Abas com Editores de Texto")
tab_widget.resize(500, 400)
tab_widget.show()

sys.exit(app.exec())