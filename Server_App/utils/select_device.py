from pages.login import login
from pages.devices import filter_devices

def select_device(driver):
    login(driver)
    filter_devices(driver)
   
