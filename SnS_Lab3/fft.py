from scipy.fft import rfft
import matplotlib.pyplot as plt
from os import listdir
import numpy as np

folder = './SnS_Lab3/'
entries = sorted(listdir(folder))
print(*[f'[{i}] {name}' for i, name in enumerate(entries)], sep='\n')
idx = int(input("Select file: "))
with open(folder+entries[idx], 'r') as f:
    data = [float(i) for i in f.readlines()]


plt.plot(range(len(data)), data)
plt.show()

dfft = np.abs(rfft(data[-1000:]))
plt.plot(range(len(dfft)), dfft)
plt.xlabel('Frequency, Hz')
plt.ylabel('Magnitude, units^2')
plt.show()