import re


ansi_escape = re.compile(r'\x1b\[[0-9;]*m')


def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

# Color codes for text
colors = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
    "reset": "0"
}


def check_board_ver(line, dict):
     if line.__contains__("sifly-main: BUILD_VERSION:"):     
        board_ver = line[51:69]
        key = 'Board Version'
        dict[key] = board_ver
        print(f"{key}: {dict[key]}")
        

def check_sensor_hub_ver(line, dict):
    if line.__contains__("sensorhub: sensorhub_create - Device firmware version:"):
        sensor_ver_raw = line[-22:]
        sensor_ver = ansi_escape.sub('', sensor_ver_raw)
        key = 'Sensor Hub Version'
        dict[key] = sensor_ver
        print(f"{key}: {dict[key]}")

def check_batt_ver(line, dict):
    if line.__contains__("btdevmng: battery - firmware version:"):
        batt_ver_raw = line[-22:]
        batt_ver = ansi_escape.sub('', batt_ver_raw)
        key = 'Battery Version'
        dict[key] = batt_ver
        print(f"{key}: {dict[key]}")


def check_remote_ver(line, dict):
    if line.__contains__("btdevmng: remote - firmware version:"):
        remote_ver_raw = line[-22:]
        remote_ver = ansi_escape.sub('', remote_ver_raw)
        key = 'Remote Version'
        dict[key] = remote_ver
        print(f"{key}: {dict[key]}")

def check_if_all_ver_equal(dict):
    if len(dict) == 4 or len(dict) == 3:
        # print('\n'.join(f"{key}: {value}" for key, value in dict.items()))

        values = dict.values()
       
        unique_values = set(values)
       
        if len(unique_values) == 1:
            return  print_colored("All devices have the same version", colors["green"])
        else:
         return print_colored("Not all devices have the same version", colors["red"])
    return True
                                                                     