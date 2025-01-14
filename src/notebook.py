import sqlite3
import json

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

def main_db(data_dict):
    """
    Creates the main reactions table (if it doesn't exist) and inserts a new reaction record.

    Args:
        data_dict (dict): A dictionary containing reaction data to insert into the main table.
                          Example:
                          {
                              "Date": "2025-01-13",
                              "Time_s": 120.5,
                              "Average_pH": 7.25,
                              "Average_Temperature_C": 25.5
                          }

    Returns:
        int: The ID of the newly inserted reaction (used to create a corresponding sub-table).
    """
    connection = sqlite3.connect('PyChemLogger.db')
    cursor = connection.cursor()

    # Create the main reactions table if it doesn't exist
    cursor.execute(config['query']['main_table_create'])
    connection.commit()

    # Insert data into the main reactions table
    cursor.execute(config['query']['main_table_insert'], data_dict)
    connection.commit()

    # Get the ID of the last inserted row
    reaction_id = cursor.lastrowid

    # Close the connection
    connection.close()

    return reaction_id

def sub_table(reaction_id, data_dict):
    """
    Creates a sub-table for a specific reaction and populates it with data.

    Args:
        reaction_id (int): The ID of the reaction (used to name the sub-table).
        data_dict (dict): A dictionary containing data to insert into the sub-table.
                          Keys should match the column names, and values should be lists.
                          Example:
                          {
                              "Time_s": [0.1, 0.2, 0.3],
                              "Temperature_C": [25.0, 25.1, 25.2],
                              "pH": [7.0, 7.1, 7.2]
                          }
    """
    connection = sqlite3.connect("PyChemLogger.db")
    cursor = connection.cursor()

    # Dynamically name the sub-table based on the reaction ID
    reaction_table_name = f"reaction_{reaction_id}"
    print(f"Creating table: {reaction_table_name}")

    # Create the sub-table if it doesn't exist
    cursor.execute(
        config['query']['sub_table_create'].replace("{reaction_table_name}", reaction_table_name)
    )
    connection.commit()

    # Prepare rows for bulk insertion into the sub-table
    rows = [
        (time, temp, pH, reaction_id)
        for time, temp, pH in zip(
            data_dict["Time_s"], data_dict["Temperature_C"], data_dict["pH"]
        )
    ]

    # Insert rows into the sub-table
    cursor.executemany(
        config['query']['sub_table_insert'].replace("{reaction_table_name}", reaction_table_name),
        rows
    )
    connection.commit()

    print(f"Inserted {len(rows)} rows into table {reaction_table_name}")

    # Close the connection
    connection.close()