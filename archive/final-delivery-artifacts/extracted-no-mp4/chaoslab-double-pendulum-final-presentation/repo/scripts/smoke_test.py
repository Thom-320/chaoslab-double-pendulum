from __future__ import annotations

from pathlib import Path
import shutil
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chaoslab.physics import DoublePendulumParams, simulate, energy, divergence, estimate_lyapunov_slope
from chaoslab.fractal import flip_time_map


def main() -> None:
    params = DoublePendulumParams()
    y0 = np.array([np.radians(120.0), 0.0, np.radians(-10.0), 0.0])
    t, y = simulate(y0, params, t_max=6.0, n=600)
    assert y.shape == (600, 4), y.shape

    _, _, E = energy(y, params)
    rel_drift = np.max(np.abs((E - E[0]) / max(abs(E[0]), 1e-12)))
    assert rel_drift < 1e-4, rel_drift

    y0b = y0.copy()
    y0b[2] += 1e-6
    _, yb = simulate(y0b, params, t_max=6.0, n=600)
    delta = divergence(y, yb)
    assert np.isfinite(delta).all()
    slope = estimate_lyapunov_slope(t, delta, fit_window=(1.0, 5.0))
    assert np.isfinite(slope), slope

    theta1, theta2, flip_times = flip_time_map(resolution=18, t_max=1.5, dt=0.05, params=params)
    assert theta1.shape == (18,)
    assert theta2.shape == (18,)
    assert flip_times.shape == (18, 18)
    assert np.isfinite(flip_times).all()

    required = [
        ROOT / "figures" / "trajectory_mass2.png",
        ROOT / "figures" / "energy_vs_time.png",
        ROOT / "figures" / "divergence_semilog.png",
        ROOT / "figures" / "flip_time_fractal_map.png",
        ROOT / "animations" / "double_pendulum.gif",
        ROOT / "presentation" / "index.html",
        ROOT / "presentation" / "script.js",
        ROOT / "presentation" / "style.css",
        ROOT / "presentation" / "data" / "chaos_data.js",
    ]
    missing = [str(p) for p in required if not p.exists()]
    assert not missing, "Missing generated assets: " + ", ".join(missing)

    deck = (ROOT / "presentation" / "index.html").read_text(encoding="utf-8")
    script = (ROOT / "presentation" / "script.js").read_text(encoding="utf-8")
    data_js = (ROOT / "presentation" / "data" / "chaos_data.js").read_text(encoding="utf-8")
    assert "Lyapunov formal" in deck, "Presentation must avoid overclaiming formal chaos proof"
    assert "Cada pixel" in deck, "Map slide must explain how the global map is produced"
    assert "renderMap" in script, "Presentation script must render the progressive map"
    assert '"map"' in data_js and '"flipTimes"' in data_js, "Presentation data must include a coarse map payload"

    print("ChaosLab smoke test passed")
    print(f"energy_relative_drift={rel_drift:.3e}")
    print(f"log_delta_slope={slope:.3g} 1/s")
    print(f"ffmpeg_available={shutil.which('ffmpeg') is not None}")


if __name__ == "__main__":
    main()
