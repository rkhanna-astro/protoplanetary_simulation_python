import numpy as np
import matplotlib.pyplot as plt

def subaxis(rows, cols, *args, **kwargs):
    # Default settings
    settings = {
        'SpacingVertical': 0.05,
        'SpacingHorizontal': 0.05,
        'PaddingLeft': 0,
        'PaddingRight': 0,
        'PaddingTop': 0,
        'PaddingBottom': 0,
        'MarginLeft': 0.1,
        'MarginRight': 0.1,
        'MarginTop': 0.1,
        'MarginBottom': 0.1,
        'Holdaxis': False
    }

    # Update settings with any provided keyword arguments
    settings.update(kwargs)

    # Determine the cell position
    if len(args) == 1:
        cell = args[0]
        if isinstance(cell, (list, tuple)) and len(cell) == 2:
            x1, y1 = cell
            x2, y2 = cell
        else:
            x1 = (cell - 1) % cols + 1
            x2 = x1
            y1 = (cell - 1) // cols + 1
            y2 = y1
    elif len(args) == 2:
        x1, y1 = args
        x2, y2 = x1, y1
    elif len(args) == 4:
        x1, y1, spanx, spany = args
        x2 = x1 + spanx - 1
        y2 = y1 + spany - 1
    else:
        raise ValueError('subaxis argument error')

    # Calculate the position of the subplot
    cellwidth = ((1 - settings['MarginLeft'] - settings['MarginRight']) - (cols - 1) * settings['SpacingHorizontal']) / cols
    cellheight = ((1 - settings['MarginTop'] - settings['MarginBottom']) - (rows - 1) * settings['SpacingVertical']) / rows
    xpos1 = settings['MarginLeft'] + settings['PaddingLeft'] + cellwidth * (x1 - 1) + settings['SpacingHorizontal'] * (x1 - 1)
    xpos2 = settings['MarginLeft'] - settings['PaddingRight'] + cellwidth * x2 + settings['SpacingHorizontal'] * (x2 - 1)
    ypos1 = settings['MarginTop'] + settings['PaddingTop'] + cellheight * (y1 - 1) + settings['SpacingVertical'] * (y1 - 1)
    ypos2 = settings['MarginTop'] - settings['PaddingBottom'] + cellheight * y2 + settings['SpacingVertical'] * (y2 - 1)

    # Create the subplot
    if settings['Holdaxis']:
        ax = plt.axes([xpos1, 1 - ypos2, xpos2 - xpos1, ypos2 - ypos1])
    else:
        ax = plt.subplot2grid((rows, cols), (y1 - 1, x1 - 1), rowspan=(y2 - y1 + 1), colspan=(x2 - x1 + 1))

    ax.set_box_aspect(1)
    ax.set_tag('subaxis')

    return ax

# Define the time array
t = np.arange(0, 2 * np.pi + 0.001, 0.001)

# Create the figure
fig = plt.figure(2)

# Loop to create subplots
for i in range(1, 7):
    ax = subaxis(3, 2, i, Spacing=0.0, Padding=0, Margin=0.1)
    if i % 2 == 0:
        ax.plot(t, np.sin(i * t))
    else:
        ax.plot(t, np.cos(i * t))
    ax.axis('tight')
    # ax.axis('off')

plt.show()
