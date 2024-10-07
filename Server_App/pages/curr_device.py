from config import config
from selenium.webdriver.common.by import By
from utils.loading_funcs import wait_for_element


def edit_curr_device(driver, version=0):

    wait_for_element(driver, config.EDIT_DEVICE_VERSION)
    try:
        edit_device_version_button = driver.find_element(
            By.XPATH, f"{config.EDIT_DEVICE_VERSION}[2]"
        )
        edit_device_version_button.click()

    except:
        edit_device_version_button = driver.find_element(
            By.XPATH, f"{config.EDIT_DEVICE_VERSION}[1]"
        )
        edit_device_version_button.click()

    select_specific_version_button = driver.find_element(
        By.XPATH, config.SELECT_SPECIFIC_VERSION
    )
    select_specific_version_button.click()

    select_device_version_button = driver.find_element(
        By.XPATH, config.SELECT_DEVICE_VERSION
    )
    select_device_version_button.click()

    if version == 0:
        select_last_version_button = driver.find_element(
            By.XPATH, config.SELECT_LAST_VERSION
        )
        select_last_version_button.click()
    else:

        select_last_version_button = driver.find_element(
            By.XPATH,
            f"//*[contains(@class, 'mat-option-text') and contains(text(), '{version}')]",
        )
        select_last_version_button.click()

    save_version_button = driver.find_element(By.XPATH, config.SAVE_VERSION_BUTTON)
    save_version_button.click()
