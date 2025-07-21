import matplotlib.pyplot as plt
import numpy as np

def label_line(ax, label_strings):
    lines = ax.get_lines()
    n = len(lines)
    for k in range(n):
        x_data = lines[k].get_xdata()
        y_data = lines[k].get_ydata()
        ind = round(len(x_data) / 2)
        ax.text(x_data[ind], y_data[ind], label_strings[n - k - 1])

# Example usage
fig, ax = plt.subplots()
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
ax.plot(x, y1)
ax.plot(x, y2)
label_strings = ['sin(x)', 'cos(x)']
label_line(ax, label_strings)
plt.show()