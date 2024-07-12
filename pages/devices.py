import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import config
# from utils.loading_funcs import wait_for_page_load



def filter_devices(driver):
    devices_tab = driver.find_element(By.XPATH, config.DEVICES_TAB)
    devices_tab.click()

    time.sleep(4)
   

    select_device_type = driver.find_element(By.ID, config.SELECT_DEVICE_TYPE)
    select_device_type.click()      


    select_type = driver.find_element(By.ID, config.SELECT_TYPE)
    select_type.click()


    input_serial_number_feild = driver.find_element(By.ID, config.INPUT_SERIAL_NUMBER)
    input_serial_number_feild.send_keys(config.CURRENT_SERIAL_NUM + Keys.ENTER)

    time.sleep(0.25)

    first_device = driver.find_element(By.XPATH, config.FIRST_DEVICE)
    first_device.click()