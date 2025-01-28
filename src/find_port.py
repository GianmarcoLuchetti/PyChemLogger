from serial.tools import list_ports

def find_port():
    """
    Lists all available serial ports on the system.

    This function retrieves and prints detailed information about each detected serial port,
    including the device name, description, and hardware ID. It is useful for identifying
    the correct port for connecting to your sensor or other serial devices.

    Returns:
    """
    # Retrieve a list of all available serial ports
    ports = list_ports.comports()

    if not ports:
        print("No serial ports found.")
    else:
        print("Available serial ports:")
        # Iterate over each detected port and print details
        for port in ports:
            print(f"Device: {port.device}, Description: {port.description}, HWID: {port.hwid}")

# Call the function to list serial ports
find_port()
