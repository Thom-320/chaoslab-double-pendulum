# Informe final — Esqueleto

## Resumen
Se desarrolló una simulación computacional del péndulo doble para estudiar la transición entre movimiento regular y comportamiento caótico en un sistema mecánico clásico. Se resolvió numéricamente un sistema de ecuaciones diferenciales ordinarias acopladas y se analizaron trayectorias, conservación de energía, sensibilidad a condiciones iniciales y mapas de tiempo hasta el primer giro completo.

## 1. Planteamiento del problema
El péndulo simple es uno de los modelos más conocidos de movimiento oscilatorio. Sin embargo, al acoplar dos péndulos, las mismas leyes de Newton generan un sistema no lineal cuya evolución puede ser altamente sensible a pequeñas variaciones en las condiciones iniciales. El problema consiste en explicar y visualizar cómo surge esa pérdida práctica de predictibilidad.

## 2. Objetivos
Incluir objetivo general y objetivos específicos de `docs/propuesta.md`.

## 3. Marco teórico
- Péndulo simple y aproximación de ángulo pequeño.
- Coordenadas angulares, velocidad angular y aceleración angular.
- Energía cinética y potencial gravitacional.
- Conservación de energía.
- Sistemas de ecuaciones diferenciales ordinarias.
- Sensibilidad a condiciones iniciales y caos.

## 4. Metodología
- Implementación en Python.
- Parámetros físicos utilizados.
- Integración con `solve_ivp`.
- Métrica de divergencia entre trayectorias.
- Mapa de condiciones iniciales por integración vectorizada.
- Visualizaciones y demo.

## 5. Resultados
Insertar:
1. `figures/trajectory_mass2.png`
2. `figures/energy_vs_time.png`
3. `figures/energy_vs_time_relative_error.png`
4. `figures/divergence_semilog.png`
5. `figures/flip_time_fractal_map.png`

## 6. Discusión
La energía total casi constante valida que la integración conserva razonablemente la estructura física. La divergencia entre trayectorias muestra sensibilidad a condiciones iniciales. El mapa de flip time evidencia regiones estables e inestables con frontera compleja, lo cual conecta con la estructura fractal reportada en la literatura.

## 7. Conclusiones
El péndulo doble muestra que un sistema clásico gobernado por leyes deterministas puede ser prácticamente impredecible a largo plazo debido a la sensibilidad a condiciones iniciales. La simulación permite visualizar y cuantificar el fenómeno de manera reproducible.
