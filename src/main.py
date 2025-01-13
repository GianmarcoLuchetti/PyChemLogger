import utils
import pandas as pd
import datetime
import notebook
from src.notebook import main_db


def main(serialcom, data_dict):
    """
    Main function to continuously read, decode, and process sensor data.

    This function performs the following tasks:
    1. Continuously reads data from the serial communication interface.
    2. Decodes the received data into a UTF-8 string.
    3. Updates the provided dictionary with the new sensor readings (time, temperature, pH).
    4. Prints the formatted output of the readings with two decimal places.
    5. Handles errors gracefully:
        - `ValueError` for data conversion issues.
        - `KeyboardInterrupt` to allow the user to safely terminate the program.
    6. Converts the updated dictionary into a Pandas DataFrame at the end for further analysis or export.

    Args:
        serialcom (serial.Serial): The serial communication object for interfacing with the sensor.
        data_dict (dict): A dictionary with keys corresponding to the sensor parameters
                          (e.g., 'Time (s)', 'Temperature (C)', 'pH') and values as lists
                          to store the respective data.

    Returns:
        pandas.DataFrame: A DataFrame containing the collected sensor data with columns
                          for 'Time (s)', 'Temperature (C)', and 'pH'.
    """
    try:
        while True:
            try:
                # Update the data dictionary with new values
                data_dict = utils.values_dict(serialcom, data_dict)

                time = data_dict['Time (s)'][-1]
                temp = data_dict['Temperature (C)'][-1]
                pH = data_dict['pH'][-1]

                # Print the formatted output of the current readings
                print(
                    f'Time: {time:.2f} s, Temperature: {temp:.2f} C, pH: {pH:.2f} \r\n'
                )

            except ValueError as ve:
                print(f"ERROR: {ve}. Data not collected. \r\n")

    except KeyboardInterrupt:
        # Handle user interruption and clean up resources
        utils.keyboard_interrupt_handler()

    finally:
        # Ensure the serial connection is closed on exit
        serialcom.close()
        print("############ Serial connection closed. ############ \r\n")

    # Convert the collected data dictionary into a Pandas DataFrame for analysis
    df = pd.DataFrame(data_dict)

    react_info = {
        'Date': datetime.datetime.now().date(),
        'Time_s': df['Time (s)'].iloc[-1],
        'Average_pH': df['pH'].mean(),
        'Average_Temperature_C': df['Temperature (C)'].mean()
    }
    main_db = notebook.main_db(react_info)

    # Return the DataFrame for further processing or saving
    return df


if __name__ == '__main__':
    # Establish a serial connection with the sensor
    # Replace with the appropriate port and baud rate for your setup
    serialCom = utils.set_sensor('/dev/cu.usbmodem101', 9600)

    # Initialize the data dictionary with predefined keys for storing sensor readings
    data_dict = {
        'Time (s)': [],
        'Temperature (C)': [],
        'pH': []
    }

    df = main(serialCom, data_dict)
    print(df)