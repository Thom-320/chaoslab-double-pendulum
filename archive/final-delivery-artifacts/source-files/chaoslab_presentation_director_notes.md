# Notas de dirección técnica — presentación final ChaosLab

## Veredicto de formato

Formato principal recomendado: **presentación HTML animada en vivo**, con `animations/chaoslab_pitch_5min.mp4` como respaldo y `streamlit run app.py` como demo opcional para preguntas. No conviene migrar todo a Manim ni a un pipeline tipo Swaptube en esta etapa: el proyecto ya tiene datos, canvas, assets, reporte y video; reescribirlo ahora cambiaría riesgo por vanidad, ese combustible renovable de los proyectos que fallan.

## Diagnóstico breve

Fortalezas actuales: el modelo físico está bien anclado en Física I, las coordenadas son explícitas, la integración numérica es reproducible, la conservación de energía funciona como control de calidad y el mapa de condiciones iniciales ya existe.

Debilidades actuales: el mapa aparecía demasiado como imagen final y no como resultado de miles de experimentos computacionales; el guion necesitaba más cuidado con el sobre-reclamo de “caos”; había falta de tildes y pulido en el español; y la escena de divergencia necesitaba una advertencia clara de que la pendiente no es un exponente de Lyapunov formal.

## Chunks de referencia 2swap adaptados

1. **Hook:** contraste entre trayectorias casi idénticas y futuros distintos. En ChaosLab se usa la perturbación `10⁻⁶ rad`.
2. **Construcción del modelo:** pasar de péndulo simple a estado `[θ₁,ω₁,θ₂,ω₂]` y coordenadas cartesianas.
3. **Visualizaciones locales:** trayectoria, energía y divergencia. Aquí se sacrifica el audio de 2swap para mantener una defensa de Física I más fuerte.
4. **Mapa global:** cada pixel es una simulación. Este era el punto débil y quedó reforzado con un mapa progresivo en canvas.
5. **Cierre:** determinismo no implica predictibilidad práctica, sin venderlo como prueba formal completa de caos.

## Cambios realizados

- `presentation/index.html`: copy pulido, tildes, métricas, caveat de Lyapunov y nuevo mapa narrativo.
- `presentation/script.js`: render progresivo del mapa usando una malla reducida real exportada desde `data/flip_time_map_120.npz`.
- `presentation/style.css`: estilos para métricas, caveats y mapa computacional.
- `scripts/export_presentation_data.py`: ahora exporta un payload reducido del mapa para el HTML.
- `scripts/smoke_test.py`: ahora verifica que la presentación tenga datos, mapa y advertencia de no sobre-reclamo.
- `slides/guion_5_min.md`: guion final cronometrado.
- `src/chaoslab/physics.py`: se quitaron frases coloquiales en docstrings para dejar el código más profesional.

## Riesgo restante

El video MP4 ya existe, pero no conviene regenerarlo justo antes de entregar salvo que sea estrictamente necesario. La versión HTML es más flexible para exposición oral y el MP4 debe quedar como respaldo si el navegador o el proyector deciden participar en la tragedia.
