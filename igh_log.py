#!/usr/bin/env python3
import os
import random
import string
import datetime
import struct


# log file
logfile_dir = "log_files"


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_tuple_name(tuple_id):
    switcher = {
        0x00: "MSG_ACK_TUPLE",
        0x01: "SPEAR_ID",
        0x02: "STORE_TIMESTAMP",
        0x03: "SEND_TIMESTAMP",
        0x04: "SOIL_MOISTURE",
        0x05: "AIR_HUMIDITY",
        0x06: "SOIL_HUMIDITY",
        0x07: "WATER_DISPENSED",
        0x08: "CARBON_DIOXIDE",
        0x09: "AIR_TEMPERATURE",
        0x0A: "SOIL_TEMPERATURE",
        0x0B: "SOIL_NITROGEN",
        0x0C: "LIGHT_INTENSITY",
        0x0D: "SHIELD_BATTERY_LEVEL",
        0x0E: "SPEAR_BATTERY_LEVEL",
        0x0F: "VALVE_POSITION",
        0x10: "IGH_SEND_SETTINGS",
        0x11: "IGH_READ_SETTINGS",
        0x12: "SPEAR_DATA",
        0x13: "SPEAR_RF_ID",
        0x14: "SHIELD_RF_ID",
        0x15: "SEND_INTERVAL",
        0x16: "OP_STATE",
        0x17: "SHIELD_ID",
        0x18: "SPEAR_BATT_LOW_THRESHOLD",
        0x19: "SHIELD_BATT_LOW_THRESHOLD",
        0x1A: "BUTTON_PRESS",
        0x1B: "SHIELD_FW_VERSION",
        0x1C: "SOIL_POTASSIUM",
        0x1D: "SOIL_PHOSPHOROUS",
        0x1E: "SPEAR_SERIAL_SENSOR_TYPE",
        0x1F: "SPEAR_FW_VERSION",
        0xFC: "EVENT",
        0xFD: "RESTART",
        0xFE: "DATA_PKT",
        0xFF: "END_OF_PKT_ID"
    }
    return switcher.get(tuple_id, "UNKNOWN")


def process_and_upload_tuples(packet, start, stop, _boron_id):
    local_bucket_name = _boron_id
    local_bucket_key = "55"+_boron_id
    print("\nbucket: " + local_bucket_name + " bucket key: " +
          local_bucket_key + "\n")

    byte_tracker = start
    current_unix_time = 0

    while byte_tracker < stop:

        tuple_id = packet[byte_tracker]

        if 0x3e == tuple_id:  # Break if end of message
            break

        tuple_len = packet[(byte_tracker + 1)]
        tuple_data = packet[(byte_tracker + 2): (byte_tracker + 2 + tuple_len)]
        tuple_name = get_tuple_name(tuple_id)
        print(tuple_name, end=' : ')

        if tuple_id == 18:

            print(str(tuple_data.hex()))
            byte_tracker += 2
        else:
            if tuple_len == 0x01:
                print(tuple_data[0])
            elif tuple_len == 0x02:
                [uint16_var] = struct.unpack('<H', tuple_data)
                print(uint16_var)
            elif tuple_len == 0x04:
                if (tuple_id == 0x0D) or (tuple_id == 0x07):
                    [float_var] = struct.unpack('<f', tuple_data)
                    print("%.2f" % float_var)
                else:  # assume it is a uint32, timestamps
                    [uint32_var] = struct.unpack('<I', tuple_data)
                    print(uint32_var)
                    if tuple_id == 0x02:
                        current_unix_time = uint32_var
                        _timestamp = datetime.datetime.fromtimestamp(
                            current_unix_time)
                        str_timestamp = _timestamp.strftime(
                            '%Y/%m/%d,%H:%M:%S')

            else:  # print out the bytes for longer data
                if (tuple_id == 0x1F) or (tuple_id == 0x1B):
                    _version = str(
                        tuple_data[0]) + "." + str(tuple_data[1]) + "." + str(tuple_data[2])
                print(str(tuple_data.hex()))
            byte_tracker += tuple_len + 2

    timestamp = datetime.datetime.fromtimestamp(current_unix_time)
    print("***********************************************************")
    print("STORED TIME STAMP: ", timestamp.strftime('%Y/%m/%d,%H:%M:%S'))
    print("***********************************************************")
    print("")
    print("")
    print("")


def open_log(filename):
    try:
        fp = open(filename, 'rb')
    except FileNotFoundError:
        print(F'This {filename} file does not exist. Please try again.')
    else:
        pass
    return fp


def read_log(file):
    fp = open_log(file)
    data = fp.read()
    boron_id = str(data[4:16].hex())
    print("BORON_ID : ", boron_id)
    print("MSG_COUNTER : ", str(data[16]))
    payload_len = data[18]
    process_and_upload_tuples(data, 19, payload_len + 18, boron_id)


def main():
    for filename in os.listdir(logfile_dir):
        f = os.path.join(logfile_dir, filename)
        if os.path.isfile(f):
            print("***********************************************************")
            print(F"LOGFILE: {f}")
            print("***********************************************************")
            read_log(f)


if __name__ == "__main__":
    main()
