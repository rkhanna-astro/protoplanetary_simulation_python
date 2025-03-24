import numpy as np


def bcs(ya, yb):
    global K, G, ts, eta, gamma, Lambda0, lm, s, dSigma_dx,

    class , Mb0, mdotfactor, x0, xf

    Mdot_acc = mdotfactor * xf * yb[1] * yb[0] / (3 * gamma - 4)  # solar mass per year
    Va = -1.e-4  # (- ( (4.*l+6.)-(2.*l+6.)*gamma ) / (3.-2.*l) ) * ( Xa - (9.*(4.-3.*gamma)*Xa^3.) / (2.*l-3.)*(6.*l^2-2.*l-15.)*eta*Xa^l )

    res = [
        ya[0] - Va,
        Mdot_acc - Mb0,
        0,
        0
    ]  # yb[1] - 5.0, yb[2]

    return res

