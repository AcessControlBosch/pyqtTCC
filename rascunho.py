##################### IMPORTANDO AS BIBLIOTECAS E FUNÇÕES ################################
import sys
import datetime
import requests
from time import sleep
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QLabel, QLineEdit, QTableWidget
from PyQt5.QtGui import QIcon, QPixmap

import sqlite3
"""banco = sqlite3.connect("Banco.db")
cursor = banco.cursor()"""

"""""
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
led_vermelha = 12
led_verde = 16
GPIO.setup(led_verde, GPIO.OUT)
GPIO.setup(led_vermelha, GPIO.OUT)

GPIO.output(led_verde, False)
GPIO.output(led_vermelha, True)
"""""

##################### IMPORTANDO AS CLASSES DOS ARQUIVOS DE TELAS ################################
from Menu01 import Ui_Menu01
from Menu01_LIBERADO import Ui_Menu01_Liberado
from Menu02 import Ui_Menu02
from Caderno_Verde_Atencao import Ui_Atencao
from Liberação_Segurança import Ui_Liberacao_Seguranca
from Liberação_Meio_Ambiente import Ui_Liberacao_Meio_Ambiente
from Documentos_Menu import Ui_documentos_menu
from Documentos_Documentos_de_pecas_menuu import Ui_documentos_documentos_de_pecas_menu
from documentos_documentos_de_pecas_1 import Ui_peca01
from documentos_documentos_de_pecas_2 import Ui_peca02
from documentos_documentos_de_pecas_3 import  Ui_peca03
from documentos_diagrama_eletrico_imagens import  Ui_documentos_diagrama_eletrico
from Documentos_mapa_de_risco import Ui_mapa_de_riscos
from Aviso_liberacao import Ui_Aviso_Liberacao
from Interface_didatica_menu import Ui_interface_didatica_menu
from Interface_didatica_menu_botoes_botoeira import Ui_interface_didatica_menu_botoes
from Interface_didatica_finalidade import  Ui_interface_didatica_finalidade
from Interface_didatica_menu_botao_emergencia import Ui_interface_didatica_menu_botao_emergencia
from Registros_menu import Ui_Registros_menu
from Cadastros_menu import Ui_cadastros_menu
from Cadastros_menu_adicionar import Ui_cadastros_classes
from Cadastros_adicionar_ficha01 import Ui_cadastros_adicionar_ficha01
from Usuario_registrado import Ui_Usuario_registrado

from leitor import Ui_leitor

colaborador = "Dorigon" #cursor.execute("SELECT Nome FROM Dados WHERE ID = 2")
#banco.commit()
edv = "92896201"
verifica = bool
hoje = datetime.date.today()
print(hoje)
tag = "011"


class Connection:

    #Construtor da class faz a conexão
    def __init__(self, db):
        self.url = 'http://localhost:8000/'
        self.banco = sqlite3.connect(db)
        self.idColaborador =''
        self.nameColadorador = ''
        self.edvColaborador =''
        self.courseColaborador =''
        # self.idColaborador =''

    #Veriica se o usuario esta no banco de dados
    def pesquisar_colaborador(self, idcard):
        print(idcard)
        self.json_response_name = requests.get(self.url + 'users/' + idcard).json()
        self.nameColadorador = self.json_response_name['name']
        self.idColaborador = self.json_response_name['id']
        self.edvColaborador = self.json_response_name['EDV']

        print(self.nameColadorador)
        print(self.idColaborador)
        print(self.edvColaborador)

        cursor = self.banco.cursor()
        #função do SQL de seleção de dados



        # consulta= f"SELECT Nome, EDV FROM Usuarios WHERE ID_Card ='{int(idcard)}'"
        # cursor.execute(consulta)
        # nome = cursor.fetchall()
        #
        # cursor.close()
        # print(nome)
        # print(nome[0])
        return self.nameColadorador

    def coleta_dados (self):
        cursor = self.banco.cursor()
        consulta = ("SELECT Nome, EDV, Classe FROM Usuarios")
        cursor.execute(consulta)
        lista = cursor.fetchall()
        cursor.close()
        # print("lista:",lista)
        return lista

    def edv(self, idcard):
        cursor = self.banco.cursor()
        consulta = f"SELECT EDV FROM Usuarios WHERE ID_Card ='{int(idcard)}'"
        cursor.execute(consulta)
        edv = cursor.fetchone()
        cursor.close()
        print(edv)
        return edv[0]

    def adicionar_cadastro(self, tag_cartao, nome, classe, edv):
        cursor = self.banco.cursor()
        adicionar = ("INSERT INTO Dados (ID_Cartao, Nome, Classe, EDV)  VALUES ('" + tag_cartao + "','" + nome + "','" + classe + "'," + edv + ")")  # inserir Dados
        cursor.execute(adicionar)
        self.banco.commit()
        cursor.close()
        return print("Adicionado")






class Teste_leitor(QMainWindow, Ui_leitor):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_avancar.clicked.connect(self.comeca)
        self.lineEdit_tag.setFocus()
        self.lineEdit_tag.returnPressed.connect(self.comeca)
        self.lineEdit_tag.setText("")
        #self.centralwidget.mouseReleaseEvent = lambda event: self.comeca


    def comeca(self):
        tag = self.lineEdit_tag.text()
        print('tag',tag)
        print("leitor nameColadorador", self.nameColadorador)
        # colaborador = banco_dados.pesquisar_colaborador(tag)[0]
        colaborador2 = self.nameColadorador.split(" ")
        print(colaborador2)
        banco_dados.coleta_dados()


        Menu01.Label_Colaborador.setText(f'COLABORADOR: {colaborador2[0]} {colaborador2[-1]}')
        Menu01.Label_EDV.setText(f"EDV: {banco_dados.pesquisar_colaborador(tag)[-1]}")
        Menu02.Label_Colaborador.setText(f'COLABORADOR: {colaborador2[0]} {colaborador2[-1]}')
        Menu02.Label_EDV.setText(f"EDV: {banco_dados.edv(tag)}")

        leitor.hide()
        Menu01.show()


        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">BOTÃO PARA TRAVAR PEÇA</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Ao pressionar o botão, dois pistões pneumáticos \ntravam a peça na posição estabelecida pelo usuário.\n\n")

    def botao_05(self):
        self.label_indicacao.setText("5")
        self.label_titulo.setStyleSheet("border-style: outset;\n" "border-color: rgb(0, 0, 0);\n""border-width:6px;\n""\n""\n""font: 75 30pt \"Bosch Sans Bold\";\n""background-color: rgb(0,0,0);")
        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">BOTÃO RESET</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Botão necessário para reiniciar os processos da \nmáquina caso ocorra alguma falha, como a tentativa de \nabrir as portas de segurança durante a operação, ou ao \npressionar o botão de emergência.")

    def botao_emergencia(self):
        interface_menu_botao_emergencia.show()
        interface_menu_botoes.hide()

    def home(self):
        interface_menu.show()
        interface_menu_botoes.hide()

class Interface_botao_emergencia (QMainWindow, Ui_interface_didatica_menu_botao_emergencia):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)
        self.botao_seta_esquerda.clicked.connect(self.botoeira)

    def home(self):
        interface_menu.show()
        interface_menu_botao_emergencia.hide()

    def botoeira(self):
        interface_menu_botoes.show()
        interface_menu_botao_emergencia.hide()


class Interface_finalidade(QMainWindow, Ui_interface_didatica_finalidade):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)

    def home(self):
        interface_menu.show()
        interface_menu_finalidade.hide()

class Registros_menu (QMainWindow, Ui_Registros_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)

    def home(self):
        Menu01.show()
        registros_menu.hide()

class Cadastros_menu(QMainWindow, Ui_cadastros_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_voltar.clicked.connect(self.home)
        self.botao_adicionar.clicked.connect(self.escolher_classe)

        self.tabela.setColumnCount(3)
        self.tabela.setColumnWidth(0, 380)
        self.tabela.setColumnWidth(1, 250)
        self.tabela.setColumnWidth(2, 200)
        self.tabela.setHorizontalHeaderLabels(["NOME", "EDV", "CLASSE"])

        self.loaddata()



    def loaddata(self):
        lista = banco_dados.coleta_dados()
        row = 0
        self.tabela.setRowCount(len(lista))
        for x in lista:
            self.tabela.setItem(row, 0, QTableWidgetItem(x[0]))
            self.tabela.setItem(row, 1, QTableWidgetItem(str(x[1])))
            self.tabela.setItem(row, 2, QTableWidgetItem(x[2]))

            row = row + 1



        #https://www.youtube.com/watch?v=YySB6tkjZ7Y
        #https://www.youtube.com/watch?v=xL2NdSubiNY





    def escolher_classe(self):
        cadastros_menu_adicionar.show()
        cadastros_menu.hide()

    def home(self):
        Menu02.show()
        cadastros_menu.hide()



class Cadastros_menu_adicionar(QMainWindow, Ui_cadastros_classes):
    def __init__ (self):
        super().__init__()
        super().setupUi(self)
        self.botao_voltar.clicked.connect(self.home)
        self.botao_aprendiz.clicked.connect(self.aprendiz)
        self.botao_meio_oficial.clicked.connect(self.meio_oficial)
        self.botao_manutentor.clicked.connect(self.manutentor)
        self.botao_responsavel.clicked.connect(self.responsavel)
        self.imagem_aprendiz = QPixmap("imagens\Aprendiz_02.png")
        self.imagem_meio_oficial = QPixmap("imagens\Meio_oficial_02.png")
        self.imagem_manutentor = QPixmap("imagens\Manutentor_02.png")
        self.imagem_responsavel = QPixmap("imagens\Responsavel_02.png")

    def aprendiz(self):
        cadastros_menu_adicionar_ficha_01.classe = "Aprendiz"
        cadastros_menu_adicionar_ficha_01.label_imagem_classe.setPixmap(self.imagem_aprendiz)
        cadastros_menu_adicionar_ficha_01.show()
        cadastros_menu_adicionar.hide()

    def meio_oficial (self):
        cadastros_menu_adicionar_ficha_01.classe = "Meio-Oficial"
        cadastros_menu_adicionar_ficha_01.label_imagem_classe.setPixmap(self.imagem_meio_oficial)
        cadastros_menu_adicionar_ficha_01.show()
        cadastros_menu_adicionar.hide()

    def manutentor(self):
        cadastros_menu_adicionar_ficha_01.classe = "Manutentor"
        cadastros_menu_adicionar_ficha_01.label_imagem_classe.setPixmap(self.imagem_manutentor)
        cadastros_menu_adicionar_ficha_01.show()
        cadastros_menu_adicionar.hide()

    def responsavel(self):
        cadastros_menu_adicionar_ficha_01.classe = "Responsável"
        cadastros_menu_adicionar_ficha_01.label_imagem_classe.setPixmap(self.imagem_responsavel)
        cadastros_menu_adicionar_ficha_01.show()
        cadastros_menu_adicionar.hide()

    def home(self):
        cadastros_menu.show()
        cadastros_menu_adicionar.hide()



class Cadastros_menu_adicionar_ficha01(QMainWindow, Ui_cadastros_adicionar_ficha01):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_cancelar.clicked.connect(self.home)
        self.botao_avancar.clicked.connect(self.teste)
        self.classe = " "


    def teste(self):
        self.nome = self.lineEdit_nome.text()
        self.edv = int(self.lineEdit_edv.text())
        banco_dados.adicionar_cadastro(tag,self.nome,self.classe,str(self.edv))
        print(self.nome)
        print(self.edv)
        print(self.classe)
        usuario_registrado.show()
        #AQUI FALTA O DELAY ENTRE AS TELAS
        usuario_registrado.hide()



    def home(self):
        cadastros_menu_adicionar.show()
        cadastros_menu_adicionar_ficha_01.hide()

class Usuario_registrado (QMainWindow, Ui_Usuario_registrado):
    def __init__(self):
        super().__init__()
        super().setupUi(self)


ap = QApplication(sys.argv)
ap.setStyle("Fusion")
banco_dados = Connection("Banco.db")
Menu01 = Primeiro_Menu()
Menu02 = Segundo_Menu()
liberacao_atencao = Liberacao_atencao()
liberacao_seguranca = Liberacao_seguranca()
liberacao_meio_ambiente = Liberacao_meio_ambiente()
documentos_menu = Documentos_menu()
documentos_de_pecas_menu = Documentos_documentos_de_pecas_menu()
peca01 = Documentos_de_peca_peca01()
peca02 = Documentos_de_peca_peca02()
peca03 = Documentos_de_peca_peca03()
diagrama_eletrico = diagrama_eletrico()
mapa_de_riscos = Mapa_de_riscos()
aviso_liberacao = Aviso_liberacao()
interface_menu = Interface_menu()
interface_menu_botoes = Interface_botoes()
interface_menu_finalidade = Interface_finalidade()
interface_menu_botao_emergencia = Interface_botao_emergencia()
registros_menu = Registros_menu()
cadastros_menu = Cadastros_menu()
cadastros_menu_adicionar = Cadastros_menu_adicionar()
cadastros_menu_adicionar_ficha_01 = Cadastros_menu_adicionar_ficha01()
usuario_registrado = Usuario_registrado()



leitor = Teste_leitor()



leitor.show()
sys.exit(ap.exec())


