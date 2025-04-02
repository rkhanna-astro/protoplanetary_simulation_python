import numpy as np
import config as cfig

def funsys(x, y):
    K = cfig.K
    G = cfig.G 
    eta = cfig.eta 
    gamma = cfig.gamma 
    Lambda0 = cfig.Lambda0 
    lm = cfig.lm 
    s = cfig.s
    dSigma_dx = cfig.dSigma_dx
    ts = cfig.ts
    class_ = cfig.class_type

    mfactor = (K**1.5) * (G**((1 - 3 * gamma) / 2.0)) * (ts**(4 - 3 * gamma)) / 1.989e+30  # solar unit
    GBfactor = (4.0 * np.pi)**((gamma - 1.0) / gamma) * gamma**(-1.0 / gamma)
    # print("Lets check GBfactor", x, y)
    GammaBig = GBfactor * y[1]**(2.0 * (1.0 - gamma) / gamma) * Lambda0 * x**s
    dGammaBig_dx = GBfactor * ((2.0 * (1.0 - gamma) / gamma) * dSigma_dx * y[1]**((2.0 - 3.0 * gamma) / gamma) * Lambda0 * x**s + y[1]**(2.0 * (1.0 - gamma) / gamma) * s * Lambda0 * x**(s - 1))

    if class_ == 'disk':
        A = ((y[0] - (2 - gamma) * x)**4) * (y[0] + (2 * lm**2 - 1) * x * GammaBig) / x**2
        B = x * dGammaBig_dx - 3 * GammaBig + 12 * gamma - 18
        C = (gamma - 2) * x * dGammaBig_dx - 2 * (GammaBig**2) + (5 * gamma - 2) * GammaBig - 10 * gamma + 12
        J = ((y[1] * y[0] / (3 * gamma - 4))**0.5) * x
    else:
        Mstar_solar = 1.0
        J = (x * Mstar_solar / mfactor)**0.5

    nu = eta * (y[1]**2) * (x**2) / (J**3)

    dydx = np.zeros(5)
    if class_ == 'disk':
        dydx[0] = ((A / nu) + B * y[0] + C * x + 6 * (y[0]**2) / x) / (9 * y[0] - (3 * gamma + 2) * x - 4 * x * GammaBig)
    else:
        dydx[0] = (((y[0] - (2 - gamma) * x)**3) * (y[0] + (2 * lm**2 - 1) * x * GammaBig) / (9 * (x**2) * nu)) + (2 * y[0] / (3 * x)) - GammaBig - (2 - gamma) * x + 4 * gamma - 6

    dydx[1] = -(y[1] / x) - y[1] * (dydx[0] - (2.0 - gamma)) / (y[0] - (2.0 - gamma) * x) + y[1] * (3.0 * gamma - GammaBig - 4.0) / (y[0] - (2.0 - gamma) * x)
    dSigma_dx = dydx[1]

    dydx[2] = y[1] * x * GammaBig
    dydx[3] = GBfactor * ((2.0 * (1.0 - gamma) / gamma) * dSigma_dx * y[1]**((2.0 - 3.0 * gamma) / gamma) * Lambda0 * x**s + y[1]**(2.0 * (1.0 - gamma) / gamma) * s * Lambda0 * x**(s - 1))
    dydx[4] = y[1] * x * ((Lambda0 * (x**s)) / y[1])**2

    return dydx

# # Example usage
# K = 1.0
# G = 1.0
# eta = 1.0
# gamma = 1.4
# Lambda0 = 1.0
# lm = 1.0
# s = 1.0
# dSigma_dx = 1.0
# ts = 1.0
# class_ = 'disk'

# x = 1.0
# y = [1.0, 1.0, 1.0, 1.0, 1.0]

# result = funsys(x, y)
# print(result)