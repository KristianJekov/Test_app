import sys
# import subprocess
# subprocess.run('start cmd /k python main.py', shell=True)

sys.path.insert(1,"Server_App")
sys.path.insert(1,"Console_Log")

from selenium import webdriver
from Server_App.config import config

driver = webdriver.Firefox()
driver.get(config.URL)

import threading as th
import queue as q
from menu_tools import navigation_menu

from Console_Log import read

# wifi-service: wifi_service_event_ip_handler - got ip
# wifi-service: wifi_service_event_wifi_handler - sta disconnected

def main():
   qq = q.Queue(maxsize=1024)
   thr1 = th.Thread(target=reading, args=(qq,))
   thr2 = th.Thread(target=menu, args=(qq,))

   thr1.start()
   thr2.start()

   thr1.join()
   thr2.join()

   
def reading(qq: q.Queue):
    read.read_all("COM17", qq)

def menu(qq: q.Queue):

   while True:
        if config.FIRST_TEST == True:
            navigation_menu(qq, driver)
        else: 
            task_check = input("Do you want to continue? y/n\n")
        
            if task_check == "y":
                navigation_menu(qq, driver)

            else: 
                print("Exiting the program")
                driver.close()
                break

if __name__ == '__main__':
    main()
    