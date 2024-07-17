from utils.select_device import select_device, driver
from pages.curr_device import edit_curr_device


def update_to_last_version(): 
    select_device()
    edit_curr_device(driver)
    