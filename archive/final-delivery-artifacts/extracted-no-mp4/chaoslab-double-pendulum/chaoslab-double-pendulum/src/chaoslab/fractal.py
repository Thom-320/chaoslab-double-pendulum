from __future__ import annotations

import numpy as np
from .physics import DoublePendulumParams

Array = np.ndarray


def _rhs_vec(y: Array, p: DoublePendulumParams) -> Array:
    """Vectorized RHS for many initial conditions at once.

    y shape: (4, N, N). Returns same shape.
    """
    th1, w1, th2, w2 = y
    m1, m2, L1, L2, g = p.m1, p.m2, p.L1, p.L2, p.g
    delta = th2 - th1
    s = np.sin(delta)
    c = np.cos(delta)
    den1 = L1 * (m1 + m2 - m2 * c * c)
    den2 = L2 * (m1 + m2 - m2 * c * c)
    dw1 = (
        m2 * L1 * w1 * w1 * s * c
        + m2 * g * np.sin(th2) * c
        + m2 * L2 * w2 * w2 * s
        - (m1 + m2) * g * np.sin(th1)
    ) / den1
    dw2 = (
        -m2 * L2 * w2 * w2 * s * c
        + (m1 + m2) * (g * np.sin(th1) * c - L1 * w1 * w1 * s - g * np.sin(th2))
    ) / den2
    return np.stack([w1, dw1, w2, dw2], axis=0)


def _rk4_step(y: Array, dt: float, p: DoublePendulumParams) -> Array:
    k1 = _rhs_vec(y, p)
    k2 = _rhs_vec(y + 0.5 * dt * k1, p)
    k3 = _rhs_vec(y + 0.5 * dt * k2, p)
    k4 = _rhs_vec(y + dt * k3, p)
    return y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def flip_time_map(
    resolution: int = 140,
    t_max: float = 24.0,
    dt: float = 0.03,
    params: DoublePendulumParams = DoublePendulumParams(),
) -> tuple[Array, Array, Array]:
    """Compute a 2D map of first flip time over initial angles.

    Initial conditions: theta1, theta2 in [-pi, pi], omega1=omega2=0.
    A flip is detected when either unwrapped angle reaches |theta| >= pi.

    Returns theta1_grid, theta2_grid, flip_times. Values equal to t_max mean no
    flip was detected before t_max. This deliberately uses a coarse vectorized
    integrator to produce a fast, presentation-friendly image.
    """
    n = int(resolution)
    theta1 = np.linspace(-np.pi, np.pi, n)
    theta2 = np.linspace(-np.pi, np.pi, n)
    TH1, TH2 = np.meshgrid(theta1, theta2, indexing="xy")
    y = np.stack([TH1.copy(), np.zeros_like(TH1), TH2.copy(), np.zeros_like(TH1)], axis=0)
    flip_times = np.full_like(TH1, fill_value=float(t_max), dtype=float)
    alive = np.ones_like(TH1, dtype=bool)

    steps = int(np.ceil(t_max / dt))
    for step in range(1, steps + 1):
        y = _rk4_step(y, dt, params)
        just_flipped = alive & ((np.abs(y[0]) >= np.pi) | (np.abs(y[2]) >= np.pi))
        flip_times[just_flipped] = step * dt
        alive &= ~just_flipped
        # Stop early only if everything has flipped. It often will not.
        if not alive.any():
            break
    return theta1, theta2, flip_times
