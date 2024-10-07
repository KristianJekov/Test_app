from pages.devices import filter_devices
from pages.login import login


def select_device(driver):
    login(driver)
    filter_devices(driver)
