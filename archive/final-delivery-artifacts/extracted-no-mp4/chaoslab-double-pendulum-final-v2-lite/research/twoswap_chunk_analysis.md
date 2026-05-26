# 2swap Chunk Analysis For ChaosLab

Source downloaded locally: `research/reference_videos/dtjb2OhEQcU/Double Pendulums are Chaoticn't.mp4`.

This analysis is based on the local subtitles and the downloaded reference video. The reference is used for structure and visual strategy only; the deliverables do not embed copyrighted YouTube footage.

## Chunk Map

| Time | What 2swap does | ChaosLab adaptation |
|---:|---|---|
| 0:00-0:45 | Opens by challenging the familiar claim: double pendulums are chaotic, but not all of them diverge. Shows two nearly identical pendulums and then a coherent pretzel-like case. | Start with two nearly identical ChaosLab simulations. The hook line is: same laws, different futures. Mention that some regions remain coherent, so the story is not just randomness. |
| 0:45-1:35 | Defines the useful coordinates: top angle and bottom angle measured from the vertical. Moves from physical pendulum motion to angle-space plots. | Show dashed vertical references and arcs for `theta1` and `theta2` directly on the pendulum. Then introduce the state vector `[theta1, omega1, theta2, omega2]`. |
| 1:35-2:35 | Compares individual specimens: chaotic, Lissajous-like, pretzel. The visual point is that one system can produce very different families of motion. | Keep the five-minute pitch focused on one chaotic case, but preserve the language of regimes: regular, chaotic, stable island, high energy. Use Streamlit presets for live exploration. |
| 2:35-3:35 | Builds a grid of pendulums. Grid position corresponds to initial angles; color makes coherent and chaotic regions visible. | Use the final map as the main visual payoff. Each pixel is one numerical experiment; color is time until first flip. |
| 3:35-4:40 | Increases resolution to one pendulum per pixel and emphasizes periodicity in angle space. | Explain the axes as `theta1(0)` and `theta2(0)` over `[-pi, pi]`. Avoid overclaiming exact fractal dimension because our RK4 map is exploratory. |
| 4:40-5:55 | Tracks pairs of nearby pendulums and visualizes their divergence. | Show `Delta(t)` in semilog scale after proving the energy stays controlled. |
| 5:55-7:05 | Zooms into islands of stability and named coherent paths like pretzel, shoelace, heart. | Use this as optional verbal color, not core evidence. Mention stable islands on the map, but keep the required Physics I thread: energy and sensitivity. |
| 7:05-8:58 | Complicates the naive energy story: low energy is often stable, but high energy is not a complete explanation. Ends by being careful about definitions of chaos. | In ChaosLab, state clearly: we show evidence of sensitivity, not a formal Lyapunov proof. This protects the project academically. |

## Presentation Rules Borrowed

- Define angle conventions visually before using equations.
- Show an individual pendulum before showing the global map.
- Make the map a result, not a background.
- Use one clear measurement per scene: energy drift, phase-space distance, or flip time.
- Keep the spoken story cautious: deterministic, nonlinear, sensitive; not a formal proof of chaos.

## Corrections Applied To ChaosLab

- The canvas now maps physical `y` upward correctly, so the pendulum is not vertically inverted.
- `theta1` and `theta2` are drawn as arcs from the downward vertical reference.
- The presentation text now uses the actual symbols `theta`, `omega`, `Delta`, and the correct small-angle and energy statements.
- The video renderer is being upgraded from the original 8 fps draft to a 60 fps deliverable.

## Next Visual Beat Added

The missing bridge was the step from angles to Cartesian coordinates. ChaosLab now includes a modeling scene that constructs the double pendulum geometry in the same order as the model:

```tex
x_1 = L_1\sin\theta_1
y_1 = -L_1\cos\theta_1
x_2 = x_1 + L_2\sin\theta_2
y_2 = y_1 - L_2\cos\theta_2
```

The scene uses dashed vertical references, horizontal and vertical component guides, angle labels, and a final vector toward `(x_2,y_2)`. This follows the useful 2swap pattern: define one specimen clearly before moving to state space, divergence, and the global map.

## Peer Review Notes

Local subagent review and Hermes text review converged on the same priority: the deck needed less decorative animation and more visible model-building. Two extra changes were therefore folded into existing scenes instead of adding time:

- The simulation scene now shows the coupled ODE structure, `theta_ddot_1=f(theta_1,theta_2,omega_1,omega_2)` and `theta_ddot_2=g(...)`, so `solve_ivp` is motivated by dynamics rather than presented as a black box.
- The divergence scene now shows the two initially close pendulums beside the semilog `Delta(t)` chart, with a moving time cursor on the graph.

## Iteración final aplicada

Se añadió una escena explícita de **espacio de ángulos** entre la simulación numérica y el control de energía. Esta escena corrige el salto narrativo más importante: el público primero ve un experimento individual como curva `θ₁(t)` contra `θ₂(t)`, y solo después ve el mapa donde cada pixel corresponde a una condición inicial diferente.

También se agregó una escena opcional de Manim (`manim/chaos_geometry_scene.py`) y un clip renderizable sin Manim (`scripts/render_manim_style_geometry.py`) para reforzar el estilo 3Blue1Brown sin hacer que la entrega dependa de instalar Manim.
