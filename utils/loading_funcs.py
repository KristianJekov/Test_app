import asyncio
from selenium.webdriver.support.ui import WebDriverWait as wait

# def wait_for_page_load(driver, timeout=10):
#     wait(driver, timeout).until(
#         lambda d: d.execute_script('return document.readyState') == 'complete'
#     )

def wait_for_page_load(driver, timeout=10):
    while True:
        ready_state = driver.execute_script('return document.readyState')
        if ready_state == 'complete':
            break
       
