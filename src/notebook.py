import sqlite3

def main_db(data_dict):
    connection = sqlite3.connect('PyChemLogger.db')
    cursor = connection.cursor()

    # SQL query
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reactions (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Date DATE,
    Time_s FLOAT,
    Average_pH FLOAT,
    Average_Temperature_C FLOAT
)""")

    connection.commit()

    cursor.execute("""
        INSERT INTO reactions (Date, Time_s, Average_pH, Average_Temperature_C)
        VALUES (:Date, :Time_s, :Average_pH, :Average_Temperature_C)
        """, data_dict)
    connection.commit()
    connection.close()

