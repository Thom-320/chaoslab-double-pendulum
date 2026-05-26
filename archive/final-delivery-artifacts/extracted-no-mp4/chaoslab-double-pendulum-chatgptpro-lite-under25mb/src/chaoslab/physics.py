from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from scipy.integrate import solve_ivp

Array = np.ndarray


@dataclass(frozen=True)
class DoublePendulumParams:
    """Physical parameters for a point-mass double pendulum.

    Angles are measured from the vertical downward direction.
    The generalized coordinates are (theta1, omega1, theta2, omega2).
    """

    m1: float = 1.0
    m2: float = 1.0
    L1: float = 1.0
    L2: float = 1.0
    g: float = 9.81


def rhs(t: float, y: Array, p: DoublePendulumParams) -> Array:
    """Right-hand side of the double-pendulum ODE.

    This is the standard point-mass double pendulum model. It is sufficient for
    the project because the objective is not an industrial-grade pendulum, but a
    reproducible demonstration of nonlinear mechanics and sensitivity to initial
    conditions. Humanity survives another approximation.
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

    return np.array([w1, dw1, w2, dw2], dtype=float)


def simulate(
    y0: Array,
    params: DoublePendulumParams = DoublePendulumParams(),
    t_max: float = 20.0,
    n: int = 2000,
    rtol: float = 1e-9,
    atol: float = 1e-11,
) -> tuple[Array, Array]:
    """Integrate the double-pendulum ODE and return (t, y).

    y has shape (n, 4) with columns [theta1, omega1, theta2, omega2].
    """
    y0 = np.asarray(y0, dtype=float)
    t_eval = np.linspace(0.0, float(t_max), int(n))
    sol = solve_ivp(
        lambda t, y: rhs(t, y, params),
        (0.0, float(t_max)),
        y0,
        t_eval=t_eval,
        method="DOP853",
        rtol=rtol,
        atol=atol,
    )
    if not sol.success:
        raise RuntimeError(f"Integration failed: {sol.message}")
    return sol.t, sol.y.T


def positions(y: Array, params: DoublePendulumParams = DoublePendulumParams()) -> tuple[Array, Array, Array, Array]:
    """Return positions (x1, y1, x2, y2) from state array."""
    Y = np.asarray(y)
    th1 = Y[..., 0]
    th2 = Y[..., 2]
    x1 = params.L1 * np.sin(th1)
    y1 = -params.L1 * np.cos(th1)
    x2 = x1 + params.L2 * np.sin(th2)
    y2 = y1 - params.L2 * np.cos(th2)
    return x1, y1, x2, y2


def energy(y: Array, params: DoublePendulumParams = DoublePendulumParams()) -> tuple[Array, Array, Array]:
    """Return kinetic, potential, and total mechanical energy."""
    Y = np.asarray(y)
    th1, w1, th2, w2 = Y[..., 0], Y[..., 1], Y[..., 2], Y[..., 3]
    m1, m2, L1, L2, g = params.m1, params.m2, params.L1, params.L2, params.g

    vx1 = L1 * w1 * np.cos(th1)
    vy1 = L1 * w1 * np.sin(th1)
    vx2 = vx1 + L2 * w2 * np.cos(th2)
    vy2 = vy1 + L2 * w2 * np.sin(th2)

    T = 0.5 * m1 * (vx1 * vx1 + vy1 * vy1) + 0.5 * m2 * (vx2 * vx2 + vy2 * vy2)
    y_mass1 = -L1 * np.cos(th1)
    y_mass2 = y_mass1 - L2 * np.cos(th2)
    V = m1 * g * y_mass1 + m2 * g * y_mass2
    return T, V, T + V


def divergence(y_a: Array, y_b: Array) -> Array:
    """Phase-space distance between two double-pendulum trajectories.

    Angle differences are wrapped to [-pi, pi] so the metric does not jump
    artificially when an angle crosses a branch cut.
    """
    A = np.asarray(y_a)
    B = np.asarray(y_b)
    dtheta1 = np.arctan2(np.sin(A[:, 0] - B[:, 0]), np.cos(A[:, 0] - B[:, 0]))
    dtheta2 = np.arctan2(np.sin(A[:, 2] - B[:, 2]), np.cos(A[:, 2] - B[:, 2]))
    dw1 = A[:, 1] - B[:, 1]
    dw2 = A[:, 3] - B[:, 3]
    return np.sqrt(dtheta1 * dtheta1 + dtheta2 * dtheta2 + dw1 * dw1 + dw2 * dw2)


def estimate_lyapunov_slope(t: Array, delta: Array, fit_window: tuple[float, float] = (1.0, 6.0)) -> float:
    """Crude estimate of the early-time slope of log(delta(t)).

    It is not a formal Lyapunov exponent. It is a presentation-safe quantitative
    indicator of sensitivity, which is a polite way of not overclaiming.
    """
    t = np.asarray(t)
    delta = np.asarray(delta)
    mask = (t >= fit_window[0]) & (t <= fit_window[1]) & np.isfinite(delta) & (delta > 0)
    if mask.sum() < 5:
        return float("nan")
    coeff = np.polyfit(t[mask], np.log(delta[mask]), 1)
    return float(coeff[0])
