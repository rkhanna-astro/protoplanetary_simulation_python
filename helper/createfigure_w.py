import matplotlib.pyplot as plt
import numpy as np


def createfigure(X1, Y1):
    # Create figure
    figure1 = plt.figure()

    # Create axes
    axes1 = figure1.add_subplot(111)
    axes1.set_yscale('log')
    axes1.set_xscale('log')
    axes1.minorticks_on()

    # Uncomment the following line to preserve the X-limits of the axes
    # axes1.set_xlim([0.01, 1])
    # Uncomment the following line to preserve the Y-limits of the axes
    # axes1.set_ylim([1e-9, 0.0001])
    axes1.box(True)

    # Create loglog
    axes1.loglog(X1, Y1)

    # Create xlabel
    axes1.set_xlabel('protostellar mass')

    # Create ylabel
    axes1.set_ylabel('mass accretion rate')

    plt.show()

