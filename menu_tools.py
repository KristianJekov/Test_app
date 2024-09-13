
import queue as q
import sys 
import colorama
from colorama import Fore
from tqdm import tqdm

sys.path.insert(1, "Console_Log")
sys.path.insert(1, "Server_App")   
from Console_Log.update_info import check_if_update_available, update_board, loading_bar
from Server_App.utils.update_device import update_to_last_version, update_specific_version
from Server_App.utils.mode_select import registerate_device_in_mode
from Server_App.config import config

# def convert_version(version_str):
#     parts = version_str.rsplit('.', 1) 
#     return '-'.join(parts)

colorama.init(autoreset=True)

def navigation_menu(qq: q.Queue, driver):
        answer = input("To update the device to the last version, type u\n" +
                    "To registerate the device in specific mode, type r\n")
        
        if answer == "u":
            print(Fore.LIGHTMAGENTA_EX + "-----UPDATER------")
            update = input("To update to the last version, type l\n" +
                        "To update to specific version, type s\n")
            
            if update == "l":
                update_to_last_version(driver)

                print(Fore.CYAN + "Connect to WiFi")

                while True:
                    line = qq.get(block=True)
                    if check_if_update_available(line):
                        break

                bar = tqdm(total=400, desc="Dowloading",  bar_format="{l_bar}{bar} {percentage:3.0f}%| {n_fmt}/{total_fmt}")
                while True:
                    line = qq.get(block=True)
                    if update_board(bar, line):
                        break
                    

            elif update == "s":
                try:
                    version = input("Enter the version you want to update to:\n")
                    update_specific_version(str(version), driver)
                    # config.CURRENT_WANTED_VER = convert_version(str(version))

                    print(Fore.CYAN + "Connect to WiFi")

                    while True:
                        line = qq.get(block=True)
                        if check_if_update_available(line):
                            break 

                    bar = tqdm(total=400, desc="Dowloading",  bar_format="{l_bar}{bar} {percentage:3.0f}%| {n_fmt}/{total_fmt}")
                    while True:
                        line = qq.get(block=True)
                        if update_board(bar, line):
                            break
                    
                             
                except:
                    print("This Board doesnt support that version ")
                    return
            
        elif answer == "r":
            print(Fore.LIGHTMAGENTA_EX + "-----REGISTRATOR------")
            mode = input("To registerate the device in the Private mode, type p\n" +
                        "To registerate the device in the Business mode, type b\n" +
                        "To registerate the device in the Lease mode, type l\n")
            

            registerate_device_in_mode(config.CURRENT_MODE.get(mode), driver)
        else:
            print("Invalid input")
            return