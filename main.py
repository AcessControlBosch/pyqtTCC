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
        self.nameColadorador = ''
        self.idColadorador = ''
        self.edvColadorador = ''
        self.idCardColadorador = ''

    #Veriica se o usuario esta no banco de dados
    def pesquisar_colaborador(self, idcard):
        print(idcard)
        self.json_response = requests.get(self.url + 'users/' + idcard).json()

        print(self.json_response)
        self.nameColadorador = self.json_response['name']
        self.idColadorador = str(self.json_response['id'])
        self.edvColadorador = self.json_response['EDV']
        self.idCardColadorador = self.json_response['id_card']

        self.json_response = requests.get(self.url + 'apprentices/' + self.idColadorador).json()
        print('curso:', self.json_response['course']['name'])
        if(self.json_response['course']['name']!= 'Mecatrônica'):
            print('não vai entrar')
            return 'não'

        cursor = self.banco.cursor()
        return [self.idColadorador, self.nameColadorador, self.edvColadorador, self.idCardColadorador]

    def coleta_dados (self):
        cursor = self.banco.cursor()
        consulta = ("SELECT Nome, EDV, Classe FROM Usuarios")
        cursor.execute(consulta)
        lista = cursor.fetchall()
        cursor.close()
        print("lista:",lista)
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
        print('começou aq')
        self.botao_avancar.clicked.connect(self.comeca)
        self.lineEdit_tag.setFocus()
        self.lineEdit_tag.returnPressed.connect(self.comeca)
        self.lineEdit_tag.setText("")
        #self.centralwidget.mouseReleaseEvent = lambda event: self.comeca


    def comeca(self):
        #O programa começa aqui
        tag = self.lineEdit_tag.text()
        print('valor tag:', tag)

        #Procura o colaborador pela tag no crachá
        colaborador = banco_dados.pesquisar_colaborador(tag)

        #SE o coladorador tiver aptidão continua o programa
        if(colaborador  != 'não'):
            colaborador = banco_dados.pesquisar_colaborador(tag)[1]
            colaborador2 = colaborador.split(" ")
            print('colaborador', colaborador)
            print('colaborador2', colaborador2)

            Menu01.Label_Colaborador.setText(f'COLABORADOR: {colaborador2[0]} {colaborador2[-1]}')
            Menu01.Label_EDV.setText(f"EDV: {banco_dados.pesquisar_colaborador(tag)[2]}")
            Menu02.Label_Colaborador.setText(f'COLABORADOR: {colaborador2[0]} {colaborador2[-1]}')
            Menu02.Label_EDV.setText(f"EDV: {banco_dados.pesquisar_colaborador(tag)[2]}")

            leitor.hide()
            Menu01.show()

        #senao vai abrir a tela de aptidão -> cadastro
        else:
            leitor.hide()
            cadastros_menu_adicionar.show()
            cadastros_menu_adicionar.botao_voltar.hide()


##################### MENU 01 ################################
class Primeiro_Menu(QMainWindow, Ui_Menu01):
    def __init__(self): #FUNÇÃO QUE INICIA A TELA E DECLARA OS BOTÕES,LABELS,ETC.
        super().__init__() #COMANDO PARA INICIAR A TELA.
        super().setupUi(self) #COMANDO PARA INICIAR A TELA.
        self.estado = False
        self.Botao_Seta_Direita.clicked.connect(self.proxima_tela) #DEFINE A FUNÇÃO QUE SERÁ CHAMADA QUANDO A SETA P/ DIREITA FOR CLICADA.
        self.Botao_Liberar_Maquina.clicked.connect(self.liberacao_de_maquina) #DEFINE A FUNÇÃO QUE SERÁ CHAMADA QUANDO O BOTÃO DE LIBERAR A MÁQUINA FOR CLICADO.
        self.Botao_Interface_Didatica.clicked.connect(self.interface_didatica)
        self.Botao_Documentos.clicked.connect(self.menu_documentos) #DEFINE A FUNÇÃO QUE SERÁ CHAMADA QUANDO O BOTÃO DE DOCUMENTOS FOR CLICADO.
        self.Botao_Registros.clicked.connect(self.menu_registros)
        # self.Label_Colaborador.setText(f"COLABORADOR: {colaborador}") #DEFINE A LABEL COM O NOME DO COLABORADOR.
        # self.Label_EDV.setText(f"EDV: {edv}") #DEFINE A LABEL COM O EDV DO COLABORADOR.

    def proxima_tela(self): #FUNÇÃO QUE CHAMA O MENU 02.

        Menu02.show()
        Menu01.hide()


    def liberacao_de_maquina(self): #FUNÇÃO QUE INICIA O PROCESSO DE LIBERAÇÃO DE MÁQUINA.
        print('AQUIIIIIIII HELP')
        if self.estado == False:
            aviso_liberacao.label_texto.setText("<html><head/><body><p align=\"center\">O(s) seguinte(s) item(s) de Segurança não foram </p><p align=\"center\">marcado(s), o que significa que ele(s) apresenta(m) </p><p align=\"center\">não conformidade:</p></body></html>")
            liberacao_atencao.show()

            Menu01.hide()

        else:
            print(" ")

    def menu_documentos(self): # FUNÇÃO QUE CHAMA A TELA DE MENU DE DOCUMENTOS
        documentos_menu.show()
        Menu01.hide()

    def interface_didatica(self):
        interface_menu.show()
        Menu01.hide()

    def menu_registros(self):
        registros_menu.show()
        Menu01.hide()

class Segundo_Menu(QMainWindow, Ui_Menu02):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.Botao_Seta_Esquerda.clicked.connect(self.tela_anterior)
        self.Botao_Cadastros.clicked.connect(self.cadastros)
        self.Botao_Sair.clicked.connect(self.sair)


        self.Label_Colaborador.setText(f"COLABORADOR: {colaborador}")
        self.Label_EDV.setText(f"EDV: {edv}")

    def tela_anterior(self):
        print(colaborador)
        Menu01.show()
        Menu02.hide()

    def cadastros(self):
        cadastros_menu.show()
        Menu02.hide()

    def sair(self):
        leitor.lineEdit_tag.setText("")
        leitor.show()
        Menu02.hide()

class Liberacao_atencao(QMainWindow, Ui_Atencao):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_continuar.clicked.connect(self.tela_de_seguranca)
        self.botao_home.clicked.connect(self.home)


    def tela_de_seguranca(self):
        print('SEGURANÇAAAAAAAAAAAAAAAA')
        liberacao_seguranca.show()
        liberacao_atencao.hide()


    def home(self):
        Menu01.show()
        liberacao_atencao.hide()




class Liberacao_seguranca(QMainWindow, Ui_Liberacao_Seguranca):
    def __init__(self):
        print('---------- TO AQUI ---------')
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)
        self.botao_continuar.clicked.connect(self.tela_meio_ambiente)
        self.checkBox_1.clicked.connect(self.item01)
        self.checkBox_2.clicked.connect(self.item02)
        self.checkBox_3.clicked.connect(self.item03)
        self.checkBox_4.clicked.connect(self.item04)
        self.checkBox_5.clicked.connect(self.item05)
        self.checkBox_6.clicked.connect(self.item06)
        self.checkBox_7.clicked.connect(self.item07)
        self.checkBox_8.clicked.connect(self.item08)
        self.checkBox_9.clicked.connect(self.item09)

        self.lista_real = []
        self.lista_erros = []
        self.texto = []


    def tela_meio_ambiente(self):
        if self.resposta() == True:
            aviso_liberacao.seguranca = True
            liberacao_meio_ambiente.show()
            liberacao_seguranca.hide()


        else:
            aviso_liberacao.label_itens_desmarcados.setText(f"<html><head/><body><p align=\"center\">{self.texto}")
            aviso_liberacao.seguranca = False
            aviso_liberacao.show()
            liberacao_seguranca.hide()


    def home(self):
        Menu01.show()
        liberacao_seguranca.hide()


    def item01(self):

        if self.checkBox_1.isChecked():
            self.lista_real.append(1)

        else:
            self.lista_real.remove(1)

    def item02(self):
        if self.checkBox_2.isChecked():
            self.lista_real.append(2)

        else:
            self.lista_real.remove(2)

    def item03(self):
        if self.checkBox_3.isChecked():
            self.lista_real.append(3)

        else:
            self.lista_real.remove(3)

    def item04(self):
        if self.checkBox_4.isChecked():
            self.lista_real.append(4)

        else:
            self.lista_real.remove(4)

    def item05(self):
        if self.checkBox_5.isChecked():
            self.lista_real.append(5)

        else:
            self.lista_real.remove(5)

    def item06(self):
        if self.checkBox_6.isChecked():
            self.lista_real.append(6)

        else:
            self.lista_real.remove(6)

    def item07(self):
        if self.checkBox_7.isChecked():
            self.lista_real.append(7)

        else:
            self.lista_real.remove(7)

    def item08(self):
        if self.checkBox_8.isChecked():
            self.lista_real.append(8)

        else:
            self.lista_real.remove(8)

    def item09(self):
        if self.checkBox_9.isChecked():
            self.lista_real.append(9)

        else:
            self.lista_real.remove(9)


    def resposta(self):
        for i in range(1,10):
            if i  not in self.lista_real:
                self.lista_erros.append(i)

        if len(self.lista_erros) != 0:
            self.texto = str(self.lista_erros)
            return False

        else:
            return True




class Aviso_liberacao(QMainWindow, Ui_Aviso_Liberacao):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.seguranca = False
        self.botao_voltar.clicked.connect(self.voltar_check_list)
        self.botao_relatar_problema.clicked.connect(self.boletim)

    def voltar_check_list(self):

        if self.seguranca == False:
            liberacao_seguranca.lista_erros = []
            liberacao_seguranca.show()
            aviso_liberacao.hide()


        else:
            liberacao_meio_ambiente.show()
            aviso_liberacao.hide()


    def boletim(self):
        print("Agora só falta a tela")


class Liberacao_meio_ambiente(QMainWindow, Ui_Liberacao_Meio_Ambiente):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)
        self.botao_continuar.clicked.connect(self.resposta)
        self.img1 = QPixmap("imagens/CADEADO_FECHADO.png")
        self.img2 = QIcon ("imagens/CADEADO_ABERTO.png")


    def home(self):
        Menu01.show()
        liberacao_meio_ambiente.hide()


    def resposta(self):
        if self.checkBox_1.isChecked():
            Menu01.estado = True
            Menu01.Botao_Liberar_Maquina.setIcon(self.img2)
            Menu01.show()
            liberacao_meio_ambiente.hide()


        else:
            aviso_liberacao.label_texto.setText("<html><head/><body><p align=\"center\">O(s) seguinte(s) item(s) de Meio Ambiente não foram </p><p align=\"center\"> marcado(s), o que significa que ele(s) apresenta(m)</p><p align=\"center\"> não conformidade:</p></body></html>")
            aviso_liberacao.label_itens_desmarcados.setText(f"<html><head/><body><p align=\"center\">1")
            aviso_liberacao.show()
            liberacao_meio_ambiente.hide()




class Documentos_menu(QMainWindow,Ui_documentos_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)
        self.botao_documentos_de_pecas01.clicked.connect(self.documentos_de_pecas)
        self.botao_documentos_de_pecas02.clicked.connect(self.documentos_de_pecas)
        self.botao_diagrama_eletrico01.clicked.connect(self.diagrama_eletrico)
        self.botao_diagrama_eletrico02.clicked.connect(self.diagrama_eletrico)
        self.botao_mae01.clicked.connect(self.mapa_de_riscos)
        self.botao_mae02.clicked.connect(self.mapa_de_riscos)



    def home(self):
        Menu01.show()
        documentos_menu.hide()


    def documentos_de_pecas(self):
        documentos_de_pecas_menu.show()
        documentos_menu.hide()


    def diagrama_eletrico(self):
        diagrama_eletrico.show()
        documentos_menu.hide()


    def mapa_de_riscos(self):
        mapa_de_riscos.show()
        documentos_menu.hide()



class Documentos_documentos_de_pecas_menu(QMainWindow, Ui_documentos_documentos_de_pecas_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)
        self.botao_peca01_1.clicked.connect(self.peca01)
        self.botao_peca01_2.clicked.connect(self.peca01)
        self.botao_peca02_1.clicked.connect(self.peca02)
        self.botao_peca02_2.clicked.connect(self.peca02)
        self.botao_peca03_1.clicked.connect(self.peca03)
        self.botao_peca03_2.clicked.connect(self.peca03)

    def home(self):
        documentos_menu.show()
        documentos_de_pecas_menu.hide()


    def peca01(self):
        peca01.show()
        documentos_de_pecas_menu.hide()


    def peca02(self):
        peca02.show()
        documentos_de_pecas_menu.hide()


    def peca03(self):
        peca03.show()
        documentos_de_pecas_menu.hide()


class Documentos_de_peca_peca01(QMainWindow,Ui_peca01):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)


    def home(self):
        documentos_de_pecas_menu.show()
        peca01.hide()



class Documentos_de_peca_peca02(QMainWindow, Ui_peca02):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)

    def home(self):
        documentos_de_pecas_menu.show()
        peca02.hide()



class Documentos_de_peca_peca03(QMainWindow, Ui_peca03):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)

    def home(self):
        documentos_de_pecas_menu.show()
        peca03.hide()








class diagrama_eletrico(QMainWindow,Ui_documentos_diagrama_eletrico):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.contador = 1


        self.botao_home.clicked.connect(self.home)
        self.botao_seta_direita.clicked.connect(self.proxima_pagina)
        self.botao_seta_esquerda.clicked.connect(self.pagina_anterior)



        self.pagina1 = QPixmap("imagens/cachorro.png")
        self.pagina2 = QPixmap("imagens/jacare.png")
        self.pagina3 = QPixmap("imagens/MANUTENCAO.png")
        self.label_imagem.setPixmap(self.pagina1)


        if self.botao_seta_esquerda.clicked:
            print("oi")


    def home(self):
        documentos_menu.show()
        diagrama_eletrico.hide()


    def proxima_pagina(self):
        if self.contador<3:
            self.contador += 1

        if self.contador == 2:
            self.label_imagem.setPixmap(self.pagina2)
            self.label_paginas.setText("PÁGINA 02/03")

        if self.contador == 3:
            self.label_imagem.setPixmap(self.pagina3)
            self.label_paginas.setText("PÁGINA 03/03")




    def pagina_anterior(self):
        if self.contador>1:
            self.contador -= 1

        if self.contador == 1:
            self.label_imagem.setPixmap(self.pagina1)
            self.label_paginas.setText("PÁGINA 01/03")

        if self.contador == 2:
            self.label_imagem.setPixmap(self.pagina2)
            self.label_paginas.setText("PÁGINA 02/03")


class Mapa_de_riscos(QMainWindow, Ui_mapa_de_riscos):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)

    def home(self):
        documentos_menu.show()
        mapa_de_riscos.hide()



class Interface_menu(QMainWindow,Ui_interface_didatica_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_botoes.clicked.connect(self.botoes)
        self.botao_finalidades.clicked.connect(self.finalidade)
        self.botao_home.clicked.connect(self.home)



    def finalidade(self):
        interface_menu_finalidade.show()
        interface_menu.hide()


    def botoes(self):
        interface_menu_botoes.show()
        interface_menu.hide()


    def home(self):
        Menu01.show()
        interface_menu.hide()



class Interface_botoes(QMainWindow, Ui_interface_didatica_menu_botoes):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_1.clicked.connect(self.botao_01)
        self.botao_2.clicked.connect(self.botao_02)
        self.botao_3.clicked.connect(self.botao_03)
        self.botao_4.clicked.connect(self.botao_04)
        self.botao_5.clicked.connect(self.botao_05)
        self.botao_home.clicked.connect(self.home)
        self.botao_seta_dirteita.clicked.connect(self.botao_emergencia)

    def botao_01(self):
        self.label_indicacao.setText("1")
        self.label_titulo.setStyleSheet(
            "border-style: outset;\n" "border-color: rgb(0, 0, 0);\n""border-width:6px;\n""\n""\n""font: 75 30pt \"Bosch Sans Bold\";\n""background-color: rgb(0,0,0);")
        self.label_titulo.setText( "<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">BOTÃO LIGA A SERRA</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Botão responsável por iniciar o processo de \ncorte do perfil se a porta estiver trancada e a peça \ntravada. \n")

    def botao_02(self):
        self.label_titulo.setStyleSheet("border-style: outset;\n" "border-color: rgb(0, 0, 0);\n""border-width:6px;\n""\n""\n""font: 75 30pt \"Bosch Sans Bold\";\n""background-color: rgb(0,0,0);")
        self.label_indicacao.setText("2")
        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">CHAVE SELETORA DE PERFIL 30/45</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Chave seletora responsável por definir se o \nperfil a ser cortado é de 30 ou 45 para estabelecer a \ndistância que a serra deverá cortar para ultrapassar o \nperfil de 30/45 completamente.")

    def botao_03(self):
        self.label_indicacao.setText("3")
        self.label_titulo.setStyleSheet("border-style: outset;\n" "border-color: rgb(0, 0, 0);\n""border-width:6px;\n""\n""\n""font: 75 28pt \"Bosch Sans Bold\";\n""background-color: rgb(0,0,0);")
        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">CHAVE SELETORA DE PORTA TRANCADA</span></p></body></html>")
        self.label_caixa_de_texto.setText( "             Chave seletora responsável por garantir o \ntravamento da porta.\n\n")

    def botao_04(self):
        self.label_indicacao.setText("4")
        self.label_titulo.setStyleSheet("border-style: outset;\n" "border-color: rgb(0, 0, 0);\n""border-width:6px;\n""\n""\n""font: 75 30pt \"Bosch Sans Bold\";\n""background-color: rgb(0,0,0);")
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


