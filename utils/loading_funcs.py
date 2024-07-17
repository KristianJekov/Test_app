import asyncio
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time

# def wait_for_page_load(driver, timeout=10):
#     wait(driver, timeout).until(
#         lambda d: d.execute_script('return document.readyState') == 'complete'
#     )

def wait_for_page_load(driver, timeout=10):
    while True:
        ready_state = driver.execute_script('return document.readyState')
        if ready_state == 'complete':
            break
       
def wait_for_element(driver, element):
    while True:
        time.sleep(0.2)
        try:

            WebDriverWait(driver,timeout=6).until(EC.element_to_be_clickable((By.XPATH, element)))
            break
        
        except:
            print("Waiting for devices to load...")
            time.sleep(0.2)
            break