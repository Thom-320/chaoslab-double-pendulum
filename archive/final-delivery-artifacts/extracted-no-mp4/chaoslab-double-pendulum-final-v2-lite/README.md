# ChaosLab: Double Pendulum as Classical Chaos

**ChaosLab** es una simulación computacional del péndulo doble para un proyecto final de Física. El objetivo es visualizar cómo un sistema mecánico clásico, gobernado por ecuaciones deterministas, puede perder predictibilidad práctica por sensibilidad extrema a condiciones iniciales.

La estética está inspirada en videos tipo 2swap / 3Blue1Brown: fondo oscuro, colores de alto contraste, trayectorias continuas, mapas de condiciones iniciales y una narrativa donde la visualización no adorna la explicación, sino que la lleva.

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
- Presentación HTML animada para exposición en vivo.
- Guion y video corto estilo divulgación matemática.
- Clip opcional `animations/manim_style_geometry.mp4` y escena Manim `manim/chaos_geometry_scene.py` para reforzar la explicación geométrica.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Dependencia de sistema para video:

```bash
ffmpeg -version
```

Dependencia de sistema para el informe PDF:

```bash
latexmk -v
pdflatex --version
```

Si FFmpeg no existe, instala FFmpeg antes de renderizar MP4. Si `latexmk` o `pdflatex` no existen, instala una distribucion LaTeX antes de regenerar `report/informe_final.pdf`. Manim queda como ruta opcional; la entrega principal no depende de Manim.

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


## Clip opcional estilo Manim

La entrega principal **no depende de Manim**. Para tener un guiño visual tipo 3Blue1Brown sin convertir la entrega en una guerra de dependencias, el repositorio incluye dos rutas:

```bash
python scripts/render_manim_style_geometry.py
```

Esto genera:

```text
animations/manim_style_geometry.mp4
```

Si Manim ya está instalado localmente, también se puede renderizar la escena opcional:

```bash
pip install -r requirements-manim.txt
manim -pqh manim/chaos_geometry_scene.py ChaosGeometryScene
```

Ese clip es decorativo y pedagógico; la defensa académica sigue siendo la simulación reproducible, energía, divergencia y mapa de condiciones iniciales.

## Correr la app

```bash
streamlit run app.py
```

## Presentación animada

Primero exporta los datos compactos usados por la presentación:

```bash
python scripts/export_presentation_data.py
```

Luego abre:

```text
presentation/index.html
```

Controles:

- Flecha derecha, espacio o botón `Siguiente`: avanzar.
- Flecha izquierda o botón `Anterior`: retroceder.
- `N` o botón `Notas`: mostrar/ocultar guion del presentador.

## Verificación y entregables finales

```bash
python scripts/smoke_test.py
python scripts/build_documents.py
python scripts/render_pitch_video.py
```

Entregables finales:

```text
report/latex/informe_final.tex
report/latex/references.bib
report/informe_final.md
report/informe_final.pdf
slides/presentacion_final.pdf
slides/guion_5_min.md
animations/chaoslab_pitch_5min.mp4
presentation/index.html
```

## Estructura

```text
src/chaoslab/physics.py   # EDOs, energía, divergencia
src/chaoslab/fractal.py   # mapa vectorizado de tiempo hasta flip
src/chaoslab/visuals.py   # figuras y animaciones
scripts/generate_assets.py
scripts/render_pitch_video.py
scripts/build_documents.py
scripts/export_presentation_data.py
scripts/smoke_test.py
app.py
docs/propuesta.md
slides/guion_5_min.md
report/latex/informe_final.tex
report/informe_final.md
presentation/index.html
```

## Resultados esperados

1. La trayectoria de la segunda masa forma patrones complejos aun cuando la energía total se conserva aproximadamente.
2. Dos trayectorias con diferencia inicial de apenas `1e-6 rad` terminan separándose.
3. El mapa de condiciones iniciales muestra regiones con fronteras complejas: pequeñas variaciones cambian el tiempo hasta el primer flip.

## Nota sobre IA / ML

No se usa aprendizaje automático como núcleo porque el fenómeno físico ya es rico y defendible sin desplazar el foco del curso. Si se añade IA, debe ir como extensión: por ejemplo, entrenar un modelo liviano para clasificar si una condición inicial hará flip antes de cierto tiempo a partir de los datos generados por `flip_time_map`. La tesis central del proyecto sigue siendo física: dinámica no lineal, energía mecánica y sensibilidad a condiciones iniciales.
