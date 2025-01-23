import utils
import seaborn as sns
import datetime
import json

with open('config.json', 'r') as f:
    config = json.load(f)

def main():
    """
    Main function to read, process, and store sensor data.

    This function:
    1. Continuously reads data from the serial communication interface.
    2. Updates a dictionary with real-time sensor readings.
    3. Plots real-time temperature and pH data.
    4. Prints formatted readings with two decimal places.
    5. Handles errors gracefully:
        - `ValueError`: Issues with data conversion.
        - `KeyboardInterrupt`: Graceful termination by the user.
    6. Computes statistics for pH and temperature.
    7. Saves a summary in the main database and detailed data in a sub-table.

    Returns:
        None
    """
    # Initialize the serial connection and data dictionary
    serialcom = utils.set_sensor(config['sensor']['port'], config['sensor']['baudrate'])
    data_dict = config['data_dict']

    # Set up plots for real-time data visualization
    sns.set_theme(style="darkgrid")
    fig, ax = utils.rt_plot(num_charts=2)

    try:
        while True:
            try:
                # Update the dictionary with new sensor readings
                data_dict = utils.values_dict(serialcom, data_dict)

                time = data_dict['Time_s'][-1]
                temp = data_dict['Temperature_C'][-1]
                pH = data_dict['pH'][-1]

                # Print readings formatted to two decimal places
                print(f"Time: {time:.2f} s, Temperature: {temp:.2f} C, pH: {pH:.2f}\r\n")

                # Update the real-time plots
                utils.rt_plotting(ax[0], data_dict, 'Temperature_C')
                utils.rt_plotting(ax[1], data_dict, 'pH')

            except ValueError as ve:
                # Handle data conversion errors
                print(f"ERROR: {ve}. Data not collected.\r\n")

    except KeyboardInterrupt:
        # Handle user interruption
        print("################# Recording ended #################")

    finally:
        # Ensure the serial connection is closed
        serialcom.close()
        print("############ Serial connection closed. ############\r\n")

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
        'Median_pH': ph_stat[4],
        'Min_Temperature_C': temp_stat[0],
        'Max_Temperature_C': temp_stat[1],
        'Average_Temperature_C': temp_stat[2],
        'Std_Temperature_C': temp_stat[3],
        'Median_Temperature_C': temp_stat[4],
        'Data_points': len(data_dict['Time_s']),
        'Time_interval_s': int(data_dict['Time_s'][-1] / len(data_dict['Time_s']))
    }

    # Save the reaction summary and detailed readings to the database
    reaction_id = utils.main_table(react_info)
    utils.sub_table(reaction_id, data_dict)

    # Display the final plots
    utils.plot()


if __name__ == '__main__':

    print("""
    ···········································································
    : ____         ____ _                    _                                :
    :|  _ \ _   _ / ___| |__   ___ _ __ ___ | |    ___   __ _  __ _  ___ _ __ :
    :| |_) | | | | |   | '_ \ / _ \ '_ ` _ \| |   / _ \ / _` |/ _` |/ _ \ '__|:
    :|  __/| |_| | |___| | | |  __/ | | | | | |__| (_) | (_| | (_| |  __/ |   :
    :|_|    \__, |\____|_| |_|\___|_| |_| |_|_____\___/ \__, |\__, |\___|_|   :
    :       |___/                                       |___/ |___/           :
    ···········································································
    """)

    main()