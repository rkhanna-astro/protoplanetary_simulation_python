import matplotlib.pyplot as plt

def create_figure(X1, YMatrix1, X2, Y1):
    # Create figure
    fig, ax = plt.subplots()

    # Create multiple lines using matrix input to plot
    ax.plot(X1, YMatrix1[:, 0], color=[0, 1, 0], label=r'$\alpha_0=0.8$')
    ax.plot(X1, YMatrix1[:, 1], linestyle='--', color=[1, 0, 0], label=r'$\alpha_0=0.5$')
    ax.plot(X1, YMatrix1[:, 3], linestyle='--')
    ax.plot(X1, YMatrix1[:, 4], linestyle='--', color=[0, 1, 0])
    ax.plot(X1, YMatrix1[:, 5], color=[1, 0, 0])

    # Create xlabel
    ax.set_xlabel(r'$\rm time ~({\rm yr})$', fontsize=16)

    # Create ylabel
    ax.set_ylabel(r'$\rm J_{disk}/M_{disk}~({\rm m^2.s^{-1}})$', fontsize=16)

    # Create plot
    ax.plot(X2, Y1, color=[1, 0, 0])

    # Create legend
    legend = ax.legend(loc='northwest', frameon=False)
    legend.set_visible(False)

    plt.show()

# Example usage
import numpy as np
X1 = np.linspace(0, 10, 100)
YMatrix1 = np.random.rand(100, 6)
X2 = np.linspace(0, 10, 100)
Y1 = np.random.rand(100)

create_figure(X1, YMatrix1, X2, Y1)