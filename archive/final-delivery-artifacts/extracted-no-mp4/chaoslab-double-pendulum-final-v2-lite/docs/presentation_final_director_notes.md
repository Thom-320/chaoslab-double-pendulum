# Notas de dirección técnica — presentación final ChaosLab

## Veredicto de formato

Formato principal recomendado: **presentación HTML animada en vivo**, con `animations/chaoslab_teaser.mp4` o `animations/chaoslab_pitch_5min.mp4` como respaldo si se conserva el archivo grande, y `streamlit run app.py` como demo opcional para preguntas. No conviene migrar todo a Manim ni a un pipeline tipo Swaptube: el proyecto ya tiene datos, canvas, assets, reporte y video. Reescribirlo ahora cambiaría riesgo por vanidad, ese combustible renovable de los proyectos que fallan.

## Diagnóstico breve

Fortalezas actuales: el modelo físico está bien anclado en Física I, las coordenadas son explícitas, la integración numérica es reproducible, la conservación de energía funciona como control de calidad y el mapa de condiciones iniciales ya existe.

Debilidades corregidas: el mapa aparecía demasiado como imagen final y no como resultado de muchos experimentos computacionales; faltaba una escena puente entre trayectoria individual y mapa global; el guion necesitaba más cuidado con el sobre-reclamo de “caos”; y la escena de divergencia necesitaba una advertencia clara de que la pendiente no es un exponente de Lyapunov formal.

## Chunks de referencia 2swap adaptados

1. **Hook:** contraste entre trayectorias casi idénticas y futuros distintos. En ChaosLab se usa la perturbación `10⁻⁶ rad`.
2. **Construcción del modelo:** pasar de péndulo simple a estado `[θ₁,ω₁,θ₂,ω₂]` y coordenadas cartesianas.
3. **Visualización local:** una trayectoria en espacio angular `θ₁(t)` contra `θ₂(t)`. Este puente es esencial antes del mapa.
4. **Mapa global:** cada pixel es una simulación. El mapa se revela progresivamente para que parezca un experimento repetido, no una imagen pegada.
5. **Cierre:** determinismo no implica predictibilidad práctica, sin venderlo como prueba formal completa de caos.

## Cambios realizados en esta iteración

- `presentation/index.html`: se añadió la escena `angle-space` entre simulación y energía; se actualizaron tiempos de exposición.
- `presentation/script.js`: se añadió `drawAngleSpace`, que deriva `θ₁` y `θ₂` desde las posiciones ya exportadas y dibuja la huella angular de un experimento individual.
- `presentation/style.css`: ajustes menores para la nueva escena.
- `slides/guion_5_min.md` y `docs/guion_video.md`: guion final cronometrado con la escena puente.
- `manim/chaos_geometry_scene.py`: escena opcional de Manim para mostrar el modelado geométrico con estética 3Blue1Brown.
- `requirements-manim.txt`: dependencias opcionales para renderizar Manim, separadas de la entrega principal.
- `docs/codex_antigravity_prompt.md`: prompt actualizado para revisión final externa.
- `docs/checklist_aceptacion_final.md`: comandos y criterios de aceptación.

## Riesgo restante

El video MP4 de 5 minutos no debe ser la pieza principal si no está sincronizado con la escena `angle-space`. La presentación HTML es más flexible para exposición oral. El MP4 debe quedar como respaldo, no como dependencia única.
