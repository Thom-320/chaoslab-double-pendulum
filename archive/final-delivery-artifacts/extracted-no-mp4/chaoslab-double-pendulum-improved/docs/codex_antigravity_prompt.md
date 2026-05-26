# Prompt para Codex / Google Antigravity 2.0

Actúa como ingeniero de software científico, diseñador de visualizaciones y revisor académico. Trabaja sobre el repositorio `chaoslab-double-pendulum` sin romper lo existente.

Objetivo: pulir la entrega final de ChaosLab para un proyecto final de Física I. El formato recomendado es híbrido: `presentation/index.html` para la exposición principal de 5 minutos, `app.py` para demo/Q&A, `report/informe_final.pdf` como informe, y video MP4 solo como respaldo.

Prioridades:

1. Verificar que el modelo físico sea consistente: coordenadas `x1=L1 sin(theta1)`, `y1=-L1 cos(theta1)`, `x2=x1+L2 sin(theta2)`, `y2=y1-L2 cos(theta2)`; estado `[theta1, omega1, theta2, omega2]`; energía `E=T+V`; integración con `solve_ivp`; divergencia como evidencia numérica, no prueba formal de caos.
2. Mejorar la presentación HTML sin convertirla en un proyecto gigante. Mantener fondo oscuro, pocas palabras, animaciones suaves y una idea por escena.
3. Asegurar que el mapa de condiciones iniciales se explique como un conjunto de experimentos numéricos: cada pixel corresponde a una condición inicial y el color indica tiempo hasta el primer flip.
4. Revisar ortografía, acentos, notación y consistencia entre guion, presentación, informe y README.
5. Ejecutar `python scripts/smoke_test.py` y reportar resultados.

No uses material con copyright de videos de referencia. Toma inspiración estructural de 2swap/3Blue1Brown/Veritasium, pero todo el contenido visual debe ser generado por el repositorio.

Entregables esperados:

- Diff breve y seguro.
- Lista de archivos modificados.
- Comandos de verificación.
- Riesgos restantes.
