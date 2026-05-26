# ChaosLab: Double Pendulum as Classical Chaos

**ChaosLab** es una simulación computacional del péndulo doble para un proyecto final de Física. El objetivo es visualizar cómo un sistema mecánico clásico, gobernado por ecuaciones deterministas, puede perder predictibilidad práctica por sensibilidad extrema a condiciones iniciales.

La estética está inspirada en videos tipo 2swap / 3Blue1Brown: fondo oscuro, colores de alto contraste, trayectorias continuas, mapas de condiciones iniciales y una narrativa donde la visualización no adorna la explicación, sino que la lleva. Pequeña victoria contra el PowerPoint con 97 viñetas.

## Pregunta central

¿Cómo cambia la predictibilidad de un sistema mecánico al pasar de un péndulo simple a un péndulo doble, y cómo se evidencia la sensibilidad a condiciones iniciales mediante simulación numérica, conservación de energía y mapas de condiciones iniciales?

## Qué incluye

- Modelo físico del péndulo doble como sistema de EDOs.
- Simulación con `scipy.integrate.solve_ivp`.
- Cálculo de energía cinética, potencial y total.
- Comparación de dos trayectorias separadas inicialmente por una perturbación minúscula.
- Mapa de condiciones iniciales: color = tiempo hasta el primer giro completo.
- App interactiva en Streamlit.
- Figuras y GIF listos para presentación.
- Guion de video corto estilo divulgación matemática.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Generar figuras y GIF

```bash
python scripts/generate_assets.py
```

Los resultados aparecen en:

```text
figures/
animations/
data/
```

## Correr la app

```bash
streamlit run app.py
```

## Estructura

```text
src/chaoslab/physics.py   # EDOs, energía, divergencia
src/chaoslab/fractal.py   # mapa vectorizado de tiempo hasta flip
src/chaoslab/visuals.py   # figuras y animaciones
scripts/generate_assets.py
app.py
docs/propuesta.md
docs/guion_video.md
docs/informe_esqueleto.md
```

## Resultados esperados

1. La trayectoria de la segunda masa forma patrones complejos aun cuando la energía total se conserva aproximadamente.
2. Dos trayectorias con diferencia inicial de apenas `1e-6 rad` terminan separándose.
3. El mapa de condiciones iniciales muestra regiones con fronteras complejas: pequeñas variaciones cambian el tiempo hasta el primer flip.

## Nota sobre IA / ML

No se usa aprendizaje automático como núcleo porque el fenómeno físico ya es rico y defendible sin convertir el informe en una nube de humo con GPU. Si se añade IA, debe ir como extensión: por ejemplo, entrenar un modelo liviano para clasificar si una condición inicial hará flip antes de cierto tiempo a partir de los datos generados por `flip_time_map`. Primero física, luego IA. Sí, en ese orden, aunque LinkedIn llore.
