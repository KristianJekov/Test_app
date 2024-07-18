from utils.update_device import update_to_last_version
from utils.mode_select import registerate_device_in_mode
from config import config


def main():

    answer = input("To update the device to the last version, type u\n" +
                  "To registerate the device in specific mode, type r\n")
    if answer == "u":
        print("-----UPDATER------")
        update_to_last_version()
        
    elif answer == "r":
        print("-----REGISTRATOR------")
        mode = input("To registerate the device in the Private mode, type p\n" +
                     "To registerate the device in the Business mode, type b\n" +
                    "To registerate the device in the Lease mode, type l\n")
        

        registerate_device_in_mode(config.CURRENT_MODE.get(mode))
    else:
        print("Invalid input")
        return
    
 
if __name__ == '__main__':
    main()