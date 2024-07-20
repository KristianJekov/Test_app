from pages.login import login
from pages.devices import filter_devices
from selenium import webdriver
from config import config

driver = webdriver.Firefox()
driver.get(config.URL)
# driver.set_window_position(-1000, 0)  # moves window out of the screen


def select_device():
    login(driver)
    filter_devices(driver)
   
    