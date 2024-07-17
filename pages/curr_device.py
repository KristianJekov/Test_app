from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import config


def edit_curr_device(driver):

    time.sleep(0.75)

    edit_device_version_button = driver.find_element(By.XPATH, config.EDIT_DEVICE_VERSION)
    edit_device_version_button.click()


    select_specific_version_button = driver.find_element(By.XPATH, config.SELECT_SPECIFIC_VERSION)
    select_specific_version_button.click()


    select_device_version_button = driver.find_element(By.XPATH, config.SELECT_DEVICE_VERSION)
    select_device_version_button.click()


    select_last_version_button = driver.find_element(By.XPATH, config.SELECT_LAST_VERSION)
    select_last_version_button.click()

    time.sleep(0.25)

    save_version_button = driver.find_element(By.XPATH, config.SAVE_VERSION_BUTTON)
    save_version_button.click()