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
                print_colored(f"{key}: {dict[key]}", colors["green"]) 
            else:
                print_colored(f"{key}: {dict[key]}", colors["red"])

previous_state = None

def check_if_all_connected(device_ver_dict):
    global previous_state
    

    if len(device_ver_dict) < 4:
        current_state = "Waiting for all components to connect"
        if previous_state != current_state:
            print_colored(current_state, colors["yellow"])
            previous_state = current_state
    else:
        values = device_ver_dict.values()
        unique_values = set(values)
        if len(unique_values) == 1:
            current_state = "All devices have the same version"
            if previous_state != current_state:
                print_colored(current_state, colors["cyan"])
                previous_state = current_state
        else:
            current_state = "Not all devices have the same version"
            if previous_state != current_state:
                print_colored(current_state, colors["yellow"])
                previous_state = current_state

        
         
            
                                                                    # TODO fix the remote mesg as well as all other msgs 

def check_all_components_vers(line, device_ver_dict):

    check_board_ver(line, device_ver_dict)
    check_sensor_hub_ver(line, device_ver_dict)
    check_batt_ver(line, device_ver_dict)
    check_remote_ver(line, device_ver_dict)
    check_if_all_connected(device_ver_dict)

