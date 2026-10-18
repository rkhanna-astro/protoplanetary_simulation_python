import matplotlib.pyplot as plt
import numpy as np

def SFdataXpt(ax=None):
    if ax is None:
        ax = plt.gca()

    figs = plt.get_fignums()
    if not figs:
        print('>>> Warning, axis size and limits are undefined')
    else:
        xlim_mode = ax.get_xlim()
        ylim_mode = ax.get_ylim()
        if ax.get_autoscalex_on() or ax.get_autoscaley_on():
            print('>>> Warning, axis limits not explicitly set')

    # Get the axis size in points
    units = ax.get_units()
    ax.set_units('points')
    pos_pt = ax.get_position().bounds
    ax.set_units(units)  # Restore the axes units

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    xscale = ax.get_xscale()
    if xscale == 'log':
        xlim = np.log10(xlim)
    yscale = ax.get_yscale()
    if yscale == 'log':
        ylim = np.log10(ylim)

    sf = [np.diff(xlim)[0] / pos_pt[2], np.diff(ylim)[0] / pos_pt[3]]

    return sf, xscale, yscale

# Example usage
fig, ax = plt.subplots()
ax.set_xlim([1, 100])
ax.set_ylim([1, 100])
ax.set_xscale('log')
ax.set_yscale('log')
sf, xscale, yscale = SFdataXpt(ax)
print(f'SF: {sf}, XScale: {xscale}, YScale: {yscale}')
