# Guion final de 5 minutos - ChaosLab

## 0:00-0:25 - Hook

Miren estos dos péndulos. A simple vista empiezan igual: mismas masas, mismas longitudes y las mismas leyes de Newton. La única diferencia es una perturbación inicial de apenas `1e-6 rad`, invisible para cualquier montaje de aula.

La pregunta del proyecto es: **si el sistema es determinista, por qué el futuro deja de ser predecible en la práctica?**

## 0:25-0:55 - Física I base

Partimos del péndulo simple, un sistema clásico de Física I. Su posición se describe con un ángulo `theta`; su velocidad angular es `omega = dtheta/dt`; y su aceleración angular es `d²theta/dt²`. Para ángulos pequeños usamos la aproximación de Cálculo I `sin(theta) ≈ theta`, y el movimiento se vuelve casi periódico.

Ese es nuestro caso ordenado: energía potencial y energía cinética se intercambian de forma regular.

## 0:55-1:20 - Agregar una segunda masa

Ahora agregamos una segunda masa. El estado ya no es un solo ángulo: es `[theta1, omega1, theta2, omega2]`. El movimiento de una barra afecta a la otra. Las ecuaciones quedan acopladas y aparecen términos no lineales.

No cambiamos de universo físico. Seguimos usando gravedad, energía y rotación. Solo aumentamos los grados de libertad. Naturalmente, con dos variables más, la naturaleza decide ponerse dramática.

## 1:20-1:55 - Modelo geométrico

Las posiciones no se dibujan a ojo. Salen de trigonometría:

`x1 = L1 sin(theta1)`, `y1 = -L1 cos(theta1)`, `x2 = x1 + L2 sin(theta2)`, `y2 = y1 - L2 cos(theta2)`.

Esta escena importa porque conecta vectores, coordenadas y derivadas. Una vez tenemos posición, podemos calcular velocidad, energía y evolución temporal.

## 1:55-2:20 - Simulación numérica

Como las ecuaciones del péndulo doble son acopladas y no lineales, para condiciones generales no usamos una fórmula cerrada simple. Resolvemos un problema de valor inicial: `ds/dt = f(t,s)`.

En Python se integra con `solve_ivp`. La animación no es decoración: cada frame sale de resolver el modelo físico.

## 2:20-2:45 - Espacio de ángulos

Ahora dejamos de mirar solo la masa y miramos la señal del sistema. Graficamos `theta1` contra `theta2`. Un movimiento regular dibujaría una curva limpia; un movimiento más complejo empieza a llenar el espacio de forma irregular.

Esta escena prepara el mapa final: primero estudiamos una trayectoria; luego repetimos el experimento para miles de condiciones iniciales.

## 2:45-3:20 - Energía como prueba de calidad

Antes de hablar de sensibilidad, hay que verificar que el modelo no esté fallando. Calculamos energía cinética, potencial y total.

La cinética y la potencial suben y bajan, pero la energía total permanece casi constante. En el caso base, la deriva relativa máxima es aproximadamente `2.56e-6`. Esa es la prueba clave: la divergencia no aparece porque el integrador esté creando energía de la nada.

## 3:20-3:55 - Sensibilidad inicial

Ahora corremos dos simulaciones. La segunda solo cambia `theta2(0)` en `1e-6 rad`. Medimos la distancia entre ambos estados con `Delta(t)`.

En escala logarítmica, la distancia crece rápidamente durante la ventana inicial. No afirmamos un exponente de Lyapunov formal; mostramos evidencia numérica de sensibilidad a condiciones iniciales.

La frase central es esta: **la pérdida de predictibilidad no aparece por falta de leyes, sino porque las leyes amplifican diferencias pequeñas.**

## 3:55-4:35 - Mapa de condiciones iniciales

Ahora convertimos una simulación en miles. Cada pixel del mapa es un experimento: escogemos `theta1(0)` y `theta2(0)`, soltamos el péndulo desde el reposo y medimos cuánto tarda en hacer el primer flip.

Las zonas oscuras no hacen flip dentro de la ventana simulada. Las regiones de color hacen flip en distintos tiempos. Lo importante son las fronteras: pequeñas variaciones iniciales pueden cambiar drásticamente el resultado.

Este es el cierre visual del proyecto: una regla local determinista produce una imagen global compleja.

## 4:35-5:00 - Cierre

ChaosLab muestra que un sistema clásico puede ser determinista y, aun así, difícil de predecir en la práctica. La física da las reglas; la computación revela sus consecuencias.

Como trabajo futuro se puede agregar validación experimental con video tracking, comparar integradores o entrenar un modelo surrogate que clasifique regiones de estabilidad. Pero el núcleo ya está: mecánica clásica, Cálculo I, energía, ecuaciones diferenciales y visualización científica.
