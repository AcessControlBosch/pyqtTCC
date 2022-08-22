##################### IMPORTANDO AS BIBLIOTECAS E FUNÇÕES ################################
import sys
import datetime
import requests
from time import sleep
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QLabel, QLineEdit, QTableWidget
from PyQt5.QtGui import QIcon, QPixmap
import sqlite3

from Menu01 import Ui_Menu01
from Menu01_LIBERADO import Ui_Menu01_Liberado
from Menu02 import Ui_Menu02
from leitor import Ui_leitor

class Connection:

    #Construtor da class faz a conexão
    # def __init__(self, db):
    #     self.url = 'http://localhost:8000/'
    #     self.banco = sqlite3.connect(db)

    #Veriica se o usuario esta no banco de dados
    # def pesquisar_colaborador(self, idcard):
    #     print(idcard)
    #     self.json_response = requests.get(self.url + 'users/' + idcard).json()
    #
        print('oi')
    #     print(self.json_response['name'])
    #     cursor = self.banco.cursor()
        #função do SQL de seleção de dados

class Teste_leitor(QMainWindow, Ui_leitor):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.url = 'http://localhost:8000/'
        self.botao_avancar.clicked.connect(self.comeca)
        self.lineEdit_tag.setFocus()
        self.lineEdit_tag.returnPressed.connect(self.comeca)
        self.lineEdit_tag.setText("")
        #self.centralwidget.mouseReleaseEvent = lambda event: self.comeca


    def comeca(self):
        tag = self.lineEdit_tag.text()
        self.json_response = requests.get(self.url + 'users/' + tag).json()
        print(self.json_response['name'])
        menu01.setupUi(QMainWindow)
        QMainWindow.show()






        #
        # colaborador = banco_dados.pesquisar_colaborador(tag)[0]
        # colaborador2 = colaborador.split(" ")
        # banco_dados.coleta_dados()
        #
        #
        # Menu01.Label_Colaborador.setText(f'COLABORADOR: {colaborador2[0]} {colaborador2[-1]}')
        # Menu01.Label_EDV.setText(f"EDV: {banco_dados.pesquisar_colaborador(tag)[-1]}")
        # Menu02.Label_Colaborador.setText(f'COLABORADOR: {colaborador2[0]} {colaborador2[-1]}')
        # Menu02.Label_EDV.setText(f"EDV: {banco_dados.edv(tag)}")
        #
        # leitor.hide()
        # Menu01.show()


if __name__ == '__main__':
    import sys
    ap = QApplication(sys.argv)
    ap.setStyle("Fusion")
    leitor = Teste_leitor()
    leitor.show()
    menu001 = ''
    menu01 = Ui_Menu01().setupUi(menu001)
    sys.exit(ap.exec())