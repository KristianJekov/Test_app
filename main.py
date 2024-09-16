import sys
# import subprocess
# subprocess.run('start cmd /k python main.py', shell=True)

sys.path.insert(1,"Server_App")
sys.path.insert(1,"Console_Log")

from selenium import webdriver
from Server_App.config import config
from colorama import init as colorama_init, Fore

driver = webdriver.Firefox()
driver.get(config.URL)

import threading as threading
import queue as queue
from menu_tools import navigation_menu
from Console_Log.update_info import FirmwareUpdater
from Console_Log.read import read_all

shutdown_flag = threading.Event()

def main():
    
    q = queue.Queue(maxsize=1024)
    firmware_updater = FirmwareUpdater()

    read_thread = threading.Thread(target=read_all, args=("COM17", q, shutdown_flag))
    menu_thread = threading.Thread(target=menu_loop, args=(q, driver, firmware_updater))

    read_thread.start()
    menu_thread.start()

    try:
        read_thread.join()
        menu_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        shutdown_flag.set()
        read_thread.join(timeout=2)
        menu_thread.join(timeout=2)
    finally:
        driver.quit()

def menu_loop(q: queue.Queue, driver: webdriver.Firefox, firmware_updater: FirmwareUpdater):
    while not shutdown_flag.is_set():
        navigation_menu(q, driver, firmware_updater, shutdown_flag)
        if not continue_prompt():
            print("Exiting the program")
            shutdown_flag.set()
            break

def continue_prompt():
    while True:
        answer = input(Fore.YELLOW + "Do you want to continue? (y/n): ").lower()
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

if __name__ == '__main__':
    main()
