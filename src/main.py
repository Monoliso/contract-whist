import random
# import collections, functools, operator
from impresion import *

def ingresar_jugadores():
    """ Se solicita al usuario inicial que ingrese los nombres de los jugadores separados por
        coma. La cantidad mínima es 3, y la máxima 7. """

    condicion = True
    while condicion:
        jugadores_str = input("Ingrese los nombres de los jugadores separados por coma: ")
        jugadores_lista = jugadores_str.split(',')
        if len(jugadores_lista) < 3 or len(jugadores_lista) > 7:
            print("La cantidad de jugadores no es correcta, vuelva a intentarlo.")
        else: condicion = False
    return jugadores_lista

def ingresar_prediccion(jugador: str, numero_bazas: int) -> "dict[str:int]":
    """ Dado un jugador y la cantidad de bazas que se va a jugar, se solicita
        al usuario el ingreso de su prediccion. Se impide que la prediccion supere
        la cantidad de bazas. """

    jugador_prediccion = dict()
    condicion = True
    while condicion:
        try:
            prediccion = int(input(f"{jugador}, cuantas bazas cree que ganará?: "))
            # Hay que corroborar que se ingrese un número Y que se encuentre en el rango.
            if prediccion >= 0 and prediccion <= numero_bazas:
                jugador_prediccion[jugador] = prediccion
                condicion = False
            else: print("El número excede la cantidad de bazas posible")
        except ValueError:
            print("Debe ingresar un número")
    return jugador_prediccion

def ingresar_jugada(jugador: str, cartas_jugador: "list[tuple]", \
        palo_baza_carta: "tuple[str, str]", triunfo: "tuple[str, str]") -> "tuple[str, str]":
    # print(f"Turno de {jugador}")
    # imprimir_mazo(cartas_jugador, True)
    jugada = int(input(f"{jugador}, qué carta desea jugar?: "))
    # Corroborar jugada
    return cartas_jugador[jugada-1]

def whist(jugadores: "list[str]"):
    # Herramientas funcionales: lambda, map y filter. También está reduce pero con importación.
    BAZAS_POR_MANO = [i+1 for i in range(8)] + [i for i in range(8, 0, -1)]
    mazo_ordenado_prueba = [('2', '♥️'), ('7', '♦️'), ('9', '♠️'), ('A', '♣️'), \
        ('3', '♥️'), ('10', '♦️'), ('3', '♠️'), ('K', '♣️')]
    puntos_juego = dict.fromkeys(jugadores, 0)
    for mano in BAZAS_POR_MANO:
        cartas_en_posesion, triunfo = repartir_cartas(jugadores, mano)
        datos_mano = (mano, cartas_en_posesion, triunfo)
        predicciones = obtener_predicciones(datos_mano, jugadores)
        puntos_mano = jugar_mano(jugadores, datos_mano, predicciones)
        for jugador in puntos_juego.keys():
            puntos_juego[jugador] += puntos_mano[jugador]
        # Rotar lista de jugadores   
    pass

def repartir_cartas(jugadores: "list[str]", numero_bazas: int) -> "tuple[dict, set]":
    """ Dada una lista de jugadores y la cantidad de bazas que se juega,
        se le reparten la cantidad de cartas correspondiente a cada jugador y
        se devuelve el triunfo de la baza. """
    
    PALOS = {'♥️', '♦️', '♠️', '♣️'}
    VALORES = [str(i+1) for i in range(1, 10)] + ['J', 'Q', 'K', 'A']
    mazo = {(x, y) for x in VALORES for y in PALOS}
    cartas_en_posesion = dict.fromkeys(mazo, None)

    for jugador in enumerate(jugadores):
        for numero_carta in range(numero_bazas):
            carta = random.choice(list(mazo))
            mazo.remove(carta)
            cartas_en_posesion[carta] = jugador[1]
    triunfo = random.choice(list(mazo))
    return cartas_en_posesion, triunfo

def obtener_predicciones(mano: "tuple[int, dict, tuple]", jugadores: "list[str]") -> \
        "dict[str:int]":
    """ Dado el triunfo de la baza, las cartas de los jugadores, y el orden para 
        solicitar cada prediccion, esta función se encarga de mostrarle a cada uno 
        la información pertinente para que pueda realizar la prediccion de la mano. """
    
    numero_bazas, cartas_en_posesion, triunfo = mano
    predicciones_mano = dict()
    for numero, jugador in enumerate(jugadores):
        if numero != 0:
            imprimir_predicciones(predicciones_mano)
        cartas_jugador = {carta for carta, nombre in cartas_en_posesion.items() \
            if nombre == jugador}
        imprimir_triunfo_palo(triunfo, None)
        imprimir_mazo([triunfo], False)
        print(f"Cartas de {jugador}:")
        imprimir_mazo(cartas_jugador, True) # imprimir_mazo(ordenar_cartas_por_palo(cartas_jugador))
        predicciones_mano.update(ingresar_prediccion(jugador, numero_bazas))
        if numero != len(jugadores)-1:
            input(f"Entregue la computadora a {jugadores[numero+1]}. ")
        clear()
    return predicciones_mano

def jugar_mano(jugadores: "list[str]", mano: "tuple[int, dict[tuple:str], tuple[str, str]]", \
        predicciones: "dict[str:int]") -> "dict[str:int]":
    bazas_ganadas = dict.fromkeys(jugadores, 0)
    numero_bazas, cartas_en_posesion, triunfo = mano
    for baza in range(numero_bazas):
        mesa = dict()
        palo_baza = None
        for numero, jugador in enumerate(jugadores):
            cartas_jugador = [carta for carta, nombre in cartas_en_posesion.items() \
                if nombre == jugador]
            clear()
            imprimir_triunfo_palo(triunfo, palo_baza)
            imprimir_mazo([triunfo], False)
            imprimir_mazo(cartas_jugador, True)
            jugada = ingresar_jugada(jugador, cartas_jugador, palo_baza, triunfo)
            # Esta funcion debe corroborar que la jugada sea correcta
            if numero == 0:
                palo_baza = jugada
            cartas_en_posesion[jugada] = None
            mesa[jugada] = jugador
        clear()
        print(f"La baza la ganó {ganador_baza}")
        ganador_baza = determinar_ganador_baza(mesa, palo_baza, triunfo)
        bazas_ganadas[ganador_baza] += 1
        jugadores = actualizar_orden_jugadores(jugadores, ganador_baza)
    puntos_mano = determinar_puntos_mano(bazas_ganadas, predicciones)
    return puntos_mano

def determinar_ganador_baza(mesa: "dict[tuple:str]", palo_baza_carta: "tuple[str, str]", \
        triunfo: "tuple[str, str]") -> str:

    VALORES = [str(i+1) for i in range(1, 10)] + ['J', 'Q', 'K', 'A']
    palo_triunfo = triunfo[1]
    palo_baza = palo_baza_carta[1]
    ganador = palo_baza_carta
    for carta in mesa.keys():
        if carta[1] == palo_triunfo and ganador[1] != palo_triunfo:
            ganador = carta
        elif carta[1] == palo_triunfo and VALORES.index(carta[0]) > VALORES.index(ganador[0]):
            ganador = carta
        elif carta[1] == palo_baza and VALORES.index(carta[0]) > VALORES.index(ganador[0]):
            ganador = carta
    jugador_ganador = mesa[ganador]
    return jugador_ganador

# ------------------
def ordenar_cartas_por_palo(cartas: "set[tuple]") -> "list[tuple]":
    """ Algoritmo para ordenar cartas, seguramente lo más complicado de todo
        este programa, no estaría mal revisarlo luego. """
    
    PALOS = {'♥️', '♦️', '♠️', '♣️'}
    NUMEROS = [str(i+1) for i in range(1, 10)] + ['J', 'Q', 'K', 'A']
    numeros_con_valor = enumerate(NUMEROS)
    lista_ordenada = list()
    for palo in PALOS:
        lista_ordenada_palos = list()
        for carta in cartas:
            if carta[1] == palo:
                # Añadir a lista de forma ordenada
                pass
        lista_ordenada.append(lista_ordenada_palos)
    return lista_ordenada

def ordenar_cartas_mismo_palo(lista, valor):
    NUMEROS = [str(i+1) for i in range(1, 10)] + ['J', 'Q', 'K', 'A']
    resultado = list()
    for carta in enumerate(lista):
        index_carta = NUMEROS.index(carta[0])
        index_nueva_carta = NUMEROS.index(valor[0])
        if index_nueva_carta > index_carta:
            resultado = lista[:lista[0]] + valor + lista[lista[0]+1:]
        else: resultado.insert(0, valor)
    pass

def obtener_predicciones_deprecated(jugadores: "list[str]") -> dict:
    predicciones = dict()
    for jugador in jugadores:
        prediccion = input(f"{jugador}, cuantas bazas cree que ganará?: ")
        predicciones[jugador] = prediccion
    return predicciones  
# ------------------

def main():
    clear()
    # jugadores = ingresar_jugadores()
    jugadores = ["Luca", "Marco", "Omar", "Gisela"]
    resultado = whist(jugadores)
    imprimir_resultado(resultado)

if __name__ == "__main__":
    main()