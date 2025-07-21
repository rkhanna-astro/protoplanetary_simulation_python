import numpy as np
import matplotlib.pyplot as plt

def createdata(Yv, x):
    global eta, gamma, Lambda0, lm, s

    # wind quantities
    GBfactor = (4.0 * np.pi) ** ((gamma - 1.0) / gamma) * gamma ** (-1.0 / gamma)
    GammaBig = GBfactor * Yv[:, 1] ** (2.0 * (1.0 - gamma) / gamma) * Lambda0 * x ** s

    # radial velocity: |v_r|/cs
    factor1 = ((4.0 * np.pi * gamma) ** ((gamma - 1.0) / (2.0 * gamma)) * Yv[:, 1] ** ((1.0 - gamma) / gamma)) / gamma ** 0.5
    vr_cs = np.abs(factor1 * Yv[:, 0])

    # sigma, sigma_0 = no-wind density
    sigma = 0.15 * Yv[:, 1]

    # angular momentum
    J = x * (Yv[:, 1] * (Yv[:, 0] - (2 - gamma) * x) / (3 * gamma - 4)) ** 0.5

    # Toomre parameter: Q
    dlnJ_dlnx = 0.5 + (3 * gamma - GammaBig - 4.0) * x / (2 * (Yv[:, 0] - (2.0 - gamma) * x))
    factor3 = ((4.0 * np.pi) ** (0.5 * (1.0 - gamma) / gamma)) * (gamma ** (0.5 / gamma)) * (Yv[:, 1] ** (-1.0 / gamma))
    Qtoomre = factor3 * 2 * J * (2 * dlnJ_dlnx) ** 0.5 / (x ** 2)

    # V_z+
    V_z = (Lambda0 * x ** s) / Yv[:, 1]

    # Disk aspect ratio: H/r
    H_r = (4 * np.pi) ** ((1.0 - gamma) / gamma) * (gamma ** (1.0 / gamma)) * (Yv[:, 1] ** ((gamma - 2.0) / gamma)) * (1.0 / x)

    # Pressure to volume density: P/rho
    # Temperature: T/T_nw = (P/rho) / (P_nw/rho_nw)
    P_rho = Yv[:, 1] ** ((2.0 * gamma - 2.0) / gamma)

    # Mass accretion rate: (cs^3/G)*Mdot_acc ==[CONVERTED]==> in terms of 10^-6 mass of SUN
    Mdot_acc = x * Yv[:, 1] * Yv[:, 0] / (3 * gamma - 4.0)
    factor2 = ((4.0 * np.pi) ** (gamma - 1.0) * (1.0 / gamma) * Yv[:, 1] ** (2.0 - 2.0 * gamma)) ** (3.0 / (2.0 * gamma))
    Mdot_acc = factor2 * Mdot_acc * 3.e-9

    # angular velocity: v_phi/cs, V_phi=J/x
    v_phi_cs = factor1 * J / x

    # wind vertical velocity: v_z+/cs
    v_z_cs = factor1 * V_z

    # Specific angular momentum: q
    J_M = np.sqrt(np.abs((3.0 * gamma - 4.0) / (Yv[:, 1] * (Yv[:, 0] - (2.0 - gamma) * x))))
    factor4 = ((4.0 * np.pi) ** (0.5 * (1.0 - gamma) / gamma)) * (gamma ** (0.5 / gamma)) * (Yv[:, 1] ** (gamma - 1.0 / gamma))

    # Plotting
    plt.subplot(2, 3, 1)
    plt.semilogx(x, np.abs(Yv[:, 0]))
    plt.grid()
    plt.xlabel('radius (AU)')
    plt.ylabel('radial velocity')

    plt.subplot(2, 3, 2)
    plt.semilogx(x, sigma)
    plt.grid()
    plt.xlabel('radius (AU)')
    plt.ylabel('surface density')

    plt.subplot(2, 3, 3)
    plt.semilogx(x, v_phi_cs)
    plt.grid()
    plt.xlabel('radius (AU)')
    plt.ylabel('angular velocity')

    plt.subplot(2, 3, 4)
    plt.semilogx(x, Qtoomre)
    plt.grid()
    plt.xlabel('radius (AU)')
    plt.ylabel('Toomre parameter')

    plt.subplot(2, 3, 5)
    plt.semilogx(x, H_r)
    plt.grid()
    plt.xlabel('radius (AU)')
    plt.ylabel('H/r')

    plt.subplot(2, 3, 6)
    plt.semilogx(x, Mdot_acc)
    plt.grid()
    plt.xlabel('radius (AU)')
    plt.ylabel('mass accretion rate')

    plt.show()

