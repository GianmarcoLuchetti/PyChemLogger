import serial
import time
import json
import sqlite3

with open("config.json", "r") as f:
    config = json.load(f)

def set_sensor(port, baudrate):
    """
    Initializes a serial connection with an Arduino sensor.

    This function:
    1. Opens a serial connection to the specified port with the given baud rate.
    2. Resets the Arduino by toggling the DTR signal.
    3. Flushes the input buffer to ensure clean communication.
    4. Notifies the user that the sensor is ready.

    Args:
        port (str): Serial port to connect to (e.g., '/dev/cu.usbmodem2101').
        baudrate (int): Baud rate for the connection (e.g., 9600).

    Returns:
        serial.Serial: The configured serial connection object.

    Example:
        $$$ connection = set_sensor('/dev/ttyUSB0', 9600)
        $$$ print(connection.is_open)
        True
    """
    # Establish a serial connection with the Arduino
    serialcom = serial.Serial(port=port, baudrate=baudrate)

    # Reset the Arduino
    serialcom.setDTR(False)  # Deactivate Data Terminal Ready (DTR) signal
    time.sleep(1)  # Allow time for reset
    serialcom.flushInput()  # Clear input buffer
    serialcom.setDTR(True)  # Reactivate DTR signal

    # Notify user that the sensor is ready
    print('################## Sensor ready ##################')
    print('####### Interrupt the process to save data ####### \r\n')

    return serialcom


def decoder(serialcom, encoding='utf-8'):
    """
    Reads and decodes data from a serial communication interface.

    This function:
    1. Reads a line of encoded data from the serial connection.
    2. Decodes the data using the specified character encoding.
    3. Strips any trailing newline or carriage return characters.

    Args:
        serialcom (serial.Serial): A serial communication object used to read data.
        encoding (str, optional): The character encoding to decode the data. Defaults to 'utf-8'.

    Returns:
        str: The decoded string with trailing newline and carriage return characters removed.

    Example:
        $$$ decoded_data = decoder(serialcom)
        $$$ print(decoded_data)
        "Sensor data: 23.5°C"
    """
    # Read a line of encoded data from the serial communication object
    s_bytes = serialcom.readline()

    # Decode the bytes using the specified encoding and strip trailing newline or carriage return characters
    decoded_bytes = s_bytes.decode(encoding).strip('\r\n')

    return decoded_bytes


def values_dict(serialcom, data_dict):
    """
    Reads a line of input from the serial communication interface and updates the provided dictionary.

    This function:
    1. Decodes a line of data from the serial connection.
    2. Splits the decoded string into individual values separated by commas.
    3. Appends these values to the corresponding keys in the dictionary.

    Args:
        serialcom (serial.Serial): The serial communication object used to read sensor data.
        data_dict (dict): A dictionary where:
                          - Keys are parameter names (e.g., 'Time (s)', 'Temperature (C)', 'pH').
                          - Values are lists to store the corresponding data.

    Returns:
        dict: The updated dictionary with new values appended to their respective keys.

    Raises:
        Exception: If the number of values in the decoded string does not match the number of keys in `data_dict`.

    Example:
        $$$ data_dict = {'Time (s)': [], 'Temperature (C)': [], 'pH': []}
        $$$ updated_dict = values_dict(serialcom, data_dict)
        $$$ print(updated_dict)
        {'Time (s)': [1.0], 'Temperature (C)': [23.5], 'pH': [7.4]}
    """
    # Decode a line of input from the serial connection and split the decoded string into a list of values
    decoded_values = decoder(serialcom)
    values = decoded_values.split(',')

    # Check if the number of values matches the number of keys in the dictionary
    if len(values) != len(data_dict):
        raise Exception('The dictionary must have an entry for each data record')

    # Append each value to the corresponding key in the dictionary
    for key, value in zip(data_dict.keys(), values):
        data_dict[key].append(float(value))

    return data_dict


def stat(data_list):
    """
    Compute basic statistics for a list of numerical values.

    This function calculates:
    1. The minimum value in the list.
    2. The maximum value in the list.
    3. The average (mean) of the values.
    4. The standard deviation of the values.

    Args:
        data_list (list): A list of numerical values.

    Returns:
        tuple: A tuple containing the following statistics, each rounded to 4 decimal places:
            - Minimum value (float)
            - Maximum value (float)
            - Average (float)
            - Standard deviation (float)

    Example:
        $$$ data = [1, 2, 3, 4, 5]
        $$$ stats = stat(data)
        $$$ print(stats)
        (1.0, 5.0, 3.0, 1.4142)
    """
    # Compute the minimum and maximum values
    min_val = min(data_list)
    max_val = max(data_list)

    # Compute the average (mean)
    avg = sum(data_list) / len(data_list)

    # Compute the variance and the standard deviation
    variance = sum((x - avg) ** 2 for x in data_list) / len(data_list)
    std = variance ** 0.5

    # Return all statistics rounded to 4 decimal places
    return round(min_val, 4), round(max_val, 4), round(avg, 4), round(std, 4)


def main_table(data_dict):
    """
    Creates the main reactions table (if it doesn't exist) and inserts a new reaction record.

    This function:
    1. Connects to the database `PyChemLogger.db`.
    2. Ensures the main reactions table exists by executing the table creation query.
    3. Inserts a new reaction record using the provided data dictionary.
    4. Returns the ID of the newly inserted record for further use.

    Args:
        data_dict (dict): A dictionary containing reaction data to insert into the main table.

    Returns:
        int: The ID of the newly inserted reaction, which can be used to create a corresponding sub-table.

    Example:
        $$$ data = {
        ...     "Date": "2025-01-13",
        ...     "Time_s": 120.5,
        ...     "Min_pH": 5.400,
        ...     "Max_pH": 9.200,
        ...     "Average_pH": 7.2565,
        ...     "Std_pH": 2.3423,
        ...     "Min_Temperature_C": 18.8273,
        ...     "Max_Temperature_C": 29.9383,
        ...     "Average_Temperature_C": 25.5625,
        ...     "Std_Temperature_C": 4.6563,
        ...     "Data_points": 50,
        ...     "Time_interval_s": 3
        ... }
        $$$ reaction_id = main_table(data)
        $$$ print(f"Inserted reaction ID: {reaction_id}")
        Inserted reaction ID: 1
    """

    # Retrieve SQL queries for creating the table and inserting data
    create_query = config['query']['main_table_create']
    insert_query = config['query']['main_table_insert']

    # Connect to the database using a context manager for automatic resource handling
    with sqlite3.connect('PyChemLogger.db') as connection:
        cursor = connection.cursor()

        # Create the main table if it doesn't exist
        cursor.execute(create_query)
        connection.commit()

        # Insert the reaction data into the main table
        cursor.execute(insert_query, data_dict)
        connection.commit()

        # Retrieve the ID of the last inserted row
        reaction_id = cursor.lastrowid

    return reaction_id


def sub_table(reaction_id, data_dict):
    """
    Creates a sub-table for a specific reaction and populates it with data.

    This function:
    1. Dynamically generates a sub-table name based on the reaction ID.
    2. Creates the sub-table if it does not already exist.
    3. Inserts the data from the provided dictionary into the sub-table.

    Args:
        reaction_id (int): The ID of the reaction, used to uniquely name the sub-table.
        data_dict (dict): A dictionary containing data to insert into the sub-table.
                          Keys should match the column names, and values should be lists.

    Returns:
        None

    Example:
        $$$ reaction_id = 1
        $$$ data = {
        ...     "Time_s": [0.1, 0.2, 0.3],
        ...     "Temperature_C": [25.0, 25.1, 25.2],
        ...     "pH": [7.0, 7.1, 7.2]
        ... }
        $$$ sub_table(reaction_id, data)
        Creating table: reaction_1
        Inserted 3 rows into table reaction_1
    """
    # Generate a dynamic name for the sub-table based on the reaction ID
    reaction_table_name = f"reaction_{reaction_id}"

    # Retrieve and format the SQL query for creating the sub-table
    create_query = config['query']['sub_table_create'].replace("{reaction_table_name}", reaction_table_name)

    # Prepare the data rows for insertion
    rows = [
        (time, temp, pH, reaction_id)
        for time, temp, pH in zip(
            data_dict["Time_s"], data_dict["Temperature_C"], data_dict["pH"]
        )
    ]

    # Retrieve and format the SQL query for inserting rows into the sub-table
    insert_query = config['query']['sub_table_insert'].replace("{reaction_table_name}", reaction_table_name)

    # Use a context manager to handle the database connection
    with sqlite3.connect('PyChemLogger.db') as connection:
        cursor = connection.cursor()

        # Create the sub-table if it doesn't exist
        print(f"########### Creating table: {reaction_table_name} ###########")
        cursor.execute(create_query)
        connection.commit()

        # Insert the prepared rows into the sub-table
        cursor.executemany(insert_query, rows)
        connection.commit()

    print(f"##### Inserted {len(rows)} rows into table {reaction_table_name} ##### \r\n")
