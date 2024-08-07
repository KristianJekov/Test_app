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
        dict.append(board_ver)
        print(f"Board Version: {board_ver}")

def check_sensor_hub_ver(line, dict):
    if line.__contains__("sensorhub: sensorhub_create - Device firmware version:"):
        sensor_ver_raw = line[-22:]
        sensor_ver = ansi_escape.sub('', sensor_ver_raw)
        dict.append(sensor_ver)
        print(f"Sensor Version: {sensor_ver}")

def check_batt_ver(line, dict):
    if line.__contains__("btdevmng: battery - firmware version:"):
        batt_ver_raw = line[-22:]
        batt_ver = ansi_escape.sub('', batt_ver_raw)
        dict.append(batt_ver)
        print(f"Battery Version: {batt_ver}")


def check_remote_ver(line, dict):
    if line.__contains__("btdevmng: remote - firmware version:"):
        remote_ver_raw = line[-22:]
        remote_ver = ansi_escape.sub('', remote_ver_raw)
        dict.append(remote_ver)
        print(f"Remote Version: {remote_ver}")

def check_if_all_ver_equal(dict):
    if len(dict) == 4:
        print(dict)
        first_element = dict[0]
        if all(element == first_element for element in dict):
            return  print_colored("All devices have the same version", colors["green"])
        else:
         return print_colored("Not all devices have the same version", colors["red"])
    return True
                                                                     