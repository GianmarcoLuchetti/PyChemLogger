from serial.tools import list_ports

def find_port():
    ports = list_ports.comports()
    for port in ports:
        print(port)

find_port()