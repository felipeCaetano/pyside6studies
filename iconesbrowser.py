import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QPushButton, QLabel, QScrollArea, QGroupBox)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor


class IconsDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Opções de Ícones no PySide6")
        self.setGeometry(100, 100, 900, 700)

        # Widget central com scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setSpacing(20)

        # Título
        title = QLabel("🎨 Guia Completo de Ícones no PySide6")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; padding: 20px;")
        layout.addWidget(title)

        # 1. Emojis Unicode (o que eu usei)
        emoji_group = self.create_emoji_section()
        layout.addWidget(emoji_group)

        # 2. Ícones do Sistema
        system_group = self.create_system_icons_section()
        layout.addWidget(system_group)

        # 3. Ícones de Arquivos
        file_group = self.create_file_icons_section()
        layout.addWidget(file_group)

        # 4. QtAwesome (recomendado!)
        qtawesome_group = self.create_qtawesome_section()
        layout.addWidget(qtawesome_group)

        # 5. Ícones Customizados
        custom_group = self.create_custom_icons_section()
        layout.addWidget(custom_group)

        layout.addStretch()

    def create_emoji_section(self):
        group = QGroupBox("1️⃣ Emojis Unicode (Simples, mas limitado)")
        layout = QVBoxLayout()

        info = QLabel("""
<b>Vantagens:</b> Não precisa de arquivos externos, fácil de usar
<b>Desvantagens:</b> Aparência varia por sistema, difícil de estilizar, não escala bem

<b>Exemplos:</b>
        """)
        layout.addWidget(info)

        emojis = [
            ("🏠", "Home"), ("📊", "Dashboard"), ("⚙️", "Settings"),
            ("📁", "Folder"), ("👤", "User"), ("🔍", "Search"),
            ("📧", "Email"), ("🔔", "Notification"), ("❤️", "Favorite"),
            ("🗑️", "Delete"), ("✏️", "Edit"), ("💾", "Save")
        ]

        emoji_layout = QVBoxLayout()
        for emoji, desc in emojis:
            btn = QPushButton(f"{emoji}  {desc}")
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px;
                    font-size: 14px;
                    background: #f0f0f0;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover { background: #e0e0e0; }
            """)
            emoji_layout.addWidget(btn)

        layout.addLayout(emoji_layout)

        # Link para mais emojis
        link = QLabel(
            '<a href="https://emojipedia.org">📌 Buscar mais emojis em emojipedia.org</a>')
        link.setOpenExternalLinks(True)
        link.setStyleSheet("padding: 10px; font-size: 12px;")
        layout.addWidget(link)

        group.setLayout(layout)
        return group

    def create_system_icons_section(self):
        group = QGroupBox("2️⃣ Ícones Padrão do Sistema (QStyle)")
        layout = QVBoxLayout()

        info = QLabel("""
<b>Vantagens:</b> Já incluídos no Qt, seguem o estilo do SO
<b>Desvantagens:</b> Opções limitadas, aparência varia por plataforma

<b>Código:</b> QStyle.StandardPixmap
        """)
        layout.addWidget(info)

        # Ícones do sistema disponíveis
        system_icons = [
            ("SP_FileIcon", "Arquivo"),
            ("SP_DirIcon", "Diretório"),
            ("SP_DialogOkButton", "OK"),
            ("SP_DialogCancelButton", "Cancelar"),
            ("SP_MessageBoxInformation", "Informação"),
            ("SP_MessageBoxWarning", "Aviso"),
            ("SP_MessageBoxCritical", "Erro"),
            ("SP_TrashIcon", "Lixeira"),
            ("SP_BrowserReload", "Recarregar"),
            ("SP_MediaPlay", "Play"),
            ("SP_MediaPause", "Pause"),
            ("SP_MediaStop", "Stop"),
        ]

        icons_layout = QVBoxLayout()
        style = self.style()

        for icon_name, desc in system_icons:
            btn = QPushButton(desc)
            # Pega o enum da classe QStyle, não da instância
            from PySide6.QtWidgets import QStyle
            pixmap_type = getattr(QStyle, icon_name)
            icon = style.standardIcon(pixmap_type)
            btn.setIcon(icon)
            btn.setIconSize(QSize(24, 24))
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px;
                    font-size: 14px;
                    background: #f0f0f0;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover { background: #e0e0e0; }
            """)
            icons_layout.addWidget(btn)

        layout.addLayout(icons_layout)
        group.setLayout(layout)
        return group

    def create_file_icons_section(self):
        group = QGroupBox("3️⃣ Ícones de Arquivos (SVG/PNG)")
        layout = QVBoxLayout()

        info = QLabel("""
<b>Vantagens:</b> Totalmente customizável, profissional
<b>Desvantagens:</b> Precisa gerenciar arquivos externos

<b>Código:</b>
<pre style='background: #f5f5f5; padding: 10px; border-radius: 5px;'>
icon = QIcon("icons/home.svg")
button.setIcon(icon)
button.setIconSize(QSize(32, 32))
</pre>

<b>🎨 Onde baixar ícones gratuitos:</b>
        """)
        info.setTextFormat(Qt.RichText)
        layout.addWidget(info)

        # Lista de recursos
        resources = [
            ("Material Icons", "https://fonts.google.com/icons",
             "8000+ ícones do Google"),
            ("FontAwesome", "https://fontawesome.com/icons",
             "2000+ ícones gratuitos"),
            ("Heroicons", "https://heroicons.com", "Ícones SVG minimalistas"),
            ("Feather Icons", "https://feathericons.com",
             "Ícones simples e limpos"),
            ("Phosphor Icons", "https://phosphoricons.com", "Ícones flexíveis"),
            ("Iconify", "https://icon-sets.iconify.design", "200.000+ ícones!"),
        ]

        for name, url, desc in resources:
            link = QLabel(f'• <b>{name}</b>: {desc}<br/>'
                          f'  <a href="{url}">{url}</a>')
            link.setOpenExternalLinks(True)
            link.setStyleSheet("padding: 5px; font-size: 12px;")
            link.setTextFormat(Qt.RichText)
            layout.addWidget(link)

        group.setLayout(layout)
        return group

    def create_qtawesome_section(self):
        group = QGroupBox("4️⃣ QtAwesome - Font Icons (⭐ RECOMENDADO!)")
        layout = QVBoxLayout()

        info = QLabel("""
<b>🌟 A MELHOR OPÇÃO!</b>
<b>Vantagens:</b> 7000+ ícones, customizável por código, escala perfeitamente
<b>Desvantagens:</b> Precisa instalar biblioteca extra

<b>Instalação:</b>
<pre style='background: #2c3e50; color: white; padding: 10px; border-radius: 5px;'>
pip install QtAwesome
</pre>

<b>Exemplo de uso:</b>
<pre style='background: #f5f5f5; padding: 10px; border-radius: 5px;'>
import qtawesome as qta

# Ícone simples
icon = qta.icon('fa5s.home')
button.setIcon(icon)

# Ícone colorido
icon = qta.icon('fa5s.heart', color='red')

# Ícone com animação
icon = qta.icon('fa5s.spinner', color='blue', animation=qta.Spin(button))
</pre>

<b>Ícones disponíveis:</b>
• FontAwesome 5/6 (fa5s, fa5r, fa6s)
• Material Design Icons (mdi, mdi6)
• Elusive Icons (ei)
• Phosphor (ph)
        """)
        info.setTextFormat(Qt.RichText)
        layout.addWidget(info)

        # Link para galeria
        link = QLabel(
            '<a href="https://github.com/spyder-ide/qtawesome">📚 Ver galeria completa no GitHub</a>')
        link.setOpenExternalLinks(True)
        link.setStyleSheet("padding: 10px; font-size: 14px; font-weight: bold;")
        layout.addWidget(link)

        # Exemplo prático (se QtAwesome estiver instalado)
        try:
            import qtawesome as qta

            example_label = QLabel("<b>Exemplos funcionais:</b>")
            layout.addWidget(example_label)

            examples = [
                ('fa5s.home', 'Home', 'blue'),
                ('fa5s.chart-line', 'Dashboard', 'green'),
                ('fa5s.cog', 'Settings', 'gray'),
                ('fa5s.folder', 'Folder', 'orange'),
                ('fa5s.user', 'User', 'purple'),
                ('fa5s.heart', 'Favorite', 'red'),
            ]

            for icon_name, text, color in examples:
                btn = QPushButton(text)
                btn.setIcon(qta.icon(icon_name, color=color))
                btn.setIconSize(QSize(24, 24))
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding: 10px;
                        font-size: 14px;
                        background: #f0f0f0;
                        border: none;
                        border-radius: 5px;
                    }
                    QPushButton:hover { background: #e0e0e0; }
                """)
                layout.addWidget(btn)

        except ImportError:
            note = QLabel(
                "⚠️ QtAwesome não instalado. Execute: pip install QtAwesome")
            note.setStyleSheet(
                "color: orange; padding: 10px; font-weight: bold;")
            layout.addWidget(note)

        group.setLayout(layout)
        return group

    def create_custom_icons_section(self):
        group = QGroupBox("5️⃣ Criar Ícones Programaticamente")
        layout = QVBoxLayout()

        info = QLabel("""
<b>Vantagens:</b> Controle total, sem arquivos externos
<b>Desvantagens:</b> Mais trabalhoso para ícones complexos

<b>Exemplo:</b> Criar ícone colorido com QPainter
        """)
        layout.addWidget(info)

        # Criar alguns ícones customizados
        colors = [
            (QColor("#e74c3c"), "Vermelho"),
            (QColor("#3498db"), "Azul"),
            (QColor("#2ecc71"), "Verde"),
            (QColor("#f39c12"), "Laranja"),
        ]

        for color, name in colors:
            btn = QPushButton(f"Ícone {name}")
            icon = self.create_colored_icon(color)
            btn.setIcon(icon)
            btn.setIconSize(QSize(24, 24))
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px;
                    font-size: 14px;
                    background: #f0f0f0;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover { background: #e0e0e0; }
            """)
            layout.addWidget(btn)

        group.setLayout(layout)
        return group

    def create_colored_icon(self, color):
        """Cria um ícone circular colorido"""
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(4, 4, 24, 24)
        painter.end()

        return QIcon(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IconsDemo()
    window.show()
    sys.exit(app.exec())