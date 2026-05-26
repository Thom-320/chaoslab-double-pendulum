from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chaoslab.physics import DoublePendulumParams, simulate, positions, energy, divergence, estimate_lyapunov_slope


def _round_list(values, decimals=5):
    return np.round(np.asarray(values, dtype=float), decimals).tolist()


def main() -> None:
    out_dir = ROOT / "presentation" / "data"
    out_dir.mkdir(parents=True, exist_ok=True)

    params = DoublePendulumParams()
    y0 = np.array([np.radians(120.0), 0.0, np.radians(-10.0), 0.0])
    y0b = y0.copy()
    y0b[2] += 1e-6
    t, y = simulate(y0, params, t_max=24.0, n=720)
    _, yb = simulate(y0b, params, t_max=24.0, n=720)
    x1, y1, x2, y2 = positions(y, params)
    xb1, yb1, xb2, yb2 = positions(yb, params)
    T, V, E = energy(y, params)
    delta = divergence(y, yb)

    reg_t = np.linspace(0.0, 12.0, 360)
    theta = 0.52 * np.cos(np.sqrt(params.g / params.L1) * reg_t)
    simple = {
        "t": _round_list(reg_t, 4),
        "x": _round_list(np.sin(theta), 5),
        "y": _round_list(-np.cos(theta), 5),
        "theta": _round_list(theta, 5),
    }

    data = {
        "meta": {
            "epsilon": 1e-6,
            "slope": estimate_lyapunov_slope(t, delta, (1.0, 7.0)),
            "energyDrift": float(np.max(np.abs((E - E[0]) / max(abs(E[0]), 1e-12)))),
        },
        "double": {
            "t": _round_list(t, 4),
            "x1": _round_list(x1),
            "y1": _round_list(y1),
            "x2": _round_list(x2),
            "y2": _round_list(y2),
            "xb1": _round_list(xb1),
            "yb1": _round_list(yb1),
            "xb2": _round_list(xb2),
            "yb2": _round_list(yb2),
        },
        "energy": {
            "t": _round_list(t, 4),
            "kinetic": _round_list(T, 5),
            "potential": _round_list(V, 5),
            "total": _round_list(E, 5),
        },
        "divergence": {
            "t": _round_list(t, 4),
            "delta": _round_list(delta, 10),
        },
        "simple": simple,
    }

    js = "window.CHAOS_DATA = " + json.dumps(data, separators=(",", ":")) + ";\n"
    (out_dir / "chaos_data.js").write_text(js, encoding="utf-8")
    print(out_dir / "chaos_data.js")


if __name__ == "__main__":
    main()
