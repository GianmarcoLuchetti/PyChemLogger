import utils

# Establish a serial connection with the Arduino and reset it
# Specify the correct port and baud rate (e.g. 9600)
serialCom = utils.set_arduino('/dev/cu.usbmodem2101', 9600)

# Loop to continuously read data from the serial port
while True:
    try:
        # Read encoded data
        s_bytes = serialCom.readline()
        # Decode the received bytes to a UTF-8
        decoded_bytes = s_bytes.decode("utf-8".strip('\r\n'))

        # Create a dictionary to store the recorded values
        dict = utils.values_dict(decoded_bytes)
        print(dict)
    except:
        print("ERROR. Line was not recorded \r\n")
