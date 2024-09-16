import sys
from colorama import Fore
from tqdm import tqdm
import queue
import threading

sys.path.extend(["Console_Log", "Server_App"])

from Server_App.utils.update_device import update_to_last_version, update_specific_version
from Server_App.utils.mode_select import registerate_device_in_mode
from Server_App.config import config

def navigation_menu(qq: queue.Queue, driver, firmware_updater, shutdown_flag: threading.Event):
    while not shutdown_flag.is_set():
        print(Fore.LIGHTMAGENTA_EX + "-----MAIN MENU------")
        answer = input("u: Update device\n"
                       "r: Register device in specific mode\n"
                       "q: Quit\n"
                       "Enter your choice: ").lower()

        if answer == 'u':
            update_menu(qq, driver, firmware_updater, shutdown_flag)
        elif answer == 'r':
            register_menu(driver)
        elif answer == 'q':
            shutdown_flag.set()
            break
        else:
            print("Invalid input. Please try again.")

def update_menu(qq: queue.Queue, driver, firmware_updater, shutdown_flag: threading.Event):
    print(Fore.LIGHTMAGENTA_EX + "-----UPDATER------")
    update = input("l: Update to the last version\n"
                   "s: Update to specific version\n"
                   "Enter your choice: ").lower()

    if update == 'l':
        update_to_last_version(driver)
    elif update == 's':
        version = input("Enter the version you want to update to: ")
        try:
            update_specific_version(version, driver)
        except Exception as e:
            print(f"Error: {e}")
            return

    print(Fore.CYAN + "Connect to WiFi")
    wait_for_update(qq, firmware_updater, shutdown_flag)

def register_menu(driver):
    print(Fore.LIGHTMAGENTA_EX + "-----REGISTRATOR------")
    mode = input("p: Register in Private mode\n"
                 "b: Register in Business mode\n"
                 "l: Register in Lease mode\n"
                 "Enter your choice: ").lower()

    if mode in config.CURRENT_MODE:
        registerate_device_in_mode(config.CURRENT_MODE[mode], driver)
    else:
        print("Invalid mode selected.")

def wait_for_update(qq: queue.Queue, firmware_updater, shutdown_flag: threading.Event):
    while not shutdown_flag.is_set():
        try:
            line = qq.get(timeout=1)  # Wait for 1 second before checking the shutdown flag
            if firmware_updater.check_if_update_available(line):
                break
        except queue.Empty:
            continue  # If the queue is empty, continue the loop

    bar = tqdm(total=400, desc="Downloading", bar_format="{l_bar}{bar} {percentage:3.0f}%| {n_fmt}/{total_fmt}")
    while not shutdown_flag.is_set():
        try:
            line = qq.get(timeout=1)
            if firmware_updater.update_board(bar, line):
                return  # Return to main menu after update is complete
        except queue.Empty:
            continue  # If the queue is empty, continue the loop
    
    bar.close()