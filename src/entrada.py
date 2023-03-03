""" Este modulo incluye todas las funciones para obtener la entrada del usuario. """

import random


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
            elif corroborar_jugada(cartas_jugador, jugada, palo_baza[1], triunfo[1]):
                condicion = False
        except ValueError:
            input("Debe ingresar un número.")
    return cartas_jugador[jugada-1]


def ingresar_eleccion_orden(jugador) -> list:
    condicion = True
    while condicion:
        try:
            eleccion = int(input(f"\n{jugador}, cuál es su elección de ordenamiento?: "))
            if eleccion != 1 or eleccion != 2:
                input("Debe ingresar 1 o 2.")
            else:
                condicion = False
        except ValueError:
            input("Debe ingresar un número.")
    return eleccion
        

def corroborar_jugada(cartas_jugador: "list[tuple]", jugada: int,
                      palo_baza: str, palo_triunfo: str) -> bool:

    carta_seleccionada = cartas_jugador[jugada-1]
    palo_carta = carta_seleccionada[1]
    tiene_palo = False
    tiene_triunfo = False
    palos_baza_disponibles: list[int] = list()
    palos_triunfo_disponibles: list[int] = list()
    if palo_carta == palo_baza:
        return True
    for numero, carta in enumerate(cartas_jugador):
        if carta[1] == palo_baza:
            tiene_palo = True
            palos_baza_disponibles.append(numero+1)
        if carta[1] == palo_triunfo:
            tiene_triunfo = True
            palos_triunfo_disponibles.append(numero+1)
    if not tiene_palo and palo_carta == palo_triunfo:
        return True
    if not tiene_palo and not tiene_triunfo:
        return True
    if tiene_palo:
        print(f"Seleccionó una carta con un palo distinto al de la baza teniendo "
              f"al menos una carta con dicho palo ('{palo_baza}').")
        print("Debe seleccionar alguna de sus cartas con el palo de la baza.\n"
              f"Las que cumplen con la condición son las numero {palos_baza_disponibles}.")
    else:
        print(f"Seleccionó una carta con un palo distinto al de triunfo teniendo "
              f"al menos una carta con dicho palo ('{palo_triunfo}').")
        print("Debe seleccionar alguna de sus cartas con el palo de triunfo, ya que no "
                "tiene ninguna con el palo de la baza.\n"
                f"Las que cumplen con la condición son las numero {palos_triunfo_disponibles}.")
    return False
