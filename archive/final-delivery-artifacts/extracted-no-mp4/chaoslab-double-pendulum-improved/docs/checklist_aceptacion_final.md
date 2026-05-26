# Checklist de aceptación final - ChaosLab

## 1. Código y reproducibilidad

```bash
python scripts/smoke_test.py
python scripts/export_presentation_data.py
```

Debe aparecer `ChaosLab smoke test passed` y una deriva relativa de energía menor que `1e-4`.

## 2. Presentación principal

Abrir `presentation/index.html` y verificar:

- Slide 1: se entienden dos trayectorias casi iguales que divergen.
- Slide 2: péndulo simple conecta con Física I y Cálculo I.
- Slide 4: coordenadas correctas con signos correctos.
- Slide 6: espacio de ángulos prepara el mapa.
- Slide 7: energía total casi constante y métrica `2.56e-6`.
- Slide 8: divergencia en escala logarítmica y advertencia de no sobreafirmar Lyapunov.
- Slide 9: mapa con ejes, leyenda y lectura de pixel = experimento.
- Slide 10: cierre con determinismo vs predictibilidad práctica.

## 3. Informe

Revisar `report/informe_final.pdf`:

- Planteamiento del problema y objetivos.
- Marco teórico con péndulo simple, doble, energía y EDOs.
- Metodología computacional reproducible.
- Resultados: trayectoria, energía, divergencia y mapa.
- Discusión con limitaciones: sin fricción, sin validación experimental completa, mapa exploratorio.

## 4. Demo/Q&A

```bash
streamlit run app.py
```

Usar presets primero. No improvisar parámetros raros durante la exposición, porque el universo ya es suficientemente hostil.

## 5. Entrega

Subir al repositorio:

- `src/chaoslab/physics.py`
- `src/chaoslab/fractal.py`
- `presentation/`
- `slides/guion_5_min.md`
- `report/`
- `figures/`
- `animations/`
- `README.md`
