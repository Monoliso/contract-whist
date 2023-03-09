# import collections, functools, operator
from whist import entrada, impresion, logica

def whist(orden_jugadores: "list[str]") -> tuple:
    """ Permite jugar una partida de Whist. Maneja la entrada y salida del juego.
        Devuelve una tupla con los ganadores y el puntaje con el que ganaron. """

    # Herramientas funcionales: lambda, map y filter. También está reduce pero con importación.
    BAZAS_POR_MANO = [i+1 for i in range(8)] + [i for i in range(8, 0, -1)]
    puntos_juego = dict.fromkeys(orden_jugadores, 0)
    impresion.imprimir_inicio_juego(orden_jugadores)
    for mano in BAZAS_POR_MANO:
        impresion.imprimir_inicio_mano(mano, orden_jugadores[0])
        cartas_jugadores, triunfo = logica.repartir_cartas(orden_jugadores, mano)
        datos_mano = (mano, orden_jugadores, cartas_jugadores, triunfo)
        predicciones = obtener_predicciones(datos_mano)
        puntos_mano = jugar_mano(datos_mano, predicciones)
        for jugador in puntos_juego.keys():
            puntos_juego[jugador] += puntos_mano[jugador]
        impresion.imprimir_puntaje_mano(puntos_mano, puntos_juego)
        orden_jugadores = orden_jugadores[1:] + [orden_jugadores[0]]  # Rotar lista de jugadores
    impresion.imprimir_resultado_juego(puntos_juego)
    ganador_es = logica.determinar_ganador_juego(puntos_juego)
    return ganador_es


def obtener_predicciones(mano: tuple) -> "dict[str:int]":
    """ Dado el triunfo de la baza, las cartas de los jugadores, y el orden para
        solicitar cada prediccion, esta función se encarga de mostrarle a cada uno
        la información pertinente para que pueda realizar la prediccion de la mano. """

    numero_bazas, jugadores, cartas_jugadores, triunfo = mano
    predicciones_mano = dict()
    for numero, jugador in enumerate(jugadores):
        cartas_jugador = cartas_jugadores[jugador]
        impresion.imprimir_canto_predicciones(triunfo, jugador, cartas_jugador, predicciones_mano)
        predicciones_mano.update(entrada.ingresar_prediccion(jugador, numero_bazas))
        if numero == len(jugadores)-1:
            impresion.imprimir_transicion(jugadores[0])
        else:
            impresion.imprimir_transicion(jugadores[numero+1])
    return predicciones_mano


def jugar_mano(mano: tuple, predicciones: dict) -> "dict[str:int]":
    """ Permite jugar una mano del juego. Maneja la entrada y la salida al usuario.
        Devuelve los puntos que se realizaron en la mano. """

    numero_bazas, jugadores, cartas_jugadores, triunfo = mano
    bazas_ganadas = dict.fromkeys(jugadores, 0)
    for baza in range(numero_bazas):
        mesa = dict()
        palo_baza = None
        for numero, jugador in enumerate(jugadores):
            cartas_jugador: list = cartas_jugadores[jugador]
            impresion.imprimir_seleccion_carta(triunfo, mesa, jugador, cartas_jugador)
            jugada = entrada.ingresar_jugada(jugador, cartas_jugador, palo_baza, triunfo)
            if numero == 0:
                palo_baza = jugada
            cartas_jugador.remove(jugada)
            cartas_jugadores[jugador] = cartas_jugador
            mesa[jugada] = jugador
            if numero != len(jugadores)-1:
                impresion.imprimir_transicion(jugadores[numero+1])
        ganador_baza = logica.determinar_ganador_baza(mesa, palo_baza, triunfo)
        bazas_ganadas[ganador_baza] += 1
        jugadores = logica.actualizar_orden_jugadores(jugadores, ganador_baza)
        impresion.imprimir_ganador_baza(triunfo, mesa, ganador_baza)
        if baza < numero_bazas-1:
            impresion.imprimir_transicion(jugadores[0])
    puntos_mano = logica.determinar_puntos_mano(bazas_ganadas, predicciones)
    return puntos_mano


def main():
    impresion.clear()
    # jugadores = ingresar_jugadores()
    jugadores = ["Luca", "Marco", "Omar", "Gisela"]
    resultado = whist(jugadores)
    if len(resultado[0]) == 1:
        impresion.imprimir_ganador(resultado)
    else:
        impresion.imprimir_empate(resultado)


if __name__ == "__main__":
    main()
