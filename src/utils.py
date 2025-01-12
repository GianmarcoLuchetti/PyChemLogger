import serial
import time

def set_sensor(port, baudrate):
    """
    Initializes and sets up the Arduino connection.

    This function establishes a serial connection with the Arduino and ensures it is
    properly reset and ready for communication. It performs the following steps:
    1. Establishes a serial connection using the specified port and baud rate.
    2. Resets the Arduino by toggling the Data Terminal Ready (DTR) signal.
    3. Flushes the input buffer to ensure no leftover data affects communication.
    4. Prints a message indicating the sensor is ready.

    Args:
        port (str): The name of the serial port to connect to (e.g., '/dev/cu.usbmodem2101').
        baudrate (int): The baud rate for serial communication (e.g., 9600).

    Returns:
        serial.Serial: The initialized serial connection object.
    """
    # Establish a serial connection with the Arduino
    serialcom = serial.Serial(port=port, baudrate=baudrate)

    # Reset the Arduino to ensure a fresh start
    serialcom.setDTR(False)
    time.sleep(1)
    serialcom.flushInput()
    serialcom.setDTR(True)

    # Log message
    print('################## Sensor ready ##################')
    print('####### Interrupt the process to save data ####### \r\n')

    return serialcom


def decoder(serialcom, encoding='utf-8'):
    """
        Reads and decodes data from a serial communication interface.

        This function reads a line of encoded data from the specified serial communication object,
        decodes it using the specified encoding, and removes any trailing newline or carriage return characters.

        Args:
            serialcom (serial.Serial): A serial communication object used to read data.
            encoding (str, optional): The character encoding used to decode the data. Defaults to 'utf-8'.

        Returns:
            str: The decoded string with trailing newline and carriage return characters stripped.
        """

    # Read encoded data
    s_bytes = serialcom.readline()
    # Decode the received bytes to a UTF-8
    decoded_bytes = s_bytes.decode(encoding.strip('\r\n'))

    return decoded_bytes


def values_dict(serialcom, data_dict):
    """
    Processes a single line of input from the serial communication interface and updates the provided dictionary.

    This function:
    1. Reads and decodes a single line of input from the serial communication interface.
    2. Splits the decoded string into individual values.
    3. Appends the values to the corresponding keys in the input dictionary.

    Args:
        serialcom (serial.Serial): The serial communication object used to read the sensor data.
        data_dict (dict): A dictionary where keys are parameter names (e.g., 'Time (s)', 'Temperature (C)', 'pH'),
                          and values are lists to store the corresponding data.

    Returns:
        dict: The updated dictionary with the new values appended to the appropriate keys.

    Raises:
        Exception: If the number of values in the decoded string does not match the number of keys in the dictionary.
    """

    decoded_values = decoder(serialcom) # Decode the received bytes into a UTF-8 string

    values = decoded_values.split(',') # Split the decoded string into individual values

    # Validate that the number of values matches the number of dictionary keys
    if len(values) != len(data_dict):
        raise Exception('The dictionary must have an entry for each data record')

    for key, value in zip(data_dict.keys(), values): # Append each value to its corresponding key in the dictionary
        data_dict[key].append(float(value))

    return data_dict


def keyboard_interrupt_handler():
    print("################# Recording ended #################")