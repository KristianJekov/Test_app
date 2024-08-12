from utils.update_device import update_to_last_version, update_specific_version
from utils.mode_select import registerate_device_in_mode
from config import config

def convert_version(version_str):
    parts = version_str.rsplit('.', 1) 
    return '-'.join(parts)

def navigation_menu():
        answer = input("To update the device to the last version, type u\n" +
                    "To registerate the device in specific mode, type r\n")
        if answer == "u":
            print("-----UPDATER------")
            update = input("To update to the last version, type l\n" +
                        "To update to specific version, type s\n")
            if update == "l":
                update_to_last_version()
            elif update == "s":
                try:
                    version = input("Enter the version you want to update to:\n")
                    update_specific_version(str(version))
                    config.CURRENT_WANTED_VER = convert_version(str(version))
                    
                except:
                    print("This Board doesnt support that version ")
                    return
            
        elif answer == "r":
            print("-----REGISTRATOR------")
            mode = input("To registerate the device in the Private mode, type p\n" +
                        "To registerate the device in the Business mode, type b\n" +
                        "To registerate the device in the Lease mode, type l\n")
            

            registerate_device_in_mode(config.CURRENT_MODE.get(mode))
        else:
            print("Invalid input")
            return