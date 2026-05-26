# Reference analysis for ChaosLab

This file records the design and narrative takeaways from the requested references. Downloaded MP4 files and subtitles are kept locally under `research/reference_videos/`, which is intentionally ignored by git.

## Downloaded references

- `dtjb2OhEQcU`: **Double Pendulums are Chaoticn't**, 2swap, 538 s.
- `OIHyN7TzY6A`: **Order Within Chaos in the Double Pendulum (Island of Stability Simulation)**, Drew's Campfire, 574 s.

## 2swap structure to borrow

- Start with a misconception: "double pendulums are chaotic" becomes "not all of them are chaotic."
- Show individual specimens before the global map: chaotic case, coherent case, pretzel or stable island.
- Move from physical coordinates to angle space, then to a grid where each pixel is one experiment.
- Use the map as the final explanation, not as a decorative background.
- Keep the spoken idea simple while the visual field becomes dense.

## Observable / fractal map structure to borrow

- Use `theta1(0)` and `theta2(0)` as axes.
- Make color encode a measurable behavior, here time until first flip.
- Keep a legend visible: the map must remain a scientific plot, not just an abstract image.
- Explain that the map is exploratory if it uses a coarse fixed-step integrator.

## What to avoid

- Rebuilding SwapTube or a GPU renderer.
- Long derivations of the full equations of motion during the five-minute pitch.
- Using downloaded YouTube footage in the deliverable. The videos are for analysis only.
- Overclaiming a formal Lyapunov exponent. We report a slope of `log(Delta(t))` as evidence of sensitivity.

## Final ChaosLab adaptation

ChaosLab should be presented as a controlled, animated HTML deck:

1. Hook: two nearly identical pendulums diverge.
2. Baseline: pendulum simple, `omega = dtheta/dt`, small-angle approximation.
3. State: the second mass expands the state to `[theta1, omega1, theta2, omega2]`.
4. Simulation: the model is integrated, not hand animated.
5. Energy: total energy is the trust anchor.
6. Divergence: microscopic perturbation grows.
7. Map: each pixel is an experiment.
8. Close: deterministic does not mean predictable.
