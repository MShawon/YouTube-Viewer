"""
MIT License

Copyright (c) 2021 MShawon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import concurrent.futures.thread
import os
import platform
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import undetected_chromedriver as uc
from fake_useragent import UserAgent, UserAgentError
from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver

uc.install()

os.system("")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(bcolors.OKGREEN + """

Yb  dP  dP"Yb  88   88 888888 88   88 88""Yb 888888                   
 YbdP  dP   Yb 88   88   88   88   88 88__dP 88__                     
  8P   Yb   dP Y8   8P   88   Y8   8P 88""Yb 88""                     
 dP     YbodP  `YbodP'   88   `YbodP' 88oodP 888888  

                        Yb    dP 88 888888 Yb        dP 888888 88""Yb 
                         Yb  dP  88 88__    Yb  db  dP  88__   88__dP 
                          YbdP   88 88""     YbdPYbdP   88""   88"Yb  
                           YP    88 888888    YP  YP    888888 88  Yb 
""" + bcolors.ENDC)

print(bcolors.OKCYAN + """
           [ GitHub : https://github.com/MShawon/YouTube-Viewer ]
""" + bcolors.ENDC)
print(bcolors.OKGREEN + 'Proxy with Authentication Edition\n' + bcolors.ENDC)
print(bcolors.WARNING + 'Collecting User-Agent...' + bcolors.ENDC)

try:
    ua = UserAgent(use_cache_server=False, verify_ssl=False)
except UserAgentError:
    ua = UserAgent(path='fake_useragent_0.1.11.json')


PROXY = None
driver = None
status = None

view = []
duration_dict = {}


def load_url():
    links = []
    print(bcolors.WARNING + 'Loading urls...' + bcolors.ENDC)
    filename = 'urls.txt'
    load = open(filename)
    loaded = [items.rstrip().strip() for items in load]
    load.close()

    for lines in loaded:
        links.append(lines)

    print(bcolors.OKGREEN +
          f'{len(links)} url loaded from urls.txt' + bcolors.ENDC)

    return links


def load_search():
    search = []
    print(bcolors.WARNING + 'Loading queries...' + bcolors.ENDC)
    filename = 'search.txt'
    load = open(filename, encoding="utf-8")
    loaded = [items.rstrip().strip() for items in load]
    loaded = [[i.strip() for i in items.split(':')] for items in loaded]
    load.close()

    for lines in loaded:
        search.append(lines)

    print(bcolors.OKGREEN +
          f'{len(search)} query loaded from search.txt' + bcolors.ENDC)

    return search


def load_proxy():
    proxies = []

    filename = input(bcolors.OKBLUE +
                     'Enter your proxy file name: ' + bcolors.ENDC)
    load = open(filename)
    loaded = [items.rstrip().strip() for items in load]
    load.close()

    for lines in loaded:
        proxies.append(lines)

    return proxies


def bypassAgree(driver):
    frame = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.ID, "iframe")))
    driver._switch_to.frame(frame)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.ID, "introAgreeButton"))).click()
    driver.switch_to.default_content()


def bypassSignIn(driver):
    nothanks = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "style-scope.yt-button-renderer.style-text.size-small")))
    nothanks.click()
    time.sleep(random.randint(1, 5))
    bypassAgree(driver)


def sleeping():
    time.sleep(30)


def viewVideo(position):
    try:
        PROXY = proxy_list[position]

        agent = ua.chrome
        while OSNAME not in agent:
            agent = ua.chrome

        print(bcolors.OKBLUE + f"Tried {position} | " +
              bcolors.OKGREEN + f'{PROXY} --> Searching for videos...' + bcolors.ENDC)

        if position % 2:
            method = 1
            url = random.choice(urls)
        else:
            method = 2
            query = random.choice(queries)
            url = f"https://www.youtube.com/results?search_query={query[0].replace(' ', '%20')}"

        options = webdriver.ChromeOptions()
        options.headless = background
        viewport = ['2560,1440', '1920,1080', '1440,900',
                    '1536,864', '1366,768', '1280,1024', '1024,768']
        options.add_argument(f"--window-size={random.choice(viewport)}")
        options.add_argument("--log-level=3")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f"user-agent={agent}")
        webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {
            'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
        sw_options = {
            'disable_capture': True  # Pass all requests straight through
        }

        if proxy_type == 'https':
            sw_options = {
                'proxy': {
                    'https': f'https://{PROXY}',
                }
            }
        else:
            sw_options = {
                'proxy': {
                    'http': f'socks5://{PROXY}',
                    'https': f'socks5://{PROXY}',
                }
            }

        driver = webdriver.Chrome(
            options=options, seleniumwire_options=sw_options)

        driver.get(url)

        try:
            if method == 1:
                play = WebDriverWait(driver, 80).until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.ytp-large-play-button.ytp-button")))
                play.send_keys(Keys.ENTER)

            else:
                find_video = WebDriverWait(driver, 80).until(EC.element_to_be_clickable(
                    (By.XPATH, f'//*[@title="{query[1]}"]')))
                find_video.click()

            bypassSignIn(driver)

        except ElementNotInteractableException:
            try:
                bypassSignIn(driver)
            except ElementNotInteractableException:
                bypassAgree(driver)

        except NoSuchElementException:
            driver.refresh()

        except:
            pass

        try:
            driver.find_element_by_css_selector('[title^="Pause (k)"]')
        except:
            driver.find_element_by_css_selector('[title^="Play (k)"]').click()

        try:
            video_len = duration_dict[url]
        except KeyError:
            WebDriverWait(driver, 80).until(
                EC.element_to_be_clickable((By.ID, 'movie_player')))

            video_len = driver.execute_script(
                "return document.getElementById('movie_player').getDuration()")

            duration_dict[url] = video_len

        # Randomizing watch duration between 85% to 95% of total video duration
        # to avoid pattern and youtube next suggested video
        video_len = video_len*random.uniform(.85, .95)

        duration = time.strftime("%Hh:%Mm:%Ss", time.gmtime(video_len))
        print(bcolors.OKBLUE + f"Tried {position} |" + bcolors.OKGREEN +
              f' {PROXY} --> Video Found : {url} | Watch Duration : {duration} ' + bcolors.ENDC)

        try:
            driver.find_element_by_css_selector('[title^="Pause (k)"]')
        except:
            bypassSignIn(driver)

        time.sleep(video_len)
        driver.quit()

        view.append(position)
        print(bcolors.OKCYAN +
              f'View added : {len(view)}' + bcolors.ENDC)

    except Exception as e:
        print(bcolors.FAIL + f"Tried {position} |" +
              str(e) + bcolors.ENDC)
        driver.quit()
        pass


def main():
    pool_number = [i for i in range(total_proxies)]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(viewVideo, position)
                   for position in pool_number]

        try:
            for future in as_completed(futures):
                if len(view) == views:
                    print(
                        bcolors.WARNING + f'Amount of views added : {views} | Stopping program...But this can take some time to close all threads.' + bcolors.ENDC)
                    executor._threads.clear()
                    concurrent.futures.thread._threads_queues.clear()
                    break
                future.result()

        except KeyboardInterrupt:
            executor._threads.clear()
            concurrent.futures.thread._threads_queues.clear()


if __name__ == '__main__':

    OSNAME = platform.system()
    if OSNAME == 'Darwin':
        OSNAME = 'Macintosh'

    urls = load_url()
    queries = load_search()

    views = int(input(bcolors.OKBLUE + 'Amount of views : ' + bcolors.ENDC))

    gui = str(input(
        bcolors.WARNING + 'Do you want to run in headless(background) mode? (recommended=No) [No/yes] : ' + bcolors.ENDC)).lower()

    if gui == 'n' or gui == 'no' or gui == '':
        background = False
        threads = int(
            input(bcolors.OKBLUE+'Threads (recommended = 5): ' + bcolors.ENDC))
    else:
        background = True
        threads = int(
            input(bcolors.OKBLUE+'Threads (recommended = 10): ' + bcolors.ENDC))

    handle_proxy = str(input(
        bcolors.WARNING + "Select proxy type (HTTPS / SOCKS5) [1/2] : " + bcolors.ENDC)).lower()

    if handle_proxy == '1' or handle_proxy == 'https':
        proxy_type = 'https'
    elif handle_proxy == '2' or handle_proxy == 'socks5' or handle_proxy == 'socks':
        proxy_type = 'socks5'
    else:
        print('Input 1 for HTTPS or input 2 for SOCKS5 proxy type')
        sys.exit()

    proxy_list = load_proxy()
    proxy_list = list(set(proxy_list))  # removing duplicate proxies
    proxy_list = list(filter(None, proxy_list))  # removing empty proxies

    total_proxies = len(proxy_list)
    print(bcolors.OKCYAN + f'Total proxies : {total_proxies}' + bcolors.ENDC)

    check = -1
    while len(view) < views:
        try:
            check += 1
            if check == 0:
                main()
            else:
                sleeping()
                print(bcolors.WARNING +
                      f'Total Checked : {check} times' + bcolors.ENDC)
                main()
        except KeyboardInterrupt:
            sys.exit()
