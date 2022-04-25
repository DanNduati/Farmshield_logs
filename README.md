<h1 align="center"><b>Farmshield Logs</b></h1>

## <b>Description</b>
Decode SD card logs for offline devices

## <b>Prerequisites</b>
- Python3

## <b>Setup</b>
### 1. Clone the repository
```bash
$ git clone git@github.com:IlluminumGreenHouses/Farmshield-Logs.git
```
### 2. Create a python virtual environment activate it
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install project dependencies
```bash
$ pip install -r requirements.txt
```
### 4. Add the sd card log files to the log_files directory

### 5. Run the decode script
```bash
$ python igh_log.py
```
Sample output:
```
***********************************************************
LOGFILE: log_files/5E112576 (1).LOG
***********************************************************
BORON_ID :  e00fce682c5cb310079bc431
MSG_COUNTER :  41

bucket: e00fce682c5cb310079bc431 bucket key: 55e00fce682c5cb310079bc431

SHIELD_ID : 0102030405060708090a6402
STORE_TIMESTAMP : 1578182006
SHIELD_FW_VERSION : 010000
SHIELD_BATTERY_LEVEL : 42.41
VALVE_POSITION : 0
WATER_DISPENSED : 0.00
SPEAR_DATA : 010cffffffffffffffffffffffff1f030000030e02d60e0c0200000402b403060200ff0a0200ff0502db010902060108041f0900003e
SPEAR_ID : ffffffffffffffffffffffff
SPEAR_FW_VERSION : 000003
SPEAR_BATTERY_LEVEL : 3798
LIGHT_INTENSITY : 0
SOIL_MOISTURE : 948
SOIL_HUMIDITY : 65280
SOIL_TEMPERATURE : 65280
AIR_HUMIDITY : 475
AIR_TEMPERATURE : 262
CARBON_DIOXIDE : 2335
***********************************************************
STORED TIME STAMP:  2020/01/05,02:53:26
***********************************************************
```