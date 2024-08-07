import re


ansi_escape = re.compile(r'\x1b\[[0-9;]*m')


def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")


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
        key = 'Board'
        dict[key] = board_ver
        print(f"{key}: {dict[key]}")
        

def check_sensor_hub_ver(line, dict):
    if line.__contains__("sensorhub: sensorhub_create - Device firmware version:"):
        sensor_ver_raw = line[-22:]
        sensor_ver = ansi_escape.sub('', sensor_ver_raw)
        key = 'Sensor Hub'
        dict[key] = sensor_ver
        print(f"{key}: {dict[key]}")


def check_batt_ver(line, dict):
    if line.__contains__("btdevmng: battery - firmware version:"):
        batt_ver_raw = line[-22:]
        batt_ver = ansi_escape.sub('', batt_ver_raw)
        key = 'Battery'
        dict[key] = batt_ver
        print(f"{key}: {dict[key]}")


def check_remote_ver(line, dict):
    if line.__contains__("btdevmng: remote - firmware version:"):
        remote_ver_raw = line[-22:]
        remote_ver = ansi_escape.sub('', remote_ver_raw)
        key = 'Remote'
        dict[key] = remote_ver
        print(f"{key}: {dict[key]}")


def check_if_all_ver_equal(dict):
    if len(dict) == 4 or len(dict) == 3:

        values = dict.values()
       
        unique_values = set(values)
       
        if len(unique_values) == 1:
            return  print_colored("All devices have the same version", colors["green"])
        
        else:
            # print_colored(unique_values, colors["yellow"])
            return print_colored("Not all devices have the same version", colors["red"])
        
    return True
                                                                     



def check_all_components_vers(line, versions_dict):
    check_board_ver(line, versions_dict)
    check_sensor_hub_ver(line, versions_dict)
    check_batt_ver(line, versions_dict)
    check_remote_ver(line, versions_dict)