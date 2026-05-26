# ChaosLab - formato final recomendado

## Formato de entrega oral

Usar **presentación híbrida**:

1. `presentation/index.html` como superficie principal de exposición en vivo.
2. `animations/chaoslab_teaser.mp4` o `animations/chaoslab_pitch_5min.mp4` como respaldo si el navegador/proyector falla.
3. `app.py` en Streamlit solo para preguntas o demo posterior, no como hilo principal de los 5 minutos.
4. `report/informe_final.pdf` como entregable académico.

La presentación HTML es preferible al PDF porque permite mostrar movimiento, espacio de ángulos y mapa con preparación narrativa. El PDF funciona como respaldo, pero no debe ser la experiencia principal.

## Comandos mínimos

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python scripts/smoke_test.py
python scripts/export_presentation_data.py
streamlit run app.py           # opcional, para Q&A
```

Abrir localmente:

```text
presentation/index.html
```

Controles: flecha derecha/espacio para avanzar, flecha izquierda para retroceder, `N` para notas.

## Criterios de aceptación visual

- Cada slide debe tener una idea central, no una lista.
- El slide de geometría debe explicar las coordenadas antes de mostrar energía.
- El slide de espacio de ángulos debe preparar el mapa global.
- El mapa debe leerse como miles de experimentos numéricos, no como imagen decorativa.
- La frase final debe ser: determinismo no implica predictibilidad práctica.
