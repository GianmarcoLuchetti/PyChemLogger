import sqlite3
import json

with open("config.json", "r") as f:
    config = json.load(f)

def main_db(data_dict):
    connection = sqlite3.connect('PyChemLogger.db')
    cursor = connection.cursor()

    # SQL query
    cursor.execute(config['query']['main_table_create'])

    connection.commit()

    cursor.execute(config['query']['main_table_insert'], data_dict)
    connection.commit()
    connection.close()
