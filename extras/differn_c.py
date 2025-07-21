import numpy as np
import matplotlib.pyplot as plt

# Very simple data set
np_points = 4  # number of points on a curve
func = lambda t: 4 * np.sin(t)  # function
dfunc = lambda t: 4 * np.cos(t)  # derivative of function
t = np.linspace(0, np.pi, np_points)
y = func(t)
plotrange = [0, 4, -5, 5]  # limits for plot with room for labels

plt.figure()
plt.grid(True)
plt.axis(plotrange)
plt.title('Numerical Differentiation Example')

# Plot actual curve
tt = np.linspace(0, np.pi, 100)
yy = func(tt)
plt.plot(tt, yy, 'k--', label='y(t)')

# Plot actual derivative
yy = dfunc(tt)
plt.plot(tt, yy, 'm--', label='dy/dt')

# Plot points and connecting lines
plt.plot(t, y, 'b-s', label='y(t) points')

# Display point numbers
for i in range(len(t)):
    plt.text(t[i], y[i] + 0.3, str(i + 1), horizontalalignment='center')

# Numerical difference
dydt = np.diff(y) / np.diff(t)

# Forward difference - plot numerical derivative at first point
tt = t[:-1]
plt.plot(tt, dydt, 'r-s', label='dy/dt (forward)')

# Backward difference - plot numerical derivative at second point
tt = t[1:]
plt.plot(tt, dydt, 'g-s', label='dy/dt (backward)')

# Central difference - plot numerical derivative at midpoint
tt = t[:-1] + np.diff(t) / 2
plt.plot(tt, dydt, 'k-s', label='dy/dt (central)')

# Finish
plt.legend()
plt.show()