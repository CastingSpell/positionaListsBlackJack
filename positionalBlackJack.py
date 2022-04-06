##########################################################################
# Preparaciones previas                                                  #
##########################################################################

from array_positional_list import ArrayPositionalList as PositionalList
import random as r
import time
import os
import datetime as dt

##########################################################################
# Definición de las funciones que permitirán la ejecución del programa   #
##########################################################################

class ManoDeCartas(PositionalList):
    ''' Se una clase que hereda las características y métodos de la
    clase PositionalList importada anteriormente. Esta clase manejará
    una mano de cartas ordenadas con funciones del tipo iterar la mano,
    jugar carta, repartir... '''

    def __init__(self):
        '''Inicializamos las variables _cartas (creando el objeto
        de una lista posicional para que así herede sus médotos)'''

        self._cartas = PositionalList()

    def _search_element(self, e):
        """ Return the position of the first instance of e
        in a positional list self. Return None if e
        is not an element of self."""
        marker = self.first()  # None si lista vacía
        while marker != None and self.get_element(marker) != e:
            marker = self.after(marker)  # None si es la última
            return marker

    def _agregar_carta(self, p, v):
        ''' Se define la función _agregar_carta, la cual cual recibe como
        parámetros el palo y el valor de una carta y la mete en la mano de
        forma ordenada. '''

        global barajaIndex

        # order = {'A': 13, 'S': 10, 'C': 11, 'R': 12}
        # # Operador ternario que traduce las figuras a sus valores de orden A > nums > S > C > R
        # v = order[v] if v in order.keys() else v

        if self._cartas.is_empty():                         # Si la mano está vacía añade la carta directamente
            self._cartas.add_first((p, v))
        else:
            handPos = self._cartas.first()
            for item in self._cartas:
                if barajaIndex.index(item) > barajaIndex.index((p, v)):
                    self._cartas.add_before(handPos, (p,v))
                    break
                elif handPos == self._cartas.last():
                    self._cartas.add_after(handPos, (p,v))
                    break
                handPos += 1

    def repartir(self, numCartas):
        global baraja, barajaIndex
        ''' Reparte las cartas al azar '''

        for i in range(numCartas):              # Elegimos 4 cartas al azar
            pick = r.randint(0, len(baraja)-1)
            # print((baraja[pick][0], baraja[pick][1]))
            # Las añadimos a la mano y las ordenamos
            self._agregar_carta(baraja[pick][0], baraja[pick][1])
            temp = (baraja[pick][0], baraja[pick][1])
            baraja.pop(pick)    # La borramos de la baraja de picks

        return temp             # Devolvemos la carta añadida para mostrarla en main
    
    def cartas(self):
        ''' La función cartas itera por los elementos de la mano y los muestra'''
        cartas=[]
        for carta in self._cartas:
            cartas.append(carta)

        return cartas

    def jugar_carta(self, p):
        order = {'A': 13, 'S': 10, 'C': 11, 'R': 12} 
        values=[]
        global play

        for item in self._cartas:
            if item[0] == p:
                # Operador ternario que traduce las figuras a sus valores de orden A > nums > S > C > R
                if item[1] in order.keys():
                    values.append(order[item[1]]) 
                else:
                    values.append(item[1])

        try:
            maxVal = self._search_element((p, max(values)))
            play = self._cartas.get_element(maxVal)
            print('\n\t Jugando la carta: {}\n'.format(play))
            self._cartas.delete(maxVal)
            return True
                             # Se hace únicamente para controlar si hay que actualizar la mano en el print de main()
        except:
            palos_trad = {'C':'copas', 'O':'oros', 'E':'espadas', 'B':'bastos'}

            print('''\n≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠
* No hay cartas de {} en mano. 
            
                            Pasando...
≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠'''.format(palos_trad[p]))
            return False                                # Se hace únicamente para controlar si hay que actualizar la mano en el print de main()

    def puntos(self):
        ''' Cuenta los puntos que hay en mano, siendo el As variable y J, Q, K igual a 10
        
        Modo de funcionamiento:
        Para cada elemento coje el valor, en el caso de ser una figura suma 10 a puntos, y
        en caso de ser un numero sumará directamente. El problema viene con el As, tal y como
        en el blackjack real, este puede valer 1 o 10 según el resto de cartas. Luego también
        se tiene en cuenta que no es lo mismo conseguir justo 21 puntos que hacer un Blackjack
        esto solo sucede cuando las figuras son As K
        
        Una vez evaluado todo, el resultado es una tupla donde te devuelve los puntos, si el 
        jugador se ha pasado o no, y si ha hecho Blackjack'''


        puntos, pasarse, BJ_count, BJ = 0, False, 0, False
        # pasarse valorará si el resultado excede 21, se compará el resultado más adelante
        # BJ_count es un contador para saber si se produce BlackJack (As + K) la cual actualizará BJ a True

        As = False      # Creamos la variable As para evaluar el valor del As a final de todo
                        # y evitar errores cuando entra el As en primer lugar valor = 10, y 
                        # a posteriori entran por ejemplo un 8 y un 6, dando como resultado 24,
                        # cuando en realidad debería dar al As un valor = 1 resultando como total
                        # 15 puntos

        for i in self._cartas:
            if i[1] in ('J', 'Q', 'K'):
                puntos+=10
                if i[1] == 'K':
                    BJ_count += 1
            elif i[1] == 'A':
                As = True
                BJ_count += 1
            else:
                puntos += int(i[1])

        if As:
            if puntos > 11:
                puntos += 1
            else:
                puntos += 10

        if puntos > 21:
            pasarse = True

        if BJ_count == 2:
            BJ = True
            puntos = 21

        return (puntos, pasarse, BJ)

    def devolver(self):    
        ''' Devuelve todas las cartas al mazo para empezar una nueva partida

        Modo de funcionamiento:
        Se mira el tamaño de la mano y las eliminamos empezando por el final es decir,
        si en la mano hay 4 cartas, el range(4), devolverá 0,1,2,3 y con el reversed() 
        pasará a ser 3, 2, 1, 0. Esto se hace para no provocar errores por los índices
        en la lista posicional'''

        for i in reversed(range(len(self._cartas))):            
            self._cartas.delete(0)                               
                                                         
                                                         

play = ''                                               # Variable global para almacenar la carta jugada en cada momento

# Generación de la bajara
palos, nums = ['♠', '♣', '♥','♦'], [
    'A', 2, 3, 4, 5, 6, 7, 8, 9, 'J', 'Q', 'K']
 
baraja, barajaIndex = [], []                            # Creación de las listas donde se almacenarán las barajas
for i in palos:                                         # Bucle para generar la baraja de juego y la baraja de índices
    for j in nums:
        baraja.append((i, j))                           # Cada carta se guardará como una tupla de la forma ('Palo', 'Valor')
        barajaIndex.append((i, j))

def intro():
    ''' Animación inicial, con advertencia de uso responsable
    
    Modo de funcionamiento:
    Gracias al modulo time (concretamente la funcion time.sleep()) hemos conseguido hacer
    unos prints sucesivos, que si la ventana del terminal es del tamaño predeterminado,
    se logrará un efecto de animación
    
    No se ha hecho un bucle por la animación de la palabra 'Loading...'
    '''
    print('''
            

                .------.     .------.        .------.    .------.        .------.    .------. .------.
                |A.--. |     |3.--. |        |Q.--. |    |8.--. |        |J.--. |    |9.--. | |5.--. |
                | (\/) |     | :(): |        | (\/) |    | :/\: |        | :(): |    | :/\: | | :/\: |
                | :\/: |     | ()() |        | :\/: |    | :\/: |        | ()() |    | (__) | | (__) |
                | '--'A|     | '--'3|        | '--'Q|    | '--'8|        | '--'J|    | '--'9| | '--'5|
                `------'     `------'        `------'    `------'        `------'    `------' `------'


                        ** Advertencia:  este  proyecto  no  pretende fomentar el juego 
                        en  ninguna de  sus  variantes,  es responsabilidad del usuario
                        hacer un uso responsable de este programa y de sus dependencias.
                        Por favor,  no juegue  si ha tenido problemas con el juego o no
                        lo  considera  adecuado para usted. Juegue  con  responsabilidad
                        

            .------.        .------. .------.        .------.    .------.        .------.        .------.
            |J.--. |        |4.--. | |K.--. |        |A.--. |    |7.--. |        |Q.--. |        |10.-. |
            | :(): |        | :/\: | | :/\: |        | (\/) |    | :(): |        | (\/) |        | :(): |
            | ()() |        | :\/: | | :\/: |        | :\/: |    | ()() |        | :\/: |        | ()() | 
            | '--'J|        | '--'4| | '--'K|        | '--'A|    | '--'7|        | '--'Q|        | '-'10|
            `------'        `------' `------'        `------'    `------'        `------'        `------'
                                                    Loading

                                                    Practica 3: Pedro Redondo Loureiro y Jose Vilas Taboada                           
    ''')
    time.sleep(4)
    print('''
            

                .------.     .------.        .------.    .------.        .------.    .------. .------.
                |A.--. |     |3.--. |        |Q.--. |    |8.--. |        |J.--. |    |9.--. | |5.--. |
                | (\/) |     | :(): |        | (\/) |    | :/\: |        | :(): |    | :/\: | | :/\: |
                | :\/: |     | ()() |        | :\/: |    | :\/: |        | ()() |    | (__) | | (__) |
                | '--'A|     | '--'3|        | '--'Q|    | '--'8|        | '--'J|    | '--'9| | '--'5|
                `------'     `------'        `------'    `------'        `------'    `------' `------'


                        ██████╗ ██╗      █████╗  ██████╗██╗  ██╗     ██╗ █████╗  ██████╗██╗  ██╗
                        ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝     ██║██╔══██╗██╔════╝██║ ██╔╝
                        ██████╔╝██║     ███████║██║     █████╔╝      ██║███████║██║     █████╔╝ 
                        ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██   ██║██╔══██║██║     ██╔═██╗ 
                        ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗╚█████╔╝██║  ██║╚██████╗██║  ██╗
                        ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝

            .------.        .------. .------.        .------.    .------.        .------.        .------.
            |J.--. |        |4.--. | |K.--. |        |A.--. |    |7.--. |        |Q.--. |        |10.-. |
            | :(): |        | :/\: | | :/\: |        | (\/) |    | :(): |        | (\/) |        | :(): |
            | ()() |        | :\/: | | :\/: |        | :\/: |    | ()() |        | :\/: |        | ()() | 
            | '--'J|        | '--'4| | '--'K|        | '--'A|    | '--'7|        | '--'Q|        | '-'10|
            `------'        `------' `------'        `------'    `------'        `------'        `------'
                            
                                                     Loading.
                                                                               
    ''')
    time.sleep(0.4)
    print('''
            

                .------.     .------.        .------.    .------.        .------.    .------. .------.
                |A.--. |     |3.--. |        |Q.--. |    |8.--. |        |J.--. |    |9.--. | |5.--. |
                | (\/) |     | :(): |        | (\/) |    | :/\: |        | :(): |    | :/\: | | :/\: |
                | :\/: |     | ()() |        | :\/: |    | :\/: |        | ()() |    | (__) | | (__) |
                | '--'A|     | '--'3|        | '--'Q|    | '--'8|        | '--'J|    | '--'9| | '--'5|
                `------'     `------'        `------'    `------'        `------'    `------' `------'









            .------.        .------. .------.        .------.    .------.        .------.        .------.
            |J.--. |        |4.--. | |K.--. |        |A.--. |    |7.--. |        |Q.--. |        |10.-. |
            | :(): |        | :/\: | | :/\: |        | (\/) |    | :(): |        | (\/) |        | :(): |
            | ()() |        | :\/: | | :\/: |        | :\/: |    | ()() |        | :\/: |        | ()() | 
            | '--'J|        | '--'4| | '--'K|        | '--'A|    | '--'7|        | '--'Q|        | '-'10|
            `------'        `------' `------'        `------'    `------'        `------'        `------'
                            
                                                     Loading..
                                                                               
    ''')
    time.sleep(0.4)
    print('''
            

                .------.     .------.        .------.    .------.        .------.    .------. .------.
                |A.--. |     |3.--. |        |Q.--. |    |8.--. |        |J.--. |    |9.--. | |5.--. |
                | (\/) |     | :(): |        | (\/) |    | :/\: |        | :(): |    | :/\: | | :/\: |
                | :\/: |     | ()() |        | :\/: |    | :\/: |        | ()() |    | (__) | | (__) |
                | '--'A|     | '--'3|        | '--'Q|    | '--'8|        | '--'J|    | '--'9| | '--'5|
                `------'     `------'        `------'    `------'        `------'    `------' `------'


                        ██████╗ ██╗      █████╗  ██████╗██╗  ██╗     ██╗ █████╗  ██████╗██╗  ██╗
                        ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝     ██║██╔══██╗██╔════╝██║ ██╔╝
                        ██████╔╝██║     ███████║██║     █████╔╝      ██║███████║██║     █████╔╝ 
                        ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██   ██║██╔══██║██║     ██╔═██╗ 
                        ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗╚█████╔╝██║  ██║╚██████╗██║  ██╗
                        ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝

            .------.        .------. .------.        .------.    .------.        .------.        .------.
            |J.--. |        |4.--. | |K.--. |        |A.--. |    |7.--. |        |Q.--. |        |10.-. |
            | :(): |        | :/\: | | :/\: |        | (\/) |    | :(): |        | (\/) |        | :(): |
            | ()() |        | :\/: | | :\/: |        | :\/: |    | ()() |        | :\/: |        | ()() | 
            | '--'J|        | '--'4| | '--'K|        | '--'A|    | '--'7|        | '--'Q|        | '-'10|
            `------'        `------' `------'        `------'    `------'        `------'        `------'
                            
                                                     Loading...
                                                                               
    ''')
    time.sleep(0.4)
    print('''
            

                .------.     .------.        .------.    .------.        .------.    .------. .------.
                |A.--. |     |3.--. |        |Q.--. |    |8.--. |        |J.--. |    |9.--. | |5.--. |
                | (\/) |     | :(): |        | (\/) |    | :/\: |        | :(): |    | :/\: | | :/\: |
                | :\/: |     | ()() |        | :\/: |    | :\/: |        | ()() |    | (__) | | (__) |
                | '--'A|     | '--'3|        | '--'Q|    | '--'8|        | '--'J|    | '--'9| | '--'5|
                `------'     `------'        `------'    `------'        `------'    `------' `------'









            .------.        .------. .------.        .------.    .------.        .------.        .------.
            |J.--. |        |4.--. | |K.--. |        |A.--. |    |7.--. |        |Q.--. |        |10.-. |
            | :(): |        | :/\: | | :/\: |        | (\/) |    | :(): |        | (\/) |        | :(): |
            | ()() |        | :\/: | | :\/: |        | :\/: |    | ()() |        | :\/: |        | ()() | 
            | '--'J|        | '--'4| | '--'K|        | '--'A|    | '--'7|        | '--'Q|        | '-'10|
            `------'        `------' `------'        `------'    `------'        `------'        `------'
                            
                                                     Loading
                                                                               
    ''')
    time.sleep(0.4)
    print('''
            

                .------.     .------.        .------.    .------.        .------.    .------. .------.
                |A.--. |     |3.--. |        |Q.--. |    |8.--. |        |J.--. |    |9.--. | |5.--. |
                | (\/) |     | :(): |        | (\/) |    | :/\: |        | :(): |    | :/\: | | :/\: |
                | :\/: |     | ()() |        | :\/: |    | :\/: |        | ()() |    | (__) | | (__) |
                | '--'A|     | '--'3|        | '--'Q|    | '--'8|        | '--'J|    | '--'9| | '--'5|
                `------'     `------'        `------'    `------'        `------'    `------' `------'


                        ██████╗ ██╗      █████╗  ██████╗██╗  ██╗     ██╗ █████╗  ██████╗██╗  ██╗
                        ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝     ██║██╔══██╗██╔════╝██║ ██╔╝
                        ██████╔╝██║     ███████║██║     █████╔╝      ██║███████║██║     █████╔╝ 
                        ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██   ██║██╔══██║██║     ██╔═██╗ 
                        ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗╚█████╔╝██║  ██║╚██████╗██║  ██╗
                        ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝

            .------.        .------. .------.        .------.    .------.        .------.        .------.
            |J.--. |        |4.--. | |K.--. |        |A.--. |    |7.--. |        |Q.--. |        |10.-. |
            | :(): |        | :/\: | | :/\: |        | (\/) |    | :(): |        | (\/) |        | :(): |
            | ()() |        | :\/: | | :\/: |        | :\/: |    | ()() |        | :\/: |        | ()() | 
            | '--'J|        | '--'4| | '--'K|        | '--'A|    | '--'7|        | '--'Q|        | '-'10|
            `------'        `------' `------'        `------'    `------'        `------'        `------'
                            
                                                     Loading.
                                                                               
    ''')
    time.sleep(0.4)
    print('''
            

                .------.     .------.        .------.    .------.        .------.    .------. .------.
                |A.--. |     |3.--. |        |Q.--. |    |8.--. |        |J.--. |    |9.--. | |5.--. |
                | (\/) |     | :(): |        | (\/) |    | :/\: |        | :(): |    | :/\: | | :/\: |
                | :\/: |     | ()() |        | :\/: |    | :\/: |        | ()() |    | (__) | | (__) |
                | '--'A|     | '--'3|        | '--'Q|    | '--'8|        | '--'J|    | '--'9| | '--'5|
                `------'     `------'        `------'    `------'        `------'    `------' `------'









            .------.        .------. .------.        .------.    .------.        .------.        .------.
            |J.--. |        |4.--. | |K.--. |        |A.--. |    |7.--. |        |Q.--. |        |10.-. |
            | :(): |        | :/\: | | :/\: |        | (\/) |    | :(): |        | (\/) |        | :(): |
            | ()() |        | :\/: | | :\/: |        | :\/: |    | ()() |        | :\/: |        | ()() | 
            | '--'J|        | '--'4| | '--'K|        | '--'A|    | '--'7|        | '--'Q|        | '-'10|
            `------'        `------' `------'        `------'    `------'        `------'        `------'
                            
                                                     Loading..
                                                                               
    ''')
    time.sleep(0.4)
    print('''
            

                .------.     .------.        .------.    .------.        .------.    .------. .------.
                |A.--. |     |3.--. |        |Q.--. |    |8.--. |        |J.--. |    |9.--. | |5.--. |
                | (\/) |     | :(): |        | (\/) |    | :/\: |        | :(): |    | :/\: | | :/\: |
                | :\/: |     | ()() |        | :\/: |    | :\/: |        | ()() |    | (__) | | (__) |
                | '--'A|     | '--'3|        | '--'Q|    | '--'8|        | '--'J|    | '--'9| | '--'5|
                `------'     `------'        `------'    `------'        `------'    `------' `------'


                        ██████╗ ██╗      █████╗  ██████╗██╗  ██╗     ██╗ █████╗  ██████╗██╗  ██╗
                        ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝     ██║██╔══██╗██╔════╝██║ ██╔╝
                        ██████╔╝██║     ███████║██║     █████╔╝      ██║███████║██║     █████╔╝ 
                        ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██   ██║██╔══██║██║     ██╔═██╗ 
                        ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗╚█████╔╝██║  ██║╚██████╗██║  ██╗
                        ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝

            .------.        .------. .------.        .------.    .------.        .------.        .------.
            |J.--. |        |4.--. | |K.--. |        |A.--. |    |7.--. |        |Q.--. |        |10.-. |
            | :(): |        | :/\: | | :/\: |        | (\/) |    | :(): |        | (\/) |        | :(): |
            | ()() |        | :\/: | | :\/: |        | :\/: |    | ()() |        | :\/: |        | ()() | 
            | '--'J|        | '--'4| | '--'K|        | '--'A|    | '--'7|        | '--'Q|        | '-'10|
            `------'        `------' `------'        `------'    `------'        `------'        `------'
                            
                                                     Loading...                                                                    
    ''')

def print_table(hand, pts, dl_hand, dl_pts, bet, balance):
    '''Mostrará la mesa con un diseño predeterminado, a la que recurriremos multiples veces

    Consideraciones previas: 
    Asegúrese de que el tamaño del terminal desde el que se ejecuta esto es de 120 x 30 aproximadamente'''
    
    
    print(f'''
       



                 ___________________________________________
                /
               /    Dealer:   {dl_hand}          
              // Puntos: {dl_pts[0]}
             /                                             
            /                                           
           /    Tu mano:    {hand}             
          // Puntos: {pts[0]}
         /__________________________________________
         Apuesta: {bet} ☼ / Balance: {balance} ☼






    ''')

def check(player):
    ''' Comprueba que el jugador no se haya pasado de 21 puntos'''
    return player.puntos()[1]

def blackjack(bal):
    ''' Gestiona la partida, recibe como parámetro el balance con el que se desea iniciar.

    Modo de funcionamiento:
    blackjack() llama a la función intro(), crea las manos y luego entra en un bucle mientras
    el balance sea mayor a 0.
    En dicho bucle ya es donde se valora el juego en sí, así como los menús de selección y
    la evaluación de las manos para calcular la victoria'''

    intro()
    jugador, dealer = ManoDeCartas(), ManoDeCartas()    # Creamos los objetos asociados a la clase ManoDeCartas()
    first = True                                        # first valorará si es la primera vez de la jugada en sí para repartir 2 cartas al jugador 

    balance, win, played = bal, 0, 0

    while balance > 0:
        pts, dl_pts = 0,0

        bet = input('\n\nIntroduce el valor de la apuesta (restante {} ☼) (enter >> salir): '.format(balance))
        if bet == '':
            print('Has salido del juego, balance final {}, número de victorias a la banca {} de {}'.format(balance, win, played))
            # Comprobamos que existe el archivo bj_stats.txt para guardar los resultados, de no ser así, se crea
            # En el caso de no existir se escribe inicialmente una cabecera sobre los datos que se introducen
            stats = open('./bj_stats.txt', 'a')

            if not os.path.isfile('./bj_stats.txt'):
                stats.write('Fecha\t\tBalance\t\tVictorias / Total\n')

            stats.write('\n{}\t{}\t\t     {}   /   {}'.format(dt.date.today(), balance, win, played))
            
            print('\n\tLos datos han sido guardados en ./bj_stats.txt y ./bj_hands.txt')
            break #exit()
        else:
            balance -= int(bet)

        
        while True:                 # Creamos un bucle infinito que se romperá en los casos de victoria o derrota del jugador

            if first:               # Si es la primera vez repartimos 2 cartas al jugador y 1 al crupier
                jugador.repartir(2)
                dealer.repartir(1)
                print_table(jugador.cartas(), jugador.puntos(), dealer.cartas(), dealer.puntos(), bet, balance)
                first = False

            else:
                pedir = input('Presiona enter para nueva carta o introduce algo para plantarte: ')
                if pedir == '':
                    jugador.repartir(1)
                    print_table(jugador.cartas(), jugador.puntos(), dealer.cartas(), dealer.puntos(), bet, balance)

                    if check(jugador):      # Comprueba si se ha pasado de 21 puntos
                        print('\n\nLa banca gana!\n\n')
                        # print_table(jugador.cartas(), jugador.puntos(), dealer.cartas(), dealer.puntos(), bet, balance)
                        break

                    if jugador.puntos()[2]:      # Comprueba si ha hecho Blackjack
                        balance+=2.5*int(bet)
                        print('\n\nBlackJack! Tu balance ha sido actualizado {}☼\n\n'.format(balance))
                        # print_table(jugador.cartas(), jugador.puntos(), dealer.cartas(), dealer.puntos(), bet, balance)
                        win += 1
                        break

                    
                else:
                    while dealer.puntos()[0] < 17:      # Regla del blackjack, la banca debe plantarse con 17 puntos, 
                        time.sleep(0.8)                 # por lo que mientras su puntuación sea menor a esa, se repartirá                                       
                        dealer.repartir(1)              # más cartas
                        print_table(jugador.cartas(), jugador.puntos(), dealer.cartas(), dealer.puntos(), bet, balance)

                        if dealer.puntos()[2]:      # Comprueba si ha hecho Blackjack, tomando el tercer valor de la tupla resultado de puntos()
                            print('\n\nLa banca tiene BlackJack! Tu balance ha sido actualizado {} ☼\n\n'.format(balance))
                            # print_table(jugador.cartas(), jugador.puntos(), dealer.cartas(), dealer.puntos(), bet, balance)
                            break

                        if check(jugador):
                            balance+= 2*int(bet)
                            print('\n\nEl jugador gana! Tu balance ha sido actualizado {} ☼\n\n'.format(balance))
                            # print_table(jugador.cartas(), jugador.puntos(), dealer.cartas(), dealer.puntos(), bet, balance)
                            win += 1
                            break


                    if 21 >= dealer.puntos()[0] > jugador.puntos()[0]:
                        print('\n\nLa banca gana!\n\n')
                        # print_table(jugador.cartas(), jugador.puntos(), dealer.cartas(), dealer.puntos(), bet, balance)
                        break

                    elif dealer.puntos()[0] > 21:
                        balance += 2*int(bet)
                        print('\n\nEl jugador gana! Tu balance ha sido actualizado {}☼\n\n'.format(balance))
                        # print_table(jugador.cartas(), jugador.puntos(), dealer.cartas(), dealer.puntos(), bet, balance)
                        win += 1
                        break

                    else: 
                        balance+= 2*int(bet)
                        print('\n\nEl jugador gana! Tu balance ha sido actualizado {}☼\n\n'.format(balance))
                        # print_table(jugador.cartas(), jugador.puntos(), dealer.cartas(), dealer.puntos(), bet, balance)
                        win += 1
                        break

        # Registramos la mano al historial de manos y devolvemos las cartas al mazo          
        historial = open('./bj_hands.txt', 'a', encoding='utf-8')
        historial.write('\n\n{}\nMano jugador:  {}\nMano crupier:  {}'.format(dt.date.today(), jugador.cartas(), dealer.cartas()))

        jugador.devolver(), dealer.devolver()
        first = True
        played += 1

    if balance == 0:
        print('Se ha quedado sin monedas, mejor suerte la proxima vez...')
        print('\tHa ganado {} de {}'.format(win, played))


##########################################################################
# Ejecución del programa                                                 #
##########################################################################


blackjack(500)      # Cambiar valor para escojer el balance inicial

##########################################################################