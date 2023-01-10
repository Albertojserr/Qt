import random
class Carta:
    def __init__(self, numero,palo,estado='Visible'):
        self.numero=numero
        self.palo=palo
        self.estado=estado

        if numero==1:
            self.valor=11
        elif numero>10:
            self.valor=10
        else:
            self.valor=int(numero)

    def Mostrar(self):
        self.estado='Visible'

    def Ocultar(self):
        self.estado='Oculto'

    def Estar(self):
        if self.estado=='Visible':
            print(f'{self.numero} de {self.palo}')
        else:
            print('No se puede ver')

class Baraja:
    def __init__(self):
        self.cartas=[]
        self.jugadas=[]
        palos=['Corazones','Diamantes','Treboles','Picas']
        for palo in palos:
            for i in range(1,14):
                self.cartas.append(Carta(i,palo))
        self.barajar()
    def barajar(self):
        random.shuffle(self.cartas)

    def sacarCarta(self):
        if len(self.cartas) > 0:
            carta=self.cartas.pop()
            self.jugadas.append(carta)
            return carta
        return None

    def reiniciar(self):
        for carta in self.jugadas:
            carta.Ocultar()
            self.cartas.append(carta)
        self.jugadas=[]
        self.barajar()

class Jugador:
    def __init__(self,nombre):
        self.nombre=nombre
        self.mano=[]
        self.puntos=0

    def cogerCarta(self,carta):
        self.mano.append(carta)
        if carta.valor==11 and self.puntos+11>21:
            self.puntos+=1
        else:
            self.puntos+=carta.valor

    def mostrar(self):
        for carta in self.mano:
            carta.Estar()

    def puntaje(self):
        print(f'{self.nombre} tiene {self.puntos} puntos.')

class Juego:
    def __init__(self,jugador):
        self.baraja=Baraja()
        self.jugador=jugador
        self.banca=Jugador('Banca')

    def pedircarta(self):
        self.jugador.cogerCarta(self.baraja.sacarCarta())

    def pedircartaBanca(self):
        self.banca.cogerCarta(self.baraja.sacarCarta())

    def repartirInicial(self,juga):
        juga.cogerCarta(self.baraja.sacarCarta())
        juga.cogerCarta(self.baraja.sacarCarta())
        if juga.nombre=='Banca':
            juga.mano[1].Ocultar()

    def iniciar(self):#cuando se inicia o reinicia el programa se debe ejecutar esto
        self.repartirInicial(self.jugador)
        self.repartirInicial(self.banca)

    def comprobar(self):
        if self.jugador.puntos>21:
            return(f'== {self.banca.nombre} gana ==')
        elif self.banca.puntos>21:
            return(f'== {self.jugador.nombre} gana ==')
        elif self.jugador.puntos>self.banca.puntos:
            return(f'== {self.jugador.nombre} gana ==')
        elif self.banca.puntos==self.jugador.puntos:
            return("== Han empatado ==")
        else:
            return(f'== {self.banca.nombre} gana ==')
            #puede seguir pidiendo

    def RepartirCartas(self):
        self.jugador.cogerCarta(self.baraja.sacarCarta())
        self.jugador.mostrar()
        self.jugador.puntaje()


    def CartaBanca(self):
        self.banca.mano[1].Mostrar()
        self.banca.mostrar()
        if self.jugador.puntos<22:
            while self.banca.puntos<17:
                print(f"-------------------")
                self.banca.cogerCarta(self.baraja.sacarCarta())
                self.banca.mostrar()


    def jugar(self):
        self.jugador.puntaje()
        respuesta=input("¿Otra carta? ")
        while respuesta=='Si':
            self.RepartirCartas()
            if self.jugador.puntos>21:
                break
            respuesta=input("¿Otra carta? ")
        self.CartaBanca()
        self.comprobar()


if __name__=='__main__':
    jugador=Jugador("Marco")
    tabla=Juego(jugador)
    tabla.iniciar()
    print(f'Las cartas de {jugador.nombre}')
    jugador.mostrar()
    print(f'Las cartas de {tabla.banca.nombre}')
    tabla.banca.mostrar()
    tabla.jugar()