import platform
import random
import subprocess
import sys
import time

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

print('This will open one chrome driver to test if everything works as expected.\n')

print('Getting Chrome Driver...')

OSNAME = platform.system()

"""
Getting Chrome version code has been taken from 
https://github.com/yeongbin-jo/python-chromedriver-autoinstaller
Thanks goes to him.
"""
if OSNAME == 'Linux':
    with subprocess.Popen(['google-chrome', '--version'], stdout=subprocess.PIPE) as proc:
        version = proc.stdout.read().decode('utf-8').replace('Google Chrome', '').strip()
elif OSNAME == 'Darwin':
    OSNAME = 'Macintosh'
    process = subprocess.Popen(
        ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stdout=subprocess.PIPE)
    version = process.communicate()[0].decode(
        'UTF-8').replace('Google Chrome', '').strip()
elif OSNAME == 'Windows':
    process = subprocess.Popen(
        ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
    )
    version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
else:
    print('{} OS is not supported.'.format(OSNAME))
    sys.exit()

major_version = version.split('.')[0]

uc.TARGET_VERSION = major_version

uc.install()

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
