from utils.navigation_menu import navigation_menu
from utils.select_device import driver
from config import config


def s_main():

    while True:
        if config.FIRST_TEST == True:
            navigation_menu()
        else: 
            task_check = input("Do you want to continue? y/n\n")
        
            if task_check == "y":
                navigation_menu()

            else: 
                print("Exiting the program")
                driver.close()
                break
            

if __name__ == '__main__':
    s_main()