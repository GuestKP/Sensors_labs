from scipy.fft import rfft
import matplotlib.pyplot as plt
from os import listdir
import numpy as np

print(sorted(listdir('./SnS_Lab3/'))[-1])
with open('SnS_Lab3\log-2025-02-24-17-58-39_noise.txt', 'r') as f:
    data = [float(i) for i in f.readlines()]

dfft = np.abs(rfft(data[-1000:]))
plt.plot(range(len(dfft)), dfft)
plt.show()