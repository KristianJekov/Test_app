import sys
sys.path.insert(1,"Server_App")
sys.path.insert(1,"Console_Log")
 
import threading as th
import queue as q
from navigation_menu import navigation_menu

from Server_App.config import config
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

   print("Unrechable")
   
   menu(qq)
   
def reading(qq: q.Queue):
   read.read_all("COM17", qq)

def menu(qq: q.Queue):

   while True:
        if config.FIRST_TEST == True:
            navigation_menu(qq)
        else: 
            task_check = input("Do you want to continue? y/n\n")
        
            if task_check == "y":
                navigation_menu(qq)

            else: 
                print("Exiting the program")
                config.URL.close()
                break

if __name__ == '__main__':
    main()