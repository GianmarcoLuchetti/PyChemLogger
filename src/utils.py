import serial
import time

def set_arduino(port, baudrate):
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
    serialCom = serial.Serial(port=port, baudrate=baudrate)

    # Reset the Arduino to ensure a fresh start
    serialCom.setDTR(False)
    time.sleep(1)
    serialCom.flushInput()
    serialCom.setDTR(True)

    # Log message
    print('Sensor ready: \r\n')

    return serialCom


def values_dict(values):
    """
    Processes a single line of input and appends the values to the corresponding keys.

    Args:
        values (str): A single string containing comma-separated values in the format:
                      "time,temperature,pH".

    Returns:
        dict: A dictionary with keys 'Time (s)', 'Temperature (C)', and 'pH',
              where each key contains a list with the corresponding values converted to floats.
    """
    # Split the input string into a list of values using commas as the delimiter
    values = values.split(',')

    # Initialize the dictionary with predefined keys and empty lists as values
    data_dict = {
        'Time (s)': [],
        'Temperature (C)': [],
        'pH': []
    }

    # Append the corresponding values to the dictionary keys
    data_dict['Time (s)'].append(float(values[0]))
    data_dict['Temperature (C)'].append(float(values[1]))
    data_dict['pH'].append(float(values[2]))

    # Return the populated dictionary
    return data_dict
