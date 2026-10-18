import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_bvp


def bb():
    x = np.array([1e-6, np.pi])
    y_init = np.zeros((3, x.size))
    sol = solve_bvp(deriv, bcs, x, y_init)

    plt.plot(sol.x, sol.y[0], 'b-x')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


def deriv(x, Y):
    alpha = 0.1  # viscosity parameter 1
    l = 1.0  # viscosity parameter 2
    gamma = 1.1  # adiabatic index

    dYdx = np.zeros_like(Y)
    dYdx[0] = (2.0 * (Y[0]) ** 2 / (alpha * x ** (l - 1.0)) +
               3.0 * (2.0 * l - 1) * Y[0] ** 2 +
               (6.0 * (l + 2.0) * gamma - 8.0 * (2.0 * l + 1.0)) * Y[0] * x +
               (4.0 * (2.0 * l + 3.0) - 4.0 * (l + 3.0) * gamma) * x ** 2.0) / (
                          2.0 * x * (3.0 * Y[0] - (3.0 * gamma - 2.0) * x))

    dYdx[1] = -Y[0]
    dYdx[2] = dYdx[0] * Y[0]

    return dYdx


def bcs(ya, yb):
    return np.array([ya[1] - 1, yb[0] + 1e-6, ya[2] - 0.3])

