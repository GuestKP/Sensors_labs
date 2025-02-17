from time import sleep
from serial import Serial

from includes import Gyems, CanBus


# connecting both at the same time results in error
bus = CanBus(port="ttyACM4")
motor = Gyems(bus)
ard = Serial('/dev/ttyACM5', baudrate=115200)

try:
    print(motor.enable())
    print(motor.set_zero())
    print(motor.set_speed(100))
    while True:
        #print(motor.info())
        while ard.in_waiting:
            print(ard.readline())
        sleep(0.1)
except KeyboardInterrupt:
    pass

finally:
    motor.disable(True)
    bus.close()