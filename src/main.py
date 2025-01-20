import utils
import datetime
import json

with open('config.json', 'r') as f:
    config = json.load(f)

def main():
    """
    Main function to read, process, and store sensor data.

    Tasks:
    1. Continuously reads data from the serial communication interface.
    2. Decodes and updates the sensor readings in a dictionary.
    3. Prints formatted readings with two decimal places.
    4. Handles:
        - `ValueError`: Issues with data conversion.
        - `KeyboardInterrupt`: Graceful termination by the user.
    5. Calculates statistics (min, max, average, std deviation) for pH and temperature.
    6. Stores reaction summary in the main database and detailed readings in a sub-table.

    Args:
        None

    Returns:
        None
    """
    # Initialize the serial connection and data dictionary
    serialcom = utils.set_sensor(config['sensor']['port'], config['sensor']['baudrate'])
    data_dict = config['data_dict']

    try:
        while True:
            try:
                # Update the data dictionary with new sensor readings
                data_dict = utils.values_dict(serialcom, data_dict)

                # Extract the latest readings
                time = data_dict['Time_s'][-1]
                temp = data_dict['Temperature_C'][-1]
                pH = data_dict['pH'][-1]

                # Print formatted readings
                print(f"Time: {time:.2f} s, Temperature: {temp:.2f} C, pH: {pH:.2f} \r\n")

            except ValueError as ve:
                print(f"ERROR: {ve}. Data not collected. \r\n")

    except KeyboardInterrupt:
        # Termination by the user
        print("################# Recording ended #################")

    finally:
        # Ensure the serial connection is closed
        serialcom.close()
        print("############ Serial connection closed. ############ \r\n")

    # Compute statistics for pH and temperature
    ph_stat = utils.stat(data_dict['pH'])
    temp_stat = utils.stat(data_dict['Temperature_C'])

    # Prepare reaction summary for the database
    react_info = {
        'Date': datetime.datetime.now().date(),
        'Time_s': data_dict['Time_s'][-1],
        'Min_pH': ph_stat[0],
        'Max_pH': ph_stat[1],
        'Average_pH': ph_stat[2],
        'Std_pH': ph_stat[3],
        'Min_Temperature_C': temp_stat[0],
        'Max_Temperature_C': temp_stat[1],
        'Average_Temperature_C': temp_stat[2],
        'Std_Temperature_C': temp_stat[3],
        'Data_points': len(data_dict['Time_s']),
        'Time_interval_s': int(data_dict['Time_s'][-1]/len(data_dict['Time_s']))
    }

    # Save reaction summary to the main database and detailed readings to a sub-table
    reaction_id = utils.main_table(react_info)
    utils.sub_table(reaction_id, data_dict)


if __name__ == '__main__':
    # Execute the main function
    main()