import asyncio
from selenium.webdriver.support.ui import WebDriverWait as wait

# def wait_for_page_load(driver, timeout=10):
#     wait(driver, timeout).until(
#         lambda d: d.execute_script('return document.readyState') == 'complete'
#     )

async def wait_for_page_load(driver, timeout=10):
    start_time = asyncio.get_event_loop().time()
    while True:
        ready_state = driver.execute_script('return document.readyState')
        if ready_state == 'complete':
            return
        if asyncio.get_event_loop().time() - start_time > timeout:
            raise Exception("Page did not load within the given timeout")
        await asyncio.sleep(0.1)
