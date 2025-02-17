from scipy.fft import rfft
import matplotlib.pyplot as plt
from os import listdir
import numpy as np

print(sorted(listdir('./'))[-1])
with open(sorted(listdir('./'))[-1], 'r') as f:
    data = [float(i) for i in f.readlines()]

dfft = np.abs(rfft(data[-1000:]))
plt.plot(range(len(dfft)), dfft)
plt.show()