from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6 import QtGui,QtWidgets
from PySide6.QtGui import QPixmap
from blackjack import *
import sys
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackjack")
        self.setFixedSize(1285,900)
        self.setStyleSheet("""
            QTextEdit {background-color: #ddd; font-size:13px }
            QLabel { color: white; font-size: 40px; font-weight: 500 }
            QPushButton { background-color: #20581e; color: white;font-size: 15px }
            QPushButton:disabled { background-color: #163914 }""")
        tablero = QtGui.QImage("images/redimensionar/tablero.png")
        paleta = QtGui.QPalette()
        paleta.setBrush(QtGui.QPalette.Window, QtGui.QBrush(tablero))
        self.setPalette(paleta)

        self.botones()
        self.marcadores()
        self.registro()

        self.baraja = []
        self.ultimacarta = 51
        for i in range(0,52):
            self.baraja.append(QLabel(self))
            self.baraja[i].setPixmap(QPixmap(f'images/redimensionar/back.png'))
            self.baraja[i].move(30+i,157)
            self.baraja[i].resize(400,600)

        self.preparar()


    def mostrarBaraja(self):
        for i in range(self.ultimacarta+1,52):
            self.baraja[i].setPixmap(QPixmap(f'images/redimensionar/back.png'))
            self.baraja[i].move(30+i,157)
            self.baraja[i].resize(400,600)
            self.baraja[i].raise_()
        self.ultimacarta = 51

    def voltearCarta(self, indiceCarta, indiceBaraja):
        carta=self.juego.banca.mano[indiceCarta]
        self.baraja[indiceBaraja].setVisible(False)
        self.baraja[indiceBaraja].setPixmap(QPixmap(f"images/redimensionar/{carta.numero}{carta.palo}.png"))
        self.baraja[indiceBaraja].setVisible(True)
        self.baraja[indiceBaraja].raise_()

    def sacarCarta(self,jugador,numero,coord):
        carta=jugador.mano[numero]

        if carta.estado == 'Visible':
            self.baraja[self.ultimacarta].setPixmap(QPixmap(f"images/redimensionar/{carta.numero}{carta.palo}.png"))

        self.baraja[self.ultimacarta].move(500+25*numero,coord)
        self.baraja[self.ultimacarta].resize(300,450)
        self.baraja[self.ultimacarta].raise_()
        self.ultimacarta = self.ultimacarta - 1

    def botones(self):
        #botones colocación
        self.btnPedir = QtWidgets.QPushButton("Pedir carta", self)
        self.btnPedir.resize(175, 32)
        self.btnPedir.move(1050, 765)
        self.btnPlantar = QtWidgets.QPushButton("Plantarse", self)
        self.btnPlantar.resize(175, 32)
        self.btnPlantar.move(1050, 805)
        self.btnReiniciar = QtWidgets.QPushButton("Reiniciar", self)
        self.btnReiniciar.resize(175, 32)
        self.btnReiniciar.move(1050, 845)
        #botones funcion
        self.btnPedir.clicked.connect(self.pedir)
        self.btnPlantar.clicked.connect(self.plantar)
        self.btnReiniciar.clicked.connect(self.reiniciar)

    def marcadores(self):
        #marcador Banca
        self.marcadorBanca = QtWidgets.QLabel("0", self)
        self.marcadorBanca.resize(50, 50)
        self.marcadorBanca.move(507, 27)
        #marcador Jugador
        self.marcadorJugador = QtWidgets.QLabel("0", self)
        self.marcadorJugador.resize(50, 50)
        self.marcadorJugador.move(507, 796)

    def registro(self):
        # Texto para el registro
        self.registro = QtWidgets.QTextEdit(self)
        self.registro.setReadOnly(True)
        self.registro.move(1050, 185)
        self.registro.resize(175, 485)

    def preparar(self):
        self.registro.append(f"== Empieza Blackjack ==")
        self.mostrarBaraja()
        jugador=Jugador("Paco")
        self.juego=Juego(jugador)
        self.juego.iniciar()

        for i in range(0,len(self.juego.jugador.mano)):
            self.sacarCarta(self.juego.jugador,i,400)
        for i in range(0,len(self.juego.banca.mano)):
            self.sacarCarta(self.juego.banca,i,50)

        self.marcadorJugador.setText(str(self.juego.jugador.puntos))
        self.marcadorBanca.setText(str(self.juego.banca.mano[0].valor))



    def pedir(self):
        self.juego.pedircarta()
        self.sacarCarta(self.juego.jugador,len(self.juego.jugador.mano)-1,400)
        self.marcadorJugador.setText(str(self.juego.jugador.puntos))
        if self.juego.jugador.puntos > 21:
            self.btnPedir.setEnabled(False)
            self.btnPlantar.setEnabled(False)
            self.registro.append(self.juego.comprobar())
        elif self.juego.jugador.puntos==21:
            self.plantar()

    def plantar(self):
        self.btnPedir.setEnabled(False)
        self.btnPlantar.setEnabled(False)
        self.juego.banca.mano[1].Mostrar()
        self.voltearCarta(1, 48)
        time.sleep(0.5)
        self.marcadorBanca.setText(str(self.juego.banca.puntos))
        self.cartasBanca()
        self.registro.append(self.juego.comprobar())

    def reiniciar(self):
        self.marcadorJugador.setText("0")
        self.marcadorBanca.setText("0")
        self.registro.setText("")
        self.btnPedir.setEnabled(True)
        self.btnPlantar.setEnabled(True)
        self.preparar()

    def cartasBanca(self):
        while self.juego.banca.puntos<17:
            self.juego.pedircartaBanca()
            self.sacarCarta(self.juego.banca,len(self.juego.banca.mano)-1,50)
            self.marcadorBanca.setText(str(self.juego.banca.puntos))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())