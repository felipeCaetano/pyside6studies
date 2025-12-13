from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                               QTextEdit, QFrame)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPalette, QColor
import sys

class ModernWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 - Interface Moderna")
        self.setGeometry(100, 100, 800, 600)
        
        # Tema escuro moderno
        self.setup_dark_theme()
        
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("Dashboard Moderno")
        header.setFont(QFont("Segoe UI", 24, QFont.Bold))
        header.setStyleSheet("color: #ffffff; padding: 10px;")
        layout.addWidget(header)
        
        # Cards container
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)
        
        # Card 1
        card1 = self.create_card("Usuários", "1,234", "#6366f1")
        cards_layout.addWidget(card1)
        
        # Card 2
        card2 = self.create_card("Vendas", "R$ 45.6k", "#10b981")
        cards_layout.addWidget(card2)
        
        # Card 3
        card3 = self.create_card("Produtos", "89", "#f59e0b")
        cards_layout.addWidget(card3)
        
        layout.addLayout(cards_layout)
        
        # Seção de input
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        
        title_label = QLabel("Adicionar Novo Item")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        input_layout.addWidget(title_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome do item")
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #0f172a;
                border: 2px solid #334155;
                border-radius: 8px;
                padding: 12px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #6366f1;
            }
        """)
        input_layout.addWidget(self.name_input)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("Adicionar")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4f46e5;
            }
            QPushButton:pressed {
                background-color: #4338ca;
            }
        """)
        add_btn.clicked.connect(self.add_item)
        buttons_layout.addWidget(add_btn)
        
        clear_btn = QPushButton("Limpar")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #475569;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #64748b;
            }
        """)
        clear_btn.clicked.connect(self.clear_items)
        buttons_layout.addWidget(clear_btn)
        
        input_layout.addLayout(buttons_layout)
        layout.addWidget(input_frame)
        
        # Área de texto para resultados
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #1e293b;
                border: 2px solid #334155;
                border-radius: 12px;
                padding: 15px;
                color: #e2e8f0;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.output)
        
    def create_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        card.setMinimumHeight(120)
        
        card_layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 12))
        title_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        value_label.setStyleSheet("color: #ffffff;")
        
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        card_layout.addStretch()
        
        # Animação no hover
        card.enterEvent = lambda e: self.animate_card(card, 1.05)
        card.leaveEvent = lambda e: self.animate_card(card, 1.0)
        
        return card
    
    def animate_card(self, card, scale):
        # Simples efeito visual (PySide6 permite animações mais complexas)
        pass
    
    def add_item(self):
        text = self.name_input.text().strip()
        if text:
            self.output.append(f"✓ Item adicionado: {text}")
            self.name_input.clear()
    
    def clear_items(self):
        self.output.clear()
    
    def setup_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }
            QWidget {
                background-color: #0f172a;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernWindow()
    window.show()
    sys.exit(app.exec())