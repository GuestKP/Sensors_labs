import serial
from datetime import datetime

import numpy as np
from scipy.signal import iirnotch, lfilter

ard = serial.Serial('COM9', 115200)

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
data_time_mot_upd = 0


meanval = 0
target = 0

cur_on = 0 # "peak start" time
last_seen = 0 # "peak end" time
direction = 1
update = False
update_dir = False

def is_on(time, ping_to_off=200):
    return (time - last_seen) < ping_to_off

def control(val, time, thresh = 50, long_delta = 300):
    global cur_on, last_seen, direction, update, update_dir, target
    
    # if we have peak
    if val > thresh:
        update_dir = True
        # if assumed state is "off"
        if not is_on(time):
            # update "peak start" time
            cur_on = time
        # update "peak end" time
        last_seen = time
        # if current peak is long
        if last_seen - cur_on > long_delta:
            # turn in selected direction
            if not update:
                print(f'{90 * direction}')
                target = 90 * direction
                motor.set_angle(90 * direction, max_speed=360)
                update = True
    # if we have no peak
    else:
        # if assumed state is off:
        if not is_on(time):
            if update_dir:
                update_dir = False
                # if last peak is short
                if last_seen - cur_on < long_delta:
                    direction *= -1
            if update:
                print('0')
                target = 0
                motor.set_angle(0, max_speed=360)
                update = False


        
end_value = 0


from includes import Gyems, CanBus

bus = CanBus()
motor = Gyems(bus)
pos_target = 0
pos_prev = 0

motor.enable()
if input('Reset motor positon [y/N]? ') in 'yY':
    motor.set_zero()
    print('Reset')


while True:
    while ard.in_waiting:
        data = ard.readline().decode('utf-8', errors='replace').strip()
    
        # Check if data is valid (non-empty and numeric)
        if data:
            try:
                value = float(data)
                raw_data_buffer = raw_data_buffer[1:] + [value]
                filtered_data_buffer = lfilter(b_filt, a_filt, raw_data_buffer)

                if data_time < num_readings_calibrate * period:
                    meanval += filtered_data_buffer[-1]
                elif data_time == num_readings_calibrate * period:
                    meanval /= num_readings_calibrate
                else:
                    end_value = end_value*(1-k)+ abs(filtered_data_buffer[-1] - meanval)*k
                    end_buffer = end_buffer[1:] + [end_value]
                    control(end_value, data_time)
                data_time += period
                if data_time - data_time_mot_upd > 200:
                    motor.set_angle(target, max_speed=360)
                    data_time_mot_upd = data_time
            except ValueError:
                pass

ard.close()
