from utils.select_device import select_device, driver
from pages.curr_device import edit_curr_device
from config import config

def update_to_last_version():

    if config.FIRST_TEST == True:
        select_device()
        config.FIRST_TEST = False

    edit_curr_device(driver)
    
def update_specific_version(version):
    
    if config.FIRST_TEST == True:
        select_device()
        config.FIRST_TEST = False
        
    edit_curr_device(driver, version)
        