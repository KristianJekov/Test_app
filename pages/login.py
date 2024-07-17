import time
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import config
from utils.loading_funcs import wait_for_page_load


def login(driver):
    username = driver.find_element(By.ID, config.USERNAME_FIELD)
    password = driver.find_element(By.ID, config.PASSWORD_FIELD)

    username.send_keys(config.CURRENT_USERNAME)
    password.send_keys(config.CURRENT_PASSWORD)


    time.sleep(1.5)

    login_button = driver.find_element(By.XPATH, config.LOGIN_BUTTON)
    login_button.click()


    wait_for_page_load(driver)
 
