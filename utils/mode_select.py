from utils.select_device import select_device, driver
from utils.loading_funcs import wait_for_element
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import config
import time


    
def registerate_device_in_mode(mode):
    select_device()

    if('Deregistered' not in driver.find_element(By.XPATH, config.STATE).text):
        
        wait_for_element(driver,config.DEREGISTERATE_BTN)

        deregisterate_btn = driver.find_element(By.XPATH, config.DEREGISTERATE_BTN)
        deregisterate_btn.click()

        time.sleep(0.5)

        deregisterate_confirm = driver.find_element(By.XPATH, config.DEREGISTERATE_CONFIRM_BTN)
        deregisterate_confirm.click()



    wait_for_element(driver,config.REGISTERATE_DEVICE_BTN)

    register_btn = driver.find_element(By.XPATH, config.REGISTERATE_DEVICE_BTN)
    register_btn.click()
    
    wait_for_element(driver,config.SELECT_REGISTRATOR)

    register_select = driver.find_element(By.XPATH, config.SELECT_REGISTRATOR)
    register_select.click()
    
    if (mode == "Private"):
        select_fourth_registrator = driver.find_element(By.XPATH, config.SELECT_FOURTH_REGISTRATOR)
        select_fourth_registrator.click()
    else:
        select_first_registrator = driver.find_element(By.XPATH, config.SELECT_FIRST_REGISTRATOR)
        select_first_registrator.click()

    if (mode == "Lease"):

        select_mode = driver.find_element(By.XPATH, config.SELECT_MODE)
        select_mode.click()

        select_lease = driver.find_element(By.XPATH, config.SELECT_LEASE_MODE)
        select_lease.click()

    registerate_confirm = driver.find_element(By.XPATH, config.REGISTERATE_CONFIRM_BTN)
    registerate_confirm.click()



