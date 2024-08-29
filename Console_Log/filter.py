import re
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)


ansi_escape = re.compile(r'\x1b\[[0-9;]*m')


def check_is_ver_correct(dict, key):
    curr_ver = dict[key] 
    wanted_ver = "2.3-377"

    if  curr_ver[1:-10] == wanted_ver:
        return True
    return False
    
def check_board_ver(line, dict):
    check_component_ver(line, dict, "sifly-main: BUILD_VERSION:", "Board", 51, 69)


def check_sensor_hub_ver(line, dict):
    check_component_ver(line, dict, "sensorhub: sensorhub_create - Device firmware version:", "Sensor Hub", -22)


def check_batt_ver(line, dict):
    check_component_ver(line, dict, "btdevmng: battery - firmware version:", "Battery", -22)

def check_remote_ver(line, dict):
        check_component_ver(line, dict, "btdevmng: remote - firmware version:", "Remote", -22)

def check_component_ver(line, dict, keyword, key, slice, slice_to=None):
    if line.__contains__(keyword):
        ver_raw = line[slice:slice_to]
        ver = ansi_escape.sub('', ver_raw)
        dict[key] = ver
        print_ver_color(dict, key)


def print_ver_color(dict, key):
            if check_is_ver_correct(dict, key):
                print(Fore.GREEN + f"{key}: {dict[key]}") 
            else:
                print(Fore.RED + f"{key}: {dict[key]}")

previous_state = None    

def check_if_all_connected(device_ver_dict):
    global previous_state
    

    if len(device_ver_dict) < 4:
        current_state = "Waiting for all components to connect"
        if previous_state != current_state:
            print(Fore.YELLOW + current_state)
            previous_state = current_state
    else:
        values = device_ver_dict.values()
        unique_values = set(values)
        if len(unique_values) == 1:
            current_state = "All devices have the same version"
            if previous_state != current_state:
                print(Fore.CYAN + current_state)
                previous_state = current_state
        else:
            current_state = "Not all devices have the same version"
            if previous_state != current_state:
                print(Fore.YELLOW + current_state)
                previous_state = current_state


def check_all_components_vers(line, device_ver_dict):

    check_board_ver(line, device_ver_dict)
    check_sensor_hub_ver(line, device_ver_dict)
    check_batt_ver(line, device_ver_dict)
    check_remote_ver(line, device_ver_dict)
    check_if_all_connected(device_ver_dict)

