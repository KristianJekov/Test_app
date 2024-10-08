import asyncio
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_for_page_load(driver, timeout=10):
    while True:
        ready_state = driver.execute_script("return document.readyState")
        if ready_state == "complete":
            break


def wait_for_element(driver, element):
    while True:
        time.sleep(0.1)
        try:

            WebDriverWait(driver, timeout=6).until(
                EC.element_to_be_clickable((By.XPATH, element))
            )
            break

        except:
            print("Waiting for devices to load...")
            time.sleep(0.1)
            break


def wait_for_massage_to_dissapear(driver, element):
    while True:
        time.sleep(0.1)
        try:
            WebDriverWait(driver, timeout=6).until_not(
                EC.presence_of_element_located((By.XPATH, element))
            )
            break
        except:
            print("Waiting for devices to load...")
            time.sleep(0.1)
            break
