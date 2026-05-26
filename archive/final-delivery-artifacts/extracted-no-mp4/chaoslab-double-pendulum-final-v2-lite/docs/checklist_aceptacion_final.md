# Checklist de aceptación final — ChaosLab

## Comandos mínimos

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/smoke_test.py
python scripts/export_presentation_data.py
```

## Comandos opcionales

```bash
python scripts/generate_assets.py
python scripts/render_manim_style_geometry.py
python scripts/build_documents.py
streamlit run app.py
```

Si Manim ya está instalado:

```bash
pip install -r requirements-manim.txt
manim -pqh manim/chaos_geometry_scene.py ChaosGeometryScene
```

## Qué mirar en la presentación

- Slide 1: el hook compara dos condiciones casi iguales.
- Slide 2: el péndulo simple ancla el proyecto en Física I.
- Slide 4: las coordenadas cartesianas son correctas.
- Slide 5: `solve_ivp` aparece como integración de `ds/dt=f(t,s)`.
- Slide 6: `angle-space` muestra `θ₁(t)` contra `θ₂(t)` como puente visual.
- Slide 7: energía total casi constante.
- Slide 8: divergencia con caveat de no Lyapunov formal.
- Slide 9: el mapa se revela como muchos experimentos numéricos.
- Slide 10: cierre honesto: determinismo no implica predictibilidad práctica.

## Métricas esperadas

`python scripts/smoke_test.py` debe imprimir algo del estilo:

```text
ChaosLab smoke test passed
energy_relative_drift < 1e-4
log_delta_slope = número finito
ffmpeg_available=True/False
```

La deriva energética de la corrida usada en presentación suele estar alrededor de `10^-6`, y la pendiente temprana de `log(Delta)` debe ser positiva y finita.

## Artefactos finales

```text
README.md
src/chaoslab/
presentation/index.html
presentation/script.js
presentation/style.css
presentation/data/chaos_data.js
slides/guion_5_min.md
slides/presentacion_final.pdf
report/informe_final.pdf
report/latex/informe_final.tex
figures/
animations/double_pendulum.gif
animations/chaoslab_teaser.mp4
animations/manim_style_geometry.mp4
manim/chaos_geometry_scene.py
```

## Reglas de defensa oral

- No decir “probamos formalmente caos”. Decir “mostramos evidencia numérica de sensibilidad a condiciones iniciales”.
- No improvisar parámetros en vivo si no se probaron antes.
- No depender del WiFi.
- Tener el HTML abierto, el PDF listo y el MP4 como respaldo.
