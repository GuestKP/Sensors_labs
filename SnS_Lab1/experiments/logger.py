import serial
from time import sleep, time

stm = serial.Serial(baudrate=9600, port="COM17")

sleep(1)
while(stm.inWaiting()):
    stm.read_all()


with open('data.csv', 'w') as f:
    pass

data = ''
while True:
    try:
        sleep(0.1)
        if stm.inWaiting():
            data = stm.read_all().decode()
            #print(data)
        
            with open('data.csv', 'a') as f:
                f.write(data)
    except KeyboardInterrupt:
        break
