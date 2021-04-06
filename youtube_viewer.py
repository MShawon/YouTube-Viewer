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
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import choice, randint, uniform
from time import gmtime, sleep, strftime

import requests
import undetected_chromedriver as uc
from fake_useragent import UserAgent, UserAgentError
from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        ElementNotInteractableException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
checked = {}


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


def gather_proxy():
    proxies = []
    print(bcolors.OKGREEN + 'Scraping proxies ...' + bcolors.ENDC)

    link_list = ['https://www.proxyscan.io/download?type=http',
                 'https://www.proxyscan.io/download?type=https',
                 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
                 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
                 'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt',
                 'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt']

    for link in link_list:
        response = requests.get(link)
        output = response.content.decode()
        proxy = output.split('\n')
        proxies = proxies + proxy
        print(bcolors.OKGREEN +
              f'{proxy} proxies gathered from {link}' + bcolors.ENDC)

    return proxies


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
    sleep(1)
    nothanks = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "style-scope.yt-button-renderer.style-text.size-small")))
    nothanks.click()
    sleep(randint(1, 5))
    bypassAgree(driver)


def sleeping():
    sleep(30)


def searchVideo(driver, query):
    find_video = WebDriverWait(driver, 80).until(EC.element_to_be_clickable(
        (By.XPATH, f'//*[@title="{query[1]}"]')))
    find_video.click()


def checkState(driver):
    try:
        driver.find_element_by_css_selector('[title^="Pause (k)"]')
    except:
        try:
            driver.find_element_by_css_selector('[title^="Play (k)"]').click()
        except:
            driver.find_element_by_css_selector(
                'button.ytp-large-play-button.ytp-button').send_keys(Keys.ENTER)


def mainViewer(type1, type2, PROXY, position):
    try:
        
        checked[position] = None

        agent = ua.chrome
        while OSNAME not in agent:
            agent = ua.chrome

        headers = {
            'User-Agent': f'{agent}',
        }
        proxyDict = {
            "http": f"{type1}://"+PROXY,
            "https": f"{type2}://"+PROXY,
        }

        response = requests.get(
            'https://www.youtube.com/', headers=headers, proxies=proxyDict, timeout=30)
        status = response.status_code

        if status == 200:
            try:
                print(bcolors.OKBLUE + f"Tried {position+1} |" +
                      bcolors.OKGREEN + f'{PROXY} | {type2} --> Good Proxy | Searching for videos...' + bcolors.ENDC)

                if position % 2:
                    method = 1
                    url = choice(urls)
                else:
                    method = 2
                    query = choice(queries)
                    url = f"https://www.youtube.com/results?search_query={query[0].replace(' ', '%20')}"

                options = webdriver.ChromeOptions()
                options.headless = background
                viewport = ['2560,1440', '1920,1080', '1440,900',
                            '1536,864', '1366,768', '1280,1024', '1024,768']
                options.add_argument(
                    f"--window-size={choice(viewport)}")
                options.add_argument("--log-level=3")
                options.add_experimental_option(
                    "excludeSwitches", ["enable-automation", "enable-logging"])
                options.add_experimental_option(
                    'useAutomationExtension', False)
                options.add_argument(f"user-agent={agent}")
                webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {
                    'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

                if type1 == 'http':
                    webdriver.DesiredCapabilities.CHROME['proxy'] = {
                        "httpProxy": PROXY,
                        "sslProxy": PROXY,

                        "proxyType": "MANUAL",
                    }
                else:
                    options.add_argument(f'--proxy-server={type1}://' + PROXY)

                driver = webdriver.Chrome(options=options)

                driver.get(url)

                try:
                    consent = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
                        (By.XPATH, "//input[@type='submit' and @value='I agree']")))
                    consent.submit()
                except:
                    try:
                        consent = driver.find_element_by_css_selector(
                            'button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.IIdkle')
                        consent.click()
                    except:
                        pass
                    
                try:
                    if method == 1:
                        play = WebDriverWait(driver, 80).until(EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "button.ytp-large-play-button.ytp-button")))
                        play.send_keys(Keys.ENTER)

                    else:
                        searchVideo(driver, query)

                    bypassSignIn(driver)

                except ElementNotInteractableException:
                    try:
                        bypassSignIn(driver)
                    except ElementClickInterceptedException:
                        bypassAgree(driver)
                        searchVideo(driver, query)
                    except:
                        pass

                except ElementClickInterceptedException:
                    bypassAgree(driver)
                    searchVideo(driver, query)

                except:
                    pass

                checkState(driver)

                try:
                    video_len = duration_dict[url]
                except KeyError:
                    video_len = 0
                    WebDriverWait(driver, 80).until(
                        EC.element_to_be_clickable((By.ID, 'movie_player')))

                    while video_len == 0:
                        video_len = driver.execute_script(
                            "return document.getElementById('movie_player').getDuration()")

                    duration_dict[url] = video_len

                # Randomizing watch duration between 85% to 95% of total video duration
                # to avoid pattern and youtube next suggested video
                video_len = video_len*uniform(.85, .95)

                duration = strftime("%Hh:%Mm:%Ss", gmtime(video_len))
                print(bcolors.OKBLUE + f"Tried {position+1} |" + bcolors.OKGREEN +
                    f' {PROXY} --> Video Found : {url} | Watch Duration : {duration} ' + bcolors.ENDC)

                checkState(driver)

                sleep(video_len)
                driver.quit()

                view.append(position)
                print(bcolors.OKCYAN +
                      f'View added : {len(view)}' + bcolors.ENDC)

                status = 400

            except Exception as e:
                *_, exc_tb = sys.exc_info()
                print(bcolors.FAIL + f"Tried {position+1} | Line : {exc_tb.tb_lineno} | " +
                    str(e) + bcolors.ENDC)
                driver.quit()
                status = 400
                pass

    except:
        print(bcolors.OKBLUE + f"Tried {position+1} |" + bcolors.FAIL +
              f' {PROXY} | {type2} --> Bad proxy ' + bcolors.ENDC)
        checked[position] = type2
        pass


def viewVideo(position):
    PROXY = proxy_list[position]

    mainViewer('http', 'https', PROXY, position)
    if checked[position] == 'https':
        mainViewer('socks4', 'socks4', PROXY, position)
    if checked[position] == 'socks4':
        mainViewer('socks5', 'socks5', PROXY, position)


def main():
    pool_number = [i for i in range(total_proxies)]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(viewVideo, position)
                   for position in pool_number]

        try:
            for future in as_completed(futures):
                if len(view) == views:
                    print(
                        bcolors.WARNING + f'Amount of views added : {views} | Stopping program...' + bcolors.ENDC)
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
        bcolors.OKBLUE + 'Let YouTube Viewer handle proxies ? [Y/n] : ' + bcolors.ENDC)).lower()

    if handle_proxy == 'y' or handle_proxy == 'yes' or handle_proxy == '':
        proxy_list = gather_proxy()
    else:
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
