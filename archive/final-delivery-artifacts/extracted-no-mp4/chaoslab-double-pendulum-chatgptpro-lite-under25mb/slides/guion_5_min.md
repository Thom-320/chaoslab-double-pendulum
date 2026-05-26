# Guion de 5 minutos - ChaosLab

## 0:00-0:25 - Hook

Miren estos dos pendulos. A simple vista empiezan igual. Obedecen las mismas leyes, tienen las mismas masas y longitudes, y la diferencia inicial es de apenas `1e-6 rad`. Eso es invisible para nosotros. Sin embargo, despues de unos segundos, sus futuros se separan.

La pregunta del proyecto es: **si las leyes son deterministas, por que el futuro deja de ser predecible?**

## 0:25-0:55 - Fisica I base

Partimos del pendulo simple, un sistema clasico de Fisica I. Su posicion se describe con un angulo `theta`. La velocidad angular es `d theta / dt` y la aceleracion angular es `d^2 theta / dt^2`. Para angulos pequenos usamos `sin(theta) ~= theta`, y por eso aparece un movimiento casi periodico.

Ese es el caso ordenado: energia potencial se transforma en energia cinetica y luego vuelve.

## 0:55-1:25 - Agregar una segunda masa

Ahora agregamos una segunda masa. El estado ya no es solo un angulo: es `[theta1, omega1, theta2, omega2]`. El movimiento de una barra afecta a la otra. Las ecuaciones quedan acopladas y aparecen terminos no lineales.

No cambiamos de universo fisico. Seguimos usando gravedad, energia y movimiento rotacional. Solo aumentamos el numero de grados de libertad.

## 1:25-2:05 - Simulacion numerica

Como las ecuaciones del pendulo doble no tienen una solucion analitica simple para condiciones generales, resolvemos el sistema numericamente. En Python usamos `solve_ivp`, que integra problemas de valor inicial para sistemas de ecuaciones diferenciales.

La simulacion recibe una condicion inicial, calcula velocidades y aceleraciones, y avanza en el tiempo. El resultado no es una animacion inventada: cada punto sale de integrar el modelo fisico.

## 2:05-2:45 - Energia como prueba de calidad

Antes de hablar de caos, hay que comprobar que el modelo no esta fallando. Por eso calculamos energia cinetica, potencial y total.

La cinetica y la potencial suben y bajan, pero la energia total permanece casi constante. Esa es la prueba clave: la divergencia no aparece porque el integrador este creando energia de la nada. Aparece porque el sistema es no lineal.

## 2:45-3:35 - Sensibilidad inicial

Ahora corremos dos simulaciones. La segunda solo cambia `theta2(0)` en `1e-6 rad`. Medimos la distancia entre ambos estados con `Delta(t)`.

En escala logaritmica, la distancia crece rapidamente durante la ventana inicial. No estamos afirmando un exponente de Lyapunov formal; estamos mostrando una evidencia cuantitativa de sensibilidad a condiciones iniciales.

La frase central es esta: **la perdida de predictibilidad no aparece por falta de leyes, sino porque las leyes amplifican diferencias pequenas.**

## 3:35-4:35 - Mapa de condiciones iniciales

Ahora convertimos una simulacion en miles. Cada pixel del mapa es un experimento: escogemos `theta1(0)` y `theta2(0)`, soltamos el pendulo y medimos cuanto tarda en hacer el primer flip.

Las zonas oscuras no hacen flip dentro de la ventana simulada. Las regiones de color hacen flip en distintos tiempos. Lo importante son las fronteras: pequenas variaciones en el punto inicial pueden cambiar completamente el resultado.

Este es el momento 2swap del proyecto: una regla local sencilla produce una imagen global compleja.

## 4:35-5:00 - Cierre

ChaosLab muestra que un sistema clasico puede ser determinista y, aun asi, dificil de predecir en la practica. La fisica da las reglas; la computacion nos deja ver sus consecuencias.

Como trabajo futuro, se puede agregar validacion experimental con video tracking, comparar integradores o entrenar un modelo surrogate que clasifique regiones de estabilidad. Pero el nucleo ya esta: mecanica clasica, calculo, energia, ecuaciones diferenciales y visualizacion.
