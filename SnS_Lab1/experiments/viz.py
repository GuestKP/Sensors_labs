import matplotlib.pyplot as plt
import numpy as np

data = np.genfromtxt('data.csv', delimiter=',')
print(data.shape)
time = np.arange(data.shape[0]) * 0.001

plt.plot(time, data.T[0], label='A wire')
plt.plot(time, data.T[1], label='B wire')
plt.plot(time, data.T[2], label='Angle, [rad]')
plt.xlabel('Time, [s]')
plt.legend()
plt.show()