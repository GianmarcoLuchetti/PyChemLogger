import serial
import time

f = open('data.csv', 'w', newline='')
f.truncate()

# Establish a serial connection with the Arduino
# Specify the correct port and baud rate (e.g. 9600)
serialCom = serial.Serial('/dev/cu.usbmodem2101', 9600)

# Reset the Arduino to ensure a fresh start
serialCom.setDTR(False)
time.sleep(1)
serialCom.flushInput()
serialCom.setDTR(True)

# Loop to continuously read data from the serial port
while True:
    try:
        # Read encoded data
        s_bytes = serialCom.readline()
        # Decode the received bytes to a UTF-8
        decoded_bytes = s_bytes.decode("utf-8".strip('\r\n'))

        print(decoded_bytes)
    except:
        print("ERROR. Line was not recorded \r\n")
