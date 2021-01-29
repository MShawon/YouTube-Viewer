
import platform
import random
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OSNAME = platform.system()
if OSNAME == 'Windows':
    driver_path = 'chromedriver_win32/chromedriver.exe'
elif OSNAME == 'Linux':
    driver_path = 'chromedriver_linux64/chromedriver'
else:
    print('{} OS is not supported.'.format(OSNAME))
    exit()

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

    print("First url : {}".format(urls[0]))

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.headless = False
    options.add_argument("--log-level=3")
    webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {
        'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

    driver = webdriver.Chrome(
        executable_path=driver_path, options=options)

    link = urls[0]

    driver.get(link)
    
    play = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.ytp-large-play-button.ytp-button")))
    play.send_keys(Keys.ENTER)
    print('Video played')

    time.sleep(2)
    video_len = driver.execute_script(
        "return document.getElementById('movie_player').getDuration()")

    print('Video Duration : {}'.format(
        time.strftime("%H:%M:%S", time.gmtime(video_len))))

    video_len = video_len*random.uniform(.85, .95)
    print('Watch Duration : {}'.format(
        time.strftime("%H:%M:%S", time.gmtime(video_len))))

    time.sleep(video_len)

    driver.quit()
    print('Closing driver...')

except Exception as e:
    print(e)
    driver.quit()
    print('Closing driver...')
