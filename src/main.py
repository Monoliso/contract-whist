# import collections, functools, operator
from impresion import *
from entrada import *

def whist(jugadores: "list[str]") -> tuple:
    """ Permite jugar una partida de Whist. Maneja la entrada y salida del juego.
        Devuelve una tupla con los ganadores y el puntaje con el que ganaron.   """

    # Herramientas funcionales: lambda, map y filter. También está reduce pero con importación.
    BAZAS_POR_MANO = [i+1 for i in range(8)] + [i for i in range(8, 0, -1)]
    puntos_juego = dict.fromkeys(jugadores, 0)
    imprimir_inicio_juego(jugadores)
    for mano in BAZAS_POR_MANO:
        imprimir_inicio_mano(mano, jugadores[0])
        cartas_en_posesion, triunfo = repartir_cartas(jugadores, mano)
        datos_mano = (mano, cartas_en_posesion, triunfo)
        predicciones = obtener_predicciones(datos_mano, jugadores)
        puntos_mano = jugar_mano(jugadores, datos_mano, predicciones)
        for jugador in puntos_juego.keys():
            puntos_juego[jugador] += puntos_mano[jugador]
        imprimir_puntaje_mano(puntos_mano, puntos_juego)
        jugadores = jugadores[1:] + [jugadores[0]] # Rotar lista de jugadores
    imprimir_resultado_juego(puntos_juego)
    ganador_es = determinar_ganador_juego(puntos_juego)
    return ganador_es

def repartir_cartas(jugadores: "list[str]", numero_bazas: int) -> "tuple[dict, set]":
    """ Dada una lista de jugadores y la cantidad de bazas que se juega,
        se le reparten la cantidad de cartas correspondiente a cada jugador y
        se devuelve el triunfo de la baza. """
    
    PALOS = {'♥️', '♦️', '♠️', '♣️'}
    VALORES = [str(i+1) for i in range(1, 10)] + ['J', 'Q', 'K', 'A']
    cartas_en_posesion = {(x, y):None for y in PALOS for x in VALORES}
    mazo = set(cartas_en_posesion.keys())

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
        cartas_jugador = [carta for carta, nombre in cartas_en_posesion.items() \
            if nombre == jugador]
        imprimir_canto_predicciones(triunfo, jugador, cartas_jugador, predicciones_mano)
        predicciones_mano.update(ingresar_prediccion(jugador, numero_bazas))
        if numero == len(jugadores)-1:
            imprimir_transicion(jugadores[0])
        else: imprimir_transicion(jugadores[numero+1])
    return predicciones_mano

def jugar_mano(jugadores: "list[str]", mano: "tuple[int, dict, tuple]", 
               predicciones: "dict[str:int]") -> "dict[str:int]":
    """ Permite jugar una mano del juego. Maneja la entrada y la salida al usuario.
        Devuelve los puntos que se realizaron en la mano. """
    
    bazas_ganadas = dict.fromkeys(jugadores, 0)
    numero_bazas, cartas_en_posesion, triunfo = mano
    for baza in range(numero_bazas):
        mesa = dict()
        palo_baza = None
        for numero, jugador in enumerate(jugadores):
            cartas_jugador = [carta for carta, nombre in cartas_en_posesion.items() \
                if nombre == jugador]
            imprimir_seleccion_carta(triunfo, mesa, jugador, cartas_jugador)
            jugada = ingresar_jugada(jugador, cartas_jugador, palo_baza, triunfo)
            if numero != len(jugadores)-1:
                imprimir_transicion(jugadores[numero+1])
            if numero == 0:
                palo_baza = jugada
            cartas_en_posesion[jugada] = None
            mesa[jugada] = jugador

        ganador_baza = determinar_ganador_baza(mesa, palo_baza, triunfo)
        bazas_ganadas[ganador_baza] += 1
        jugadores = actualizar_orden_jugadores(jugadores, ganador_baza)
        imprimir_ganador_baza(triunfo, mesa, ganador_baza)
        if baza < numero_bazas-1:
            imprimir_transicion(jugadores[0])

    puntos_mano = determinar_puntos_mano(bazas_ganadas, predicciones)
    return puntos_mano

def determinar_ganador_baza(mesa: "dict[tuple:str]", palo_baza_carta: "tuple[str, str]", \
        triunfo: "tuple[str, str]") -> str:
    """ Devuelve el jugador que ganó la baza. """

    VALORES = [str(i+1) for i in range(1, 10)] + ['J', 'Q', 'K', 'A']
    palo_triunfo = triunfo[1]
    palo_baza = palo_baza_carta[1]
    ganador = palo_baza_carta
    for carta in mesa.keys():
        if carta[1] == palo_triunfo and\
                       (ganador[1] != palo_triunfo or\
                        VALORES.index(carta[0]) > VALORES.index(ganador[0])):
                ganador = carta
        if carta[1] == palo_baza and\
                       ganador[1] != palo_triunfo and\
                       VALORES.index(carta[0]) > VALORES.index(ganador[0]):
            ganador = carta
    jugador_ganador = mesa[ganador]
    return jugador_ganador

def actualizar_orden_jugadores(jugadores: "list[str]", ganador_baza: str) -> "list[str]":
    """ Devuelve una lista con el orden actualizado de los jugadores en una mano. """
    
    numero_ganador = jugadores.index(ganador_baza)
    nueva_lista = jugadores[numero_ganador:] + jugadores[:numero_ganador]
    return nueva_lista

def determinar_puntos_mano(bazas_ganadas: "dict[str:int]", predicciones: "dict[str:int]"):
    """ Computa si las bazas ganadas coinciden con la predicción. Devuelve los puntos 
        finales de la mano. """
    
    puntos_mano = dict()
    for jugador, prediccion in predicciones.items():
        if bazas_ganadas[jugador] == prediccion:
            puntos_mano[jugador] = 10 + bazas_ganadas[jugador]
        else: puntos_mano[jugador] = bazas_ganadas[jugador]
    return puntos_mano

def determinar_ganador_juego(puntaje_juego: dict) -> tuple:
    """ Devuelve el o los jugadores con mayor puntaje. """
    
    mayor_puntaje = max(puntaje_juego.values())
    ganador_es = [jugador for jugador, puntaje in puntaje_juego if puntaje == mayor_puntaje]
    return (ganador_es, mayor_puntaje)

def main():
    clear()
    jugadores = ingresar_jugadores()
    # jugadores = ["Luca", "Marco", "Omar", "Gisela"]
    resultado = whist(jugadores)
    if len(resultado[0]) == 1:
        imprimir_ganador(resultado)
    else:
        imprimir_empate(resultado)

if __name__ == "__main__":
    main()