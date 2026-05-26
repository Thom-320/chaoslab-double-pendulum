from __future__ import annotations

from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chaoslab.physics import DoublePendulumParams, simulate, divergence, estimate_lyapunov_slope
from chaoslab.fractal import flip_time_map
from chaoslab.visuals import save_trajectory, save_energy, save_divergence, save_fractal_map, animate_double_pendulum


def main():
    params = DoublePendulumParams(m1=1.0, m2=1.0, L1=1.0, L2=1.0, g=9.81)
    figures = ROOT / "figures"
    animations = ROOT / "animations"
    data = ROOT / "data"
    figures.mkdir(exist_ok=True)
    animations.mkdir(exist_ok=True)
    data.mkdir(exist_ok=True)

    y0 = np.radians([120.0, 0.0, -10.0, 0.0])
    # The state is [theta1, omega1, theta2, omega2], so overwrite angular velocities.
    y0 = np.array([np.radians(120.0), 0.0, np.radians(-10.0), 0.0])
    t, y = simulate(y0, params, t_max=24.0, n=2600)
    save_trajectory(t, y, figures / "trajectory_mass2.png", params)
    save_energy(t, y, figures / "energy_vs_time.png", params)
    animate_double_pendulum(t, y, animations / "double_pendulum.gif", params, fps=30, seconds=8.0)

    eps = 1e-6
    y0b = y0.copy()
    y0b[2] += eps
    tb, yb = simulate(y0b, params, t_max=24.0, n=2600)
    d = divergence(y, yb)
    save_divergence(t, d, figures / "divergence_semilog.png")
    slope = estimate_lyapunov_slope(t, d, fit_window=(1.0, 7.0))

    theta1, theta2, flip_times = flip_time_map(resolution=120, t_max=18.0, dt=0.035, params=params)
    save_fractal_map(theta1, theta2, flip_times, figures / "flip_time_fractal_map.png", t_max=18.0)
    np.savez_compressed(data / "flip_time_map_120.npz", theta1=theta1, theta2=theta2, flip_times=flip_times)

    (data / "summary_metrics.txt").write_text(
        "ChaosLab summary metrics\n"
        f"initial_state_rad = {y0.tolist()}\n"
        f"epsilon_theta2 = {eps}\n"
        f"estimated_log_divergence_slope_1_to_7_s = {slope:.6g} 1/s\n"
        f"max_relative_energy_drift = {np.max(np.abs((__import__('chaoslab.physics').physics.energy(y, params)[2] - __import__('chaoslab.physics').physics.energy(y, params)[2][0]) / abs(__import__('chaoslab.physics').physics.energy(y, params)[2][0]))):.6g}\n",
        encoding="utf-8",
    )
    print("Assets generated in", ROOT)


if __name__ == "__main__":
    main()
