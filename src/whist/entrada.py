""" Este modulo incluye todas las funciones para obtener la entrada del usuario. """

import random
from whist.logica import corroborar_jugada
from whist.impresion import imprimir_error_jugada

def ingresar_jugadores():
    """ Se solicita al usuario inicial que ingrese los nombres de los jugadores separados por
        coma. La cantidad mínima es 3, y la máxima 7. """

    condicion = True
    while condicion:
        entrada_usuario = input("Ingrese los nombres de los jugadores separados por coma: ")
        jugadores_lista = entrada_usuario.split(',')
        jugadores = [jugador.replace(' ', '') for jugador in jugadores_lista]
        if len(jugadores) < 3 or len(jugadores) > 7:
            print("La cantidad de jugadores no es correcta, debe ser de 3 a 7 jugadores."
                  " Vuelva a intentarlo.")
        else:
            random.shuffle(jugadores)
            condicion = False
    return jugadores


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


def ingresar_jugada(jugador: str, cartas_jugador: "list[tuple]",
                    palo_baza: tuple, triunfo: tuple) -> "tuple[str, str]":
    condicion = True
    while condicion:
        try:
            jugada = int(input(f"\n{jugador}, qué carta desea jugar?: "))
            if (jugada > (largo:=len(cartas_jugador)) or jugada <= 0):
                input(f"Debe seleccionar una carta dentro del rango 1-{largo}.")
            elif not palo_baza:
                condicion = False
            else:
                validacion_jugada = corroborar_jugada(cartas_jugador, jugada, palo_baza[1], triunfo[1])
                if validacion_jugada[0]:
                    condicion = False
                else:
                    imprimir_error_jugada(validacion_jugada[1], palo_baza[1], validacion_jugada[2])
        except ValueError:
            input("Debe ingresar un número.")
    return cartas_jugador[jugada-1]
