# Guion final de 5 minutos — ChaosLab

## 0:00–0:25 — Hook: mismas leyes, futuros distintos

Miren estas dos simulaciones. Tienen las mismas masas, las mismas longitudes y obedecen exactamente la misma ecuación diferencial. La única diferencia es que en una de ellas cambié el ángulo inicial de la segunda barra en `10⁻⁶ rad`, una perturbación demasiado pequeña para verla en la pantalla.

Durante unos segundos parecen el mismo sistema. Luego dejan de estar de acuerdo. El proyecto nace de esa tensión: **si la mecánica clásica es determinista, ¿por qué el futuro puede volverse prácticamente impredecible?**

## 0:25–0:55 — Física I base: el péndulo simple

Partimos del caso ordenado de Física I: el péndulo simple. Su posición se describe con un ángulo `θ` medido desde la vertical. La velocidad angular es `ω = dθ/dt`; para oscilaciones pequeñas usamos `sin(θ) ≈ θ`, y aparece un movimiento casi periódico.

Ese caso nos da el vocabulario: posición angular, velocidad angular, energía potencial gravitacional y energía cinética.

## 0:55–1:20 — Segunda masa: cuatro variables acopladas

Al agregar una segunda barra, el estado ya no es solo un ángulo. Ahora es

`s(t) = [θ₁, ω₁, θ₂, ω₂]`.

No cambiamos de leyes. Seguimos usando gravedad, energía y rotación. Lo que cambia es que el movimiento de una barra afecta el movimiento de la otra. Ese acoplamiento es el origen de la complejidad.

## 1:20–1:50 — Modelo geométrico: de ángulos a coordenadas

Para simular no basta con dibujar dos líneas. Primero convertimos ángulos en posiciones:

`x₁ = L₁ sin(θ₁)`, `y₁ = -L₁ cos(θ₁)`.

Luego la segunda masa se calcula desde la primera:

`x₂ = x₁ + L₂ sin(θ₂)`, `y₂ = y₁ - L₂ cos(θ₂)`.

Esto conecta la animación con el modelo físico. Cada punto que aparece en pantalla sale de estas coordenadas.

## 1:50–2:20 — Simulación numérica: resolver, no coreografiar

Las ecuaciones del péndulo doble son acopladas y no tienen una solución analítica simple para condiciones generales. Por eso las resolvemos numéricamente como un problema de valor inicial:

`ds/dt = f(t, s)`.

En el repositorio usamos `solve_ivp`. La simulación recibe una condición inicial, calcula aceleraciones y velocidades, y avanza en el tiempo. La animación no está inventada cuadro por cuadro; es una visualización de la solución numérica.

## 2:20–2:45 — Espacio de ángulos: mirar el movimiento como señal

Antes de saltar al mapa completo, miramos una sola trayectoria de otra forma: graficamos `θ₁` contra `θ₂`.

Esto convierte el movimiento del péndulo en una señal en el espacio de ángulos. La idea tomada de 2swap es importante: primero entendemos una trayectoria individual y después repetimos el experimento para muchas condiciones iniciales.

## 2:45–3:15 — Energía: control de calidad numérica

Antes de hablar de caos, hay que verificar que el integrador no esté inventando energía. Calculamos energía cinética, potencial y total.

La cinética y la potencial se intercambian, pero la energía total permanece casi constante. En esta corrida, la deriva relativa máxima está alrededor de `2.6×10⁻⁶`. Eso no prueba caos, pero sí nos dice que la simulación es confiable para analizar el comportamiento observado.

## 3:15–3:50 — Sensibilidad: una diferencia microscópica crece

Ahora corremos dos simulaciones casi idénticas y medimos

`Δ(t) = ||s(t) - s'(t)||`.

En escala logarítmica, `Δ(t)` crece rápidamente durante la ventana inicial. Esta pendiente es un indicador útil de sensibilidad, pero hay que decirlo bien: **no estamos calculando un exponente de Lyapunov formal**. Estamos mostrando evidencia numérica de sensibilidad a condiciones iniciales.

La frase central es: la pérdida de predictibilidad no aparece porque falten leyes; aparece porque las leyes amplifican diferencias pequeñas.

## 3:40–3:55 — Patrones individuales: el caos tiene reglas ocultas

Antes de ver todo el mapa, observemos tres condiciones iniciales que, contra toda expectativa, generan movimiento perfectamente periódico: un pretzel, un shoelace y un corazón. Las tres repiten su patrón de forma indefinida.

Siguiendo la idea de 2swap: primero presentamos a los individuos y después al grupo. Ahora sí: expandamos la vista a miles de experimentos.

## 3:55–4:15 — Mapa global: cada pixel es un experimento
 
Ahora pasamos de una simulación a miles. Cada pixel del mapa representa una condición inicial: en el eje horizontal está `θ₁(0)` y en el eje vertical está `θ₂(0)`. Para cada punto resolvemos la misma EDO y medimos cuánto tarda en ocurrir el primer flip.

El color codifica ese tiempo. Las zonas claras indican un flip rápido; por eso el mapa se revela como un conjunto de experimentos reales, no como una textura pegada. Lo importante es la frontera irregular: puntos iniciales sumamente cercanos pueden producir futuros drásticamente distintos.

## 4:15–4:35 — Estructuras periódicas: islas de orden en el caos

Pero dentro de esta complejidad, no todo es caos. Si miramos las regiones oscuras del mapa global —lo que llamamos islas de estabilidad— encontramos algo fascinante: trayectorias que repiten el mismo patrón de manera indefinida.

Como ven en la simulación adjunta en pantalla, bajo la condición inicial marcada por la mira de cruz (`θ₁ = 92°`, `θ₂ = -96°`), el péndulo dibuja un pretzel ordenado y recurrente. Estas órbitas demuestran que el determinismo físico puede albergar tanto una sensibilidad caótica extrema como hermosas estructuras de orden periódico estable.

## 4:35–5:00 — Cierre: determinismo no es predictibilidad práctica

ChaosLab muestra que un sistema de mecánica clásica puede ser perfectamente determinista y aun así difícil de predecir en la práctica. Las reglas son fijas; lo complejo es que pequeñas incertidumbres iniciales pueden crecer hasta cambiar el resultado observable.

El alcance de nuestro trabajo es honesto: sin rozamiento, sin medición experimental directa y sin exponente de Lyapunov formal. Pero el núcleo está completo: modelo físico, integración reproducible, conservación de energía como control de calidad, divergencia temporal entre trayectorias y mapa de condiciones iniciales. Muchas gracias.
