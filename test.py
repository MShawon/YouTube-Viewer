import random
import time

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

uc.install()


print('This will open one chrome driver to test if everything works as expected.')

driver = None

try:
    urls = []
    filename = 'urls.txt'
    load = open(filename)
    loaded = [items.rstrip().strip() for items in load]
    load.close()

    for lines in loaded:
        urls.append(lines)

    print(f"First url : {urls[0]}")

    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    options.headless = False
    options.add_argument("--log-level=3")
    webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {
        'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

    driver = webdriver.Chrome(options=options)

    link = urls[0]
    isdetected = driver.execute_script('return navigator.webdriver')
    print(f'Chrome driver detected ? : {isdetected}')
    driver.get(link)

    play = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.ytp-large-play-button.ytp-button")))
    play.send_keys(Keys.ENTER)
    print('Video played')

    time.sleep(2)
    video_len = driver.execute_script(
        "return document.getElementById('movie_player').getDuration()")

    duration = time.strftime("%Hh:%Mm:%Ss", time.gmtime(video_len))
    print(f'Video Duration : {duration}')

    video_len = video_len*random.uniform(.85, .95)
    duration = time.strftime("%Hh:%Mm:%Ss", time.gmtime(video_len))
    print(f'Watch Duration : {duration}')

    time.sleep(video_len)

    driver.quit()
    print('Closing driver...')

except Exception as e:
    print(e)
    driver.quit()
    print('Closing driver...')
