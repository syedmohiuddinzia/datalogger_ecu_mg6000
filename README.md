# Mugin-6000 ECU Datalogger

The DLA-232 aircraft engine is a high-performance two-stroke gasoline engine designed for unmanned aerial vehicles (UAVs). It is installed on the Mugin-6000 VTOL, a large fixed-wing vertical takeoff and landing UAV. The DLA-232 provides reliable power, fuel efficiency, and durability, making it ideal for long-endurance missions. Its integration with the Mugin-6000 enhances operational capabilities, enabling efficient flight performance for surveillance, mapping, and other aerial applications.

## Problem Statement
The DLA-232 aircraft engine on the Mugin-6000 VTOL can face several operational challenges that impact performance and reliability. Issues such as improper fuel mixture and combustion inefficiencies may lead to engine knocking and reduced efficiency. Overheating is another concern, especially during extended flights or in high-temperature environments, which can affect engine longevity. Ignition failures due to spark plug malfunctions or electrical issues may cause misfiring or difficulties in starting the engine. Additionally, throttle response delays can compromise flight stability, particularly during critical phases like takeoff and landing. Sensor failures, such as inaccurate temperature, pressure, or RPM readings, may also disrupt engine control. Furthermore, variations in altitude can affect engine performance due to changes in air pressure and oxygen levels, requiring continuous adjustment.<br>
To mitigate these challenges, the Engine Control Unit (ECU) plays a vital role in optimizing the DLA-232 engine's performance. It regulates fuel injection to maintain the correct air-fuel mixture for efficient combustion, ensuring smooth and reliable operation. The ECU continuously monitors key engine parameters, including temperature, RPM, and pressure, to prevent failures and improve operational safety. It also dynamically adjusts ignition timing for optimal efficiency and provides precise throttle control for stable flight performance. Additionally, the ECU serves as a diagnostic tool, detecting anomalies and triggering failsafe measures to prevent potential damage. By integrating an ECU, the Mugin-6000 VTOL achieves enhanced efficiency, reliability, and flight safety, making it well-suited for demanding UAV applications.

## Engine Control Unit
ECU plays a critical role in managing and optimizing engine performance. Below are the key features and parameters extracted from the document, along with explanations of each parameter.

# Features of ECU
1. **Power Source:** Operates on a 12V LiPo battery (≥3000mAh) to ensure stable performance.
2. **Electronic Fuel Injection (EFI):** Controls fuel injection for efficient combustion.
3. **USB Communication:** Connects to a PC via USB for tuning and monitoring.
4. **EFI Software Support:** Requires EFI software for setup and calibration (not recommended for users to modify).
5. **Throttle Servo Range Adjustment:** Ensures throttle response is within 1000–2000 µs for proper control.
6. **Propeller Matching:** Supports different propeller configurations via pre-loaded .msq files.
7. **Fuel Pump Control:** Manages a 12V fuel pump with an operating voltage of 10.5V–15V and pressure of 300kPa.
8. **Serial Communication Protocol:** Uses TTL-level serial communication with a baud rate of 115200 for data exchange.
9. **Engine Data Monitoring:** Reads real-time parameters like RPM, barometric pressure, temperatures, and battery voltage.
10. **Engine Shut-Off Command:** Can remotely stop the engine by sending a specific command.

### Parameters of ECU
| **Parameter**                              | **Description** |
|--------------------------------------------|----------------|
| **Seconds**                                | Represents the timestamp in seconds from the start of data logging. |
| **Injection Pulse Width 1 (us) & Injection Pulse Width 2 (us)** | Duration (in microseconds) for which the fuel injectors remain open. <br> Determines fuel delivery to the engine cylinders. |
| **RPM (Revolutions Per Minute)**           | Measures engine speed.<br>Essential for performance monitoring and throttle adjustments. |
| **Ignition Advance Angle (deg)**           | Timing of spark ignition in degrees before the piston reaches top dead center (TDC).<br>Affects combustion efficiency and power output. |
| **Injection Event Scheduling**             | Defines the sequence and timing of fuel injection. |
| **Engine Status Flags**                    | **Ready** – Indicates if the ECU is prepared for operation.<br> **Crank** – Signals engine cranking (starting phase).<br> **StartW** – Represents the starting warm-up phase.<br> **Warmup** – Indicates engine is in warm-up mode.<br> **TPSAEN** – Throttle Position Sensor Active Enable.<br> **TPSDEN** – Throttle Position Sensor Deactivation Enable. |
| **Air-Fuel Ratio Target 1 & Target 2**     | Desired air-fuel mixture ratio for combustion.<br>Helps optimize fuel efficiency and emissions. |
| **Wideband Oxygen Sensor (WBO2) Enable 1 & Enable 2** | Indicates whether the oxygen sensor is active for fuel adjustments. |
| **Barometric Pressure (kPa)**              | Measures atmospheric pressure.<br>Used for altitude compensation in the fuel-air mixture. |
| **Manifold Absolute Pressure (MAP) (kPa)** | Measures air pressure inside the intake manifold.<br>Helps determine engine load and fuel injection amount. |
| **Manifold Air Temperature (MAT) (°C)**    | Measures air temperature entering the engine.<br>Important for fuel-air mixture adjustments. |
| **Cylinder Temperature (°C)**              | Monitors cylinder head temperature.<br>Prevents overheating-related failures. |
| **Throttle Position (%)**                  | Represents the percentage of throttle opening.<br>Controls engine power output. |
| **Battery Voltage (V)**                    | Measures ECU power supply voltage.<br>Ensures proper electrical operation of the engine system. |

## Data-Logger for ECU
A datalogger is essential for capturing and analyzing ECU data in real-time, especially when data is not transmitted to the ground for proper monitoring. In UAVs and other engine-driven systems, the ECU continuously monitors critical parameters like RPM, fuel injection, throttle position, temperature, pressure, and battery voltage. However, without a reliable logging system, engineers and operators cannot effectively diagnose performance issues, optimize engine efficiency, or detect potential failures. A datalogger records ECU data locally, allowing for post-flight analysis, troubleshooting, and performance tuning. It helps identify irregularities in fuel delivery, ignition timing, or sensor readings that could otherwise go unnoticed during operation. Additionally, a datalogger ensures historical data storage, enabling long-term trend analysis and predictive maintenance. By implementing a robust logging system, operators can improve engine reliability, enhance flight safety, and optimize overall system performance without depending solely on real-time telemetry transmission.

## Data-Logger V1.0
First, we developed Datalogger 1.0, which utilized an Arduino Nano to read binary data from the ECU and store it efficiently. The Arduino Nano processed the incoming ECU data, converting it into a hexadecimal string, which was then appended to a microSD card for storage. This setup allowed for continuous logging of engine parameters without requiring real-time transmission to the ground. The system featured a simple hardware configuration, with one connection dedicated to power supply and another UART interface for communication between the Arduino Nano and the ECU. Additionally, an LED was mounted on the cover, which blinked whenever data was received from the ECU, providing a visual indication of successful data logging. This initial version provided a foundational approach to capturing ECU data but had limitations in terms of processing power and storage management, leading to further improvements in later versions.

### Issues
While Datalogger 1.0 provided a foundational approach to capturing ECU data, several limitations were identified, necessitating improvements in the next version:
1. **Manual Data Retrieval:** The system required physically unplugging the microSD card to access the log file. This process was cumbersome and inefficient, especially during frequent testing and data analysis sessions.
2. **Disconnection for Analysis:** To analyze the data on the ground, we had to disconnect the system and then reconnect it to EFI software. This added unnecessary downtime and made real-time diagnostics impractical.
3. **False Data Reception:** The controller occasionally received empty data packets, giving the false impression that data was being logged when, in reality, invalid or empty packets were recorded. This led to unreliable data collection and required extra verification steps.
4. **Lack of Real-Time Data Monitoring:** Since the system only logged data to the microSD card, there was no way to monitor ECU parameters in real time. This limitation made troubleshooting and live performance evaluation difficult.
5. **Lack of Wireless Connectivity:** Since the only way to retrieve data was via the microSD card, the absence of wireless data transmission meant that data couldn’t be accessed remotely or integrated into a more comprehensive telemetry system.
6. **No Error Detection & Correction:** There was no built-in mechanism to verify data integrity. Corrupted packets, communication errors, or power fluctuations could result in incomplete or inaccurate logs without any means of correction.
7. **Limited User Feedback:** Aside from the blinking LED indicating data reception, there was no user interface or logging status feedback. Users had no way of knowing if the system was functioning correctly until they retrieved and analyzed the log file.

## Data-Logger V2.0
Building on the foundation of Datalogger 1.0, we developed Datalogger 2.0, leveraging the ESP32 to enhance data acquisition, accessibility, and real-time monitoring. This version features two dedicated serial interfaces: Serial0 for troubleshooting and Serial2 for reading ECU data, ensuring seamless and uninterrupted logging. Data is stored on an MMC card while simultaneously being transmitted to an onboard web server, enabling remote access to log files for reading, downloading, and deletion without requiring physical removal of storage. Three status LEDs provide immediate feedback: one indicates a successful wireless client connection, another confirms data reception from the ECU, and the third signals data being appended to storage. Additionally, the logged packet string is sent to the server, where it is parsed into structured columns, allowing real-time monitoring of engine parameters via Node-RED. These improvements eliminate manual data retrieval, enhance troubleshooting capabilities, and enable real-time analysis, making Datalogger 2.0 a significantly more efficient and user-friendly solution.

### Improvements:
*To address the limitations of Datalogger 1.0, the new version was developed using an ESP32, significantly enhancing functionality, efficiency, and usability. The key improvements include:*

1. **ESP32 Integration:** Upgrading from the Arduino Nano to the ESP32 provided increased processing power, multiple hardware serial ports, and built-in wireless connectivity, eliminating the need for physical data retrieval.
2. **Dedicated Serial Interfaces:**
    - **Serial0:** Used for troubleshooting and debugging, allowing real-time monitoring of system operations.
    - **Serial2:** Dedicated to reading ECU data, ensuring stable and uninterrupted data acquisition.
3. **Status Indicators:** Three dedicated LEDs provide instant visual feedback:
    - **Wireless Client Connection Indicator:** Confirms that a client is connected to the server.
    - **Data Reception Indicator:** Blinks when ECU data is successfully received.
    - **Data Append Indicator:** Signals when data is successfully written to the microSD card (MMC), helping ensure data integrity.
4. **Built-in Web Server:** A server running on the ESP32 enables convenient data access and management, allowing users to:
    - Read log files directly without removing the storage device.
    - Download log files for offline analysis.
    - Delete log files when no longer needed, freeing up storage space.
5. **Live Data Parsing & Visualization:** The logged packet string is transmitted to the server, where it is parsed into structured columns. This allows each engine parameter to be accessed and visualized via Node-RED, enabling real-time monitoring and analysis.

### Benifits:
*Following are the benefits of the new system.*

- **No More Physical SD Card Removal:** Data can be accessed wirelessly, improving efficiency.
- **Real-Time Monitoring:** Parameters can be viewed in real time via the server and Node-RED.
- **Better Debugging:**  The additional serial interface (Serial0) allows for on-the-fly troubleshooting without interfering with ECU data acquisition.
- **Enhanced Reliability:** Dedicated status LEDs provide instant feedback, helping detect issues in real-time.
- **Improved Data Handling:** The ability to delete, download, and parse data via the server simplifies log management.

## Block Diagram
![block-diagram]([FIG/block-diagram.png](https://github.com/syedmohiuddinzia/datalogger_ecu_mg6000/blob/main/v2.0/fig/block-diagram.png))
## Electronic Circuit
![design]([FIG/Design.png](https://github.com/syedmohiuddinzia/datalogger_ecu_mg6000/blob/main/v2.0/fig/Design.png))
## Programming Scripts
- **ESP32 Code:**
[Arduino Code for ESP32]([DataLogger_V2.0/ECU_SDLOG_HTTP/ECU_SDLOG_HTTP.ino](https://github.com/syedmohiuddinzia/datalogger_ecu_mg6000/blob/main/v2.0/ECU_SDLOG_HTTP.ino))
- **HTML file for ESP32 Webserver**
[ESP32 Webserver HTML]([DataLogger_V2.0/ECU_SDLOG_HTTP/index.html](https://github.com/syedmohiuddinzia/datalogger_ecu_mg6000/blob/main/v2.0/index.html))
- **Node-Red Code:**
[Node Red Flows File]([DataLogger_V2.0/flows.json](https://github.com/syedmohiuddinzia/datalogger_ecu_mg6000/blob/main/v2.0/flows.json))
- **CSV Decrypt Code:**
[Decrypt string HEX to String]([DataLogger_V2.0/decryptCSV.py](https://github.com/syedmohiuddinzia/datalogger_ecu_mg6000/blob/main/v2.0/decryptCSV.py))
- **Plot Graph Code:**
[Plot graph from CSV data]([DataLogger_V2.0/CSV_read.py](https://github.com/syedmohiuddinzia/datalogger_ecu_mg6000/blob/main/v2.0/CSV_read.py))


## Instructions
- Upload ESP32 code on ESP32.
- Copy HTML file to Micro USB Card.
- Import Node Red flows file to Node Red, and then deploy it.
- Connect Power and communication connectors to ECU and battery. The power should not exceed 30V. <br>
- Start ECU.
- Connect device wifi to the system.
- Go to Node-Red user interface to analyze the guages.
- To read, delete or download the file, connect mobile or system to the datalogger and go to ip 192.168.4.1.

