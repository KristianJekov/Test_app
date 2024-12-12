import queue
import sys
import threading

from colorama import Fore
from tqdm import tqdm

from Console_Log.update_info import (
    FirmwareUpdater,  # Importing the FirmwareUpdater class
)

GREEN = "\033[92m"
RESET = "\033[0m"

sys.path.extend(["Console_Log", "Server_App", "Excel_Data"])

from Excel_Data.excel_data_table_maker import *
from Server_App.config import config
from Server_App.utils.mode_select import registerate_device_in_mode
from Server_App.utils.update_device import (
    update_specific_version,
    update_to_last_version,
    update_looper,
    wait_for_update,
)


def navigation_menu(
    qq: queue.Queue, driver, firmware_updater, shutdown_flag: threading.Event
):
    while not shutdown_flag.is_set():
        print(Fore.LIGHTMAGENTA_EX + "------MAIN MENU-------")

        if config.FIRST_TEST:
            device_id = input("Enter Device Serial Number: ")
            config.CURRENT_SERIAL_NUM = device_id

        answer = input(
            "u: Update device\n"
            "r: Register device in specific mode\n"
            "q: Quit\n"
            "Enter your choice: "
        ).lower()

        if answer == "u":
            update_menu(qq, driver, firmware_updater, shutdown_flag)
        elif answer == "r":
            register_menu(driver)
        elif answer == "q":
            shutdown_flag.set()
            break
        else:
            print("Invalid input. Please try again.")


def update_menu(
    qq: queue.Queue, driver, firmware_updater, shutdown_flag: threading.Event
):
    print(Fore.LIGHTMAGENTA_EX + "-------UPDATER--------")
    update = input(
        "l: Update to the last version\n"
        "s: Update to specific version\n"
        "q: Sequence of updates\n"
        "Enter your choice: "
    ).lower()

    if update == "l":
        # Only ask for detailed info once
        show_info = input("Show detailed info for updates? (y/n): ")
        update_to_last_version(driver)
        print(Fore.CYAN + "Connect to WiFi...")
        wait_for_update(qq, firmware_updater, shutdown_flag, show_info.lower())

    elif update == "s":
        version = input("Enter the version you want to update to: ")
        show_info = input("Show detailed info for updates? (y/n): ")

        try:
            update_specific_version(version, driver)
            print(Fore.CYAN + "Connect to WiFi...")
            wait_for_update(qq, firmware_updater, shutdown_flag, show_info.lower())

        except Exception as e:
            print(f"Error: No such version: {version} available for this device")
            return

    elif update == "q":
        print(Fore.LIGHTMAGENTA_EX + "\n----UPDATE LOOPER-----")

        amount = int(input("Amount of updates: "))
        f_version = input("Version 1: ")
        s_version = input("Version 2: ")

        create_empty_worksheet(amount, f_version, s_version)
        print(f"Creating Excel worksheet...")

        config.CURRENT_UPDATE_LOOPER_SETTINGS["amount"] = amount
        config.CURRENT_UPDATE_LOOPER_SETTINGS["f_version"] = f_version
        config.CURRENT_UPDATE_LOOPER_SETTINGS["s_version"] = s_version
        # Ask for detailed info only once for the entire loop
        show_info = input("Show detailed info for updates? (y/n): ")

        try:
            # Pass firmware_updater and queue to the update_looper
            update_looper(
                driver,
                amount,
                f_version,
                s_version,
                firmware_updater,
                qq,
                shutdown_flag,
                show_info.lower(),
            )

        except Exception as e:
            print(f"Error: {e}")
            return


def register_menu(driver):
    print(Fore.LIGHTMAGENTA_EX + "------REGISTRATOR------")
    mode = input(
        "p: Register in Private mode\n"
        "b: Register in Business mode\n"
        "l: Register in Lease mode\n"
        "Enter your choice: "
    ).lower()

    if mode in config.CURRENT_MODE:
        registerate_device_in_mode(config.CURRENT_MODE[mode], driver)
    else:
        print("Invalid mode selected.")
