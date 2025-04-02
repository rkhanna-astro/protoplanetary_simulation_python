import numpy as np
from scipy.integrate import solve_ivp
import funsys_c as funsys
import config as cfig

def funbvps(s0_new):
    print("This is the value",s0_new)
    
    x0 = cfig.xb[0]
    GBfactor = (4.0 * np.pi)**((cfig.gamma - 1.0) / cfig.gamma) * cfig.gamma**(-1.0 / cfig.gamma)
    GammaBig0 = GBfactor * s0_new**(2.0 * (1.0 - cfig.gamma) / cfig.gamma) * cfig.Lambda0 * x0**cfig.s
    w0 = s0_new * x0 * x0 * GammaBig0 / 2.0
    G0 = GBfactor * (s0_new**(2.0 * (1.0 - cfig.gamma) / cfig.gamma)) * cfig.Lambda0 * x0**cfig.s
    E0 = 0.5 * s0_new * x0 * x0 * ((cfig.Lambda0 * x0**cfig.s) / s0_new)**2

    # def funsys(x, y):
    #     # Placeholder function for funsys
    #     # You need to implement this based on your specific requirements
    #     return [v0, s0_new, w0, G0, E0]

    sol = solve_ivp(funsys.funsys, [cfig.xb[0], cfig.xb[-1]], [cfig.v0, s0_new, w0, G0, E0], t_eval=cfig.xb)
    x = sol.t
    y = sol.y

    Mdot_end = cfig.mdotfactor * x[-1] * y[1, -1] * y[0, -1] / (3 * cfig.gamma - 4)
    res = Mdot_end - cfig.Mdot_out  # dimensional
    # res = (x[-1] * y[1, -1] * y[0, -1] / (3 * gamma - 4)) - Mdot_out  # non-dimensional

    return res

# Example usage
# K = 1.0
# G = 1.0
# eta = 1.0
# gamma = 1.4
# Lambda0 = 1.0
# lm = 1.0
# s = 1.0
# dSigma_dx = 1.0
# ts = 1.0
# class_ = 1.0
# Mdot_out = 1.0
# mdotfactor = 1.0
# xb = np.linspace(0, 1, 10)
# v0 = 1.0
# w0 = 1.0
# G0 = 1.0
# E0 = 1.0

# s0_new = 1.0
# result = funbvps(s0_new)
# print(result)
