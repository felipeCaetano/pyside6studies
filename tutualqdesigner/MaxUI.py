# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'maxui.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(651, 641)
        self.actionCr_ditos = QAction(MainWindow)
        self.actionCr_ditos.setObjectName(u"actionCr_ditos")
        self.actionSobre = QAction(MainWindow)
        self.actionSobre.setObjectName(u"actionSobre")
        self.actionConectar = QAction(MainWindow)
        self.actionConectar.setObjectName(u"actionConectar")
        self.actionAbrir = QAction(MainWindow)
        self.actionAbrir.setObjectName(u"actionAbrir")
        self.actionSair = QAction(MainWindow)
        self.actionSair.setObjectName(u"actionSair")
        self.actionFormul_rio = QAction(MainWindow)
        self.actionFormul_rio.setObjectName(u"actionFormul_rio")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 651, 22))
        self.menuArquivo = QMenu(self.menubar)
        self.menuArquivo.setObjectName(u"menuArquivo")
        self.menuEditar = QMenu(self.menubar)
        self.menuEditar.setObjectName(u"menuEditar")
        self.menuAjuda = QMenu(self.menubar)
        self.menuAjuda.setObjectName(u"menuAjuda")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuArquivo.menuAction())
        self.menubar.addAction(self.menuEditar.menuAction())
        self.menubar.addAction(self.menuAjuda.menuAction())
        self.menuArquivo.addAction(self.actionConectar)
        self.menuArquivo.addAction(self.actionFormul_rio)
        self.menuArquivo.addAction(self.actionAbrir)
        self.menuArquivo.addAction(self.actionSair)
        self.menuAjuda.addAction(self.actionSobre)
        self.menuAjuda.addAction(self.actionCr_ditos)

        self.retranslateUi(MainWindow)
        self.actionSair.triggered.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionCr_ditos.setText(QCoreApplication.translate("MainWindow", u"Cr\u00e9ditos", None))
        self.actionSobre.setText(QCoreApplication.translate("MainWindow", u"Sobre", None))
        self.actionConectar.setText(QCoreApplication.translate("MainWindow", u"Conectar", None))
        self.actionAbrir.setText(QCoreApplication.translate("MainWindow", u"&Abrir", None))
        self.actionSair.setText(QCoreApplication.translate("MainWindow", u"Sair", None))
        self.actionFormul_rio.setText(QCoreApplication.translate("MainWindow", u"Formul\u00e1rio", None))
        self.menuArquivo.setTitle(QCoreApplication.translate("MainWindow", u"Arquivo", None))
        self.menuEditar.setTitle(QCoreApplication.translate("MainWindow", u"Editar", None))
        self.menuAjuda.setTitle(QCoreApplication.translate("MainWindow", u"Ajuda", None))
    # retranslateUi

