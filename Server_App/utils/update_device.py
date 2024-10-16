import queue
import threading
from colorama import Fore
from config import config
from pages.curr_device import edit_curr_device
from utils.select_device import select_device


def update_to_last_version(driver):

    if config.FIRST_TEST == True:
        select_device(driver)
        config.FIRST_TEST = False

    edit_curr_device(driver)
    config.UPDATED = True


def update_specific_version(version, driver):

    if config.FIRST_TEST == True:
        select_device(driver)
        config.FIRST_TEST = False

    edit_curr_device(driver, version)
    config.UPDATED = True


def wait_for_update(
    qq: queue.Queue, firmware_updater, shutdown_flag: threading.Event, show_info: bool
):
    """Wait for updates and show a progress bar."""
    while not shutdown_flag.is_set():
        try:
            line = qq.get(
                timeout=1
            )  # Wait for 1 second before checking the shutdown flag
            if firmware_updater.check_if_update_available(line):
                break
        except queue.Empty:
            continue  # If the queue is empty, continue the loop

    if show_info == "y":
        print("Displaying detailed update info...")
        firmware_updater.show_detiled_update_info(qq, shutdown_flag)

    else:
        firmware_updater.run_update_process(qq, shutdown_flag)


def update_looper(
    driver, amount, ver1, ver2, firmware_updater, qq, shutdown_flag, show_info
):
    """Loop through version A and B updates for the specified number of iterations."""

    for i in range(amount):
        print(f"Starting loop {i + 1} of {amount}")

        # Step 1: Set Version A
        print(f"Setting Version: {ver1}")
        update_specific_version(ver1, driver)
        print(Fore.CYAN + "Connect to WiFi...")

        # Step 2: Wait for Version A update to complete
        wait_for_update(qq, firmware_updater, shutdown_flag, show_info)

        # Check if the shutdown flag is set
        if shutdown_flag.is_set():
            print("Update process interrupted. Exiting loop.")
            break

        # Step 3: Set Version B
        print(f"Setting Version: {ver2}")
        update_specific_version(ver2, driver)
        print(Fore.CYAN + "Connect to WiFi...")

        # Step 4: Wait for Version B update to complete
        wait_for_update(qq, firmware_updater, shutdown_flag, show_info)

        # Check if the shutdown flag is set
        if shutdown_flag.is_set():
            print("Update process interrupted. Exiting loop.")
            break

    print(Fore.GREEN + f"Update Looper completed {amount} cycles successfully!")
    return True
