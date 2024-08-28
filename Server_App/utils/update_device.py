from utils.select_device import select_device 
from pages.curr_device import edit_curr_device
from config import config

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
        