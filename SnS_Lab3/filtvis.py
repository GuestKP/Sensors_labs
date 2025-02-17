import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from datetime import datetime

import numpy as np
from scipy.signal import iirnotch, lfilter, butter
from scipy.fft import rfft

ard = serial.Serial('/dev/ttyACM1', 115200)

file = open('log-'+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.txt', 'w')

# Data buffer for real-time plotting
data_buffer_size = 1000  # Number of data points to display
raw_data_buffer = deque(maxlen=data_buffer_size)
filtered_data_buffer = [0]*data_buffer_size#deque(maxlen=data_buffer_size)

b_notch, a_notch = iirnotch(fs=1000, Q=10, w0=50)
b_notch2, a_notch2 = iirnotch(fs=1000, Q=10, w0=63)

# Create the figure and axis for plotting
fig, ax = plt.subplots()
line_raw, = ax.plot([], [], lw=2, label="Raw Data")
line_filtered, = ax.plot([], [], lw=2, label="Filtered Data", color='orange')
ax.set_ylim(-10, 1030)  # Adjust based on your expected data range
ax.set_xlim(0, data_buffer_size)
ax.set_title("Real-Time Serial Data Plot with Notch Filter")
ax.set_xlabel("Time")
ax.set_ylabel("Value")
ax.legend()

# Function to initialize the plot
def init():
    line_raw.set_data([], [])
    line_filtered.set_data([], [])
    return line_raw, line_filtered

# Function to update the plot
def update(frame):
    global filtered_data_buffer
    try:
        # Read a line of data from the serial port
        while ard.in_waiting:
            data = ard.readline().decode('utf-8', errors='replace').strip()
        
        # Check if data is valid (non-empty and numeric)
            if data:
                try:
                    value = float(data)
                    file.write(f'{value}\n')
                    raw_data_buffer.append(value)
                    filtered_data_buffer = filtered_data_buffer[1:] + [(sum(filtered_data_buffer[-4:]) + value) / 5]


                    '''filtered_data_buffer = lfilter(b_notch, a_notch, raw_data_buffer)
                    filtered_data_buffer = lfilter(b_notch2, a_notch2, filtered_data_buffer)
                    filtered_data_buffer = np.abs(rfft(filtered_data_buffer)) / 100'''
                except ValueError:
                    pass
                
    except serial.SerialException as e:
        print(f"Serial read error: {e}")
    line_raw.set_data(range(len(raw_data_buffer)), raw_data_buffer)
    line_filtered.set_data(range(len(filtered_data_buffer)), filtered_data_buffer)
    
    return line_raw, line_filtered

ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=1)
plt.show()

ard.close()
