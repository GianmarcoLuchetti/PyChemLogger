/**
 * Arduino Code for pH and Temperature Monitoring
 * Hardware:
 * - PH4502C pH Sensor (OUT → A0, V+ → 5V, GND → GND)
 * - DS18B20 Temperature Sensor (DATA → D2, VCC → 5V, GND → GND with 4.7kΩ pull-up resistor)
 * 
 * Output Format: time(s), temperature(°C), pH"
 * 
 * Libraries Required:
 * - OneWire: https://www.arduino.cc/reference/en/libraries/onewire/
 * - DallasTemperature: https://www.arduino.cc/reference/en/libraries/dallastemperature/
 */

#include <OneWire.h>             // For DS18B20 communication
#include <DallasTemperature.h>   // For DS18B20 temperature conversion

// Pin Definitions
#define PH_PIN A0                // pH sensor analog input
#define ONE_WIRE_BUS 2           // DS18B20 data pin (D2)

// Calibration Constants (ADJUST THESE!)
#define PH_OFFSET 3.69           // Voltage at pH 7.0 (calibrate with pH 7 buffer)
#define PH_SLOPE -0.103          // Slope (calibrate with pH 4.0 and 7.0 buffers)
#define TEMP_COEFF 0.03          // Temperature compensation coefficient (see datasheet)

// Initialize DS18B20 sensor
OneWire oneWire(ONE_WIRE_BUS);               // OneWire bus on pin D2
DallasTemperature sensors(&oneWire);         // DallasTemperature object

void setup() {
  Serial.begin(9600);            // Start serial communication at 9600 baud
  sensors.begin();               // Initialize DS18B20 sensor
  delay(1000);                   // Allow time for sensor stabilization
}

void loop() {
  // --- Read Temperature ---
  sensors.requestTemperatures();             // Send command to read temperature
  float temperature = sensors.getTempCByIndex(0); // Read temperature in °C

  // --- Read pH Sensor ---
  int rawValue = analogRead(PH_PIN);         // Read analog value (0-1023)
  float voltage = rawValue * (5.0 / 1024.0); // Convert to voltage (0-5V)

  // --- Calculate pH ---
  // Formula: pH = [(Voltage - Offset) / Slope] + 7.0
  float pHValue = (voltage - PH_OFFSET) / PH_SLOPE + 7.0;

  // --- Temperature Compensation ---
  // Adjust pH based on temperature deviation from 25°C
  // Formula: pH_compensated = pH / (1 + k*(T - 25))
  pHValue = pHValue / (1.0 + TEMP_COEFF * (temperature - 25.0));

  // --- Print Data in CSV Format ---
  Serial.print(millis() / 1000);  // Time since startup (s)
  Serial.print(", ");
  Serial.print(temperature, 1);  // Temperature (°C, 1 decimal)
  Serial.print(", ");
  Serial.println(pHValue, 1);  // pH (2 decimals)

  delay(2000); // Sampling interval (adjust as needed)
}

// ============================================================
// Notes for Users:
// 1. Calibrate PH_OFFSET and PH_SLOPE using pH 4.0/7.0/10.0 buffer solutions.
// 2. Ensure DS18B20 has a 4.7kΩ pull-up resistor between DATA and 5V.
// 3. If pH readings drift, add a 0.1µF capacitor between pH sensor V+ and GND.
// 4. Adjust TEMP_COEFF based on the PH4502C datasheet (default = 0.03).
// ============================================================