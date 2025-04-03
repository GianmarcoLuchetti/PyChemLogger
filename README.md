# PyChemLogger

A Python-based real-time chemical data logger and analyzer.

This tool collects, visualizes, and stores sensor data (pH and temperature) from chemical reactions, providing live plotting and automatic database storage.

---

## 🚀 Features

- **Serial Sensor Connection:** Reads data from Arduino-compatible sensors.
- **Real-time Data Acquisition:** Continuously collects temperature and pH data.
- **Live Plotting:** Dynamic real-time charts using Matplotlib.
- **Statistical Analysis:** Calculates min, max, average, standard deviation, and median.
- **SQLite Database Storage:** Stores both summary statistics and detailed raw data.
- **Error Handling:** Handles data errors and user interruptions gracefully.

---

## 📂 Project Structure

```
PyChemLogger/
├── src/                    # Source code folder
│   ├── main.py             # Main script to run the logger
│   ├── utils.py            # Utility functions for data reading, plotting, and DB management
│   ├── find_port.py        # Script to list available serial ports
│   └── config.json         # Configuration file (port, baudrate, SQL queries)
├── Sensor Circuit/         # Circuit details folder
│   ├── ph_temp_sensor.ino  # Arduino sensor code
│   └── Circuit.png         # Circuit design
├── requirements.txt        # Libraries required to be installed
└── README.md               # Project documentation
```

---

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/PyChemLogger.git
   cd PyChemLogger
   ```

2. **Create a virtual environment (optional)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## 📌 Usage

1. Connect your Arduino sensor to your computer.

2. Update `src/config.json`:

   - Set the correct **port** (e.g., `/dev/cu.usbmodem101` or `COM3`).
   - Set the correct **baud rate** (default `9600`).

3. Run the data logger:

   ```bash
   python src/main.py
   ```

4. To list available serial ports:

   ```bash
   python src/find_port.py
   ```

---

## 📊 Database Structure

### **Main Table (**`reactions`**):**

Stores summary statistics for each reaction.

| Column                                                                                                     | Type  | Description                       |
|------------------------------------------------------------------------------------------------------------|-------|-----------------------------------|
| ID                                                                                                         | INT   | Primary Key                       |
| Date                                                                                                       | DATE  | Reaction date                     |
| Time\_s                                                                                                    | FLOAT | Total duration in seconds         |
| Min\_pH, Max\_pH, Avg\_pH, Std\_pH, Median\_pH                                                             | FLOAT | pH statistics                     |
| Min\_Temperature\_C, Max\_Temperature\_C, Avg\_Temperature\_C, Std\_Temperature\_C, Median\_Temperature\_C | FLOAT | Temperature statistics            |
| Data\_points                                                                                               | INT   | Number of readings collected      |
| Time\_interval\_s                                                                                          | INT   | Average interval between readings |

### **Sub Tables (**`reaction_number`**):**

Stores raw data for each reaction run.

| Column         | Type  | Description                             |
|----------------|-------|-----------------------------------------|
| ID             | INT   | Primary Key                             |
| Time\_s        | FLOAT | Timestamp in seconds                    |
| Temperature\_C | FLOAT | Temperature reading in °C               |
| pH             | FLOAT | pH reading                              |
| Reaction\_ID   | INT   | Foreign key referencing `reactions(ID)` |

---

## 📄 License

This project is licensed under the **GNU General Public License**.

---

## 👌 Acknowledgments

Developed by Gianmarco Luchetti Sfondalmondo\
2025

