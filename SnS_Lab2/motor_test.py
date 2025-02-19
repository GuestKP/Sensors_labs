from time import sleep
from serial import Serial
import numpy as np
from time import time

from includes import Gyems, CanBus


bus = CanBus()
motor = Gyems(bus)
ard = Serial('COM9', baudrate=115200)
pos_target = 0
pos_cur = 0
integr = 0
k_imag = 0.1
sim_speed = 0
last_force_update = 0
m = 1

try:
    print(motor.enable())
    print(motor.set_zero())
    state = motor.set_speed(0)

    last_force_update = time()
    while True:
        if ard.in_waiting:
            while ard.in_waiting:
                data = ard.readline()
            try:
                pos_target = -float(data.decode().strip()) / k_imag
            except:
                pass

        t_delta = time() - last_force_update
        last_force_update = time()

        pos_cur = state['angle']
        vel_cur = state['speed']
        dp, dv = pos_target - pos_cur, 0 - vel_cur
        integr += dp
        sim_acc = dp * 200 + dv * 15 + integr * 0.1 # + dp * dv * 0.05
        sim_speed += sim_acc * t_delta
        state = motor.set_speed(sim_speed)

except KeyboardInterrupt:
    pass

finally:
    motor.disable(True)
    bus.close()