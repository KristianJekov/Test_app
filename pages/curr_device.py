from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.loading_funcs import wait_for_element
from config import config


def edit_curr_device(driver):

    wait_for_element(driver, config.EDIT_DEVICE_VERSION)

    edit_device_version_button = driver.find_element(By.XPATH, config.EDIT_DEVICE_VERSION)
    edit_device_version_button.click()


    select_specific_version_button = driver.find_element(By.XPATH, config.SELECT_SPECIFIC_VERSION)
    select_specific_version_button.click()


    select_device_version_button = driver.find_element(By.XPATH, config.SELECT_DEVICE_VERSION)
    select_device_version_button.click()


    select_last_version_button = driver.find_element(By.XPATH, config.SELECT_LAST_VERSION)
    select_last_version_button.click()

    save_version_button = driver.find_element(By.XPATH, config.SAVE_VERSION_BUTTON)
    save_version_button.click()