import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from datetime import datetime

import numpy as np
from scipy.signal import iirnotch, lfilter

ard = serial.Serial('COM9', 115200)

file = open('log-'+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.txt', 'w')

data_buffer_size = 1000
raw_data_buffer = [0]*data_buffer_size
filtered_data_buffer = [0]*data_buffer_size 
std_buffer = [0]*data_buffer_size
end_buffer = [0]*data_buffer_size

period = 1 # ms
num_readings_calibrate = 400
b50, a50 = iirnotch(fs=1000/period, Q=10, w0=50)
b100, a100 = iirnotch(fs=1000/period, Q=10, w0=100)
b_filt, a_filt = np.convolve(b50, b100), np.convolve(a50, a100)
k = 0.2
data_time = 0


meanval = 0
target = 0
fig, ax = plt.subplots()
line_raw, = ax.plot([], [], lw=2, label="Raw")
line_filtered, = ax.plot([], [], lw=2, label="Filtered", color='orange')
line_std, = ax.plot([], [], lw=2, label="third", color='green')
ax.set_ylim(-10, 1030)
ax.set_xlim(0, data_buffer_size)
ax.set_title("Real-Time Serial Data Plot")
ax.set_xlabel("Reading idx")
ax.set_ylabel("Value")
ax.legend()

# Function to initialize the plot
def init():
    line_raw.set_data([], [])
    line_filtered.set_data([], [])
    line_std.set_data([], [])
    return line_raw, line_filtered, line_std


cur_on = 0 # "peak start" time
last_seen = 0 # "peak end" time
direction = 1
update = False
update_dir = False

def is_on(time, ping_to_off=200):
    return (time - last_seen) < ping_to_off
        
end_value = 0

# Function to update the plot
def update(frame):
    global filtered_data_buffer, raw_data_buffer, std_buffer, meanval, data_time, num_readings_calibrate, end_buffer, end_value
    try:
        # Read a line of data from the serial port
        while ard.in_waiting:
            data = ard.readline().decode('utf-8', errors='replace').strip()
        
            # Check if data is valid (non-empty and numeric)
            if data:
                try:
                    value = float(data)
                    file.write(f'{value}\n')
                    raw_data_buffer = raw_data_buffer[1:] + [value]
                    filtered_data_buffer = lfilter(b_filt, a_filt, raw_data_buffer)

                    if data_time < num_readings_calibrate * period:
                        meanval += filtered_data_buffer[-1]
                    elif data_time == num_readings_calibrate * period:
                        meanval /= num_readings_calibrate
                    else:
                        end_value = end_value*(1-k)+ abs(filtered_data_buffer[-1] - meanval)*k
                        end_buffer = end_buffer[1:] + [end_value]
                    data_time += period
                except ValueError:
                    pass
                
    except serial.SerialException as e:
        print(f"Serial read error: {e}")

    line_raw.set_data(range(len(raw_data_buffer)), raw_data_buffer)
    line_filtered.set_data(range(len(end_buffer)), end_buffer)
    
    return line_raw, line_filtered, line_std

ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=1)
plt.show()

ard.close()
