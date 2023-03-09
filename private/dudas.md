# Dudas

## Los errores

A la hora de devolver si una jugada es válida o no, no me sirve verificar eso *per se*, porque el problema radica en cómo obtengo la *causa del problema.*
Es por eso que en el lenguaje C por ejemplo, lo mejor es devolver un número asociado a una salida, determinando qué tipo de error se ha realizado. Pero eso ni siquiera alcanza en la mayoría de los casos, porque requiero más información, causa y explicitar *por ejemplo, la posición inválida.*

Es por eso en donde *creo* que habría que reconocer corréctamente qué herramientas tiene uno para devolver dicha información. Una opción es un tipo de dato que asocie y contenga el tipo de error, ya sea una estructura o un objeto. Otra, relacionado con Python, es devolver una Excepción, que desconozco sus límites pero, entiendo, puede contener información para la depuración.

Esto de hacer funciones puras duele a veces.


## Las dependencias

Realmente intento separar los bloques de la forma más individualmente posible, pero es complicado...
La función para ingresar una jugada (creo) que tendría sentido que devuelva una jugada válida, pero para hacer eso hay que chequear e imprimir, funciones que ubiqué en otros archivos porque me parecía que tenía sentido... LPTM.