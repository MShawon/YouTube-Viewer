import concurrent.futures.thread
import os
import platform
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from fake_useragent import UserAgent, UserAgentError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
    agent_link = 'https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt'
    response = requests.get(agent_link).content
    ua = response.decode().split('\n')
    ua = list(filter(None, ua))

PROXY = None
driver = None
status = None
driver_path = None

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
          '{} url loaded from urls.txt'.format(len(links)) + bcolors.ENDC)

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
          '{} query loaded from search.txt'.format(len(search)) + bcolors.ENDC)

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
              '{} proxies gathered from {}'.format(len(proxy), link) + bcolors.ENDC)

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


def sleeping():
    time.sleep(30)


def viewVideo(position):
    try:
        '''
        To reduce memory consumption proxy will be checked by request module
        without opening any chrome instances.
        '''
        PROXY = proxy_list[position]
        headers = {
            'User-Agent': '{}'.format(ua.random),
        }
        proxyDict = {
            "http": "http://"+PROXY,
            "https": "https://"+PROXY,
            "ftp": "ftp://"+PROXY,
        }

        response = requests.get(
            'https://www.youtube.com/', headers=headers, proxies=proxyDict, timeout=30)
        status = response.status_code

        if status == 200:
            try:
                print(bcolors.OKBLUE + "Tried {} |".format(position) +
                      bcolors.OKGREEN + '{} --> Good Proxy | Searching for videos...'.format(PROXY) + bcolors.ENDC)

                if position % 2:
                    method = 1
                    url = random.choice(urls)
                else:
                    method = 2
                    query = random.choice(queries)
                    url = f"https://www.youtube.com/results?search_query={query[0].replace(' ', '%20')}"

                options = webdriver.ChromeOptions()
                options.add_experimental_option(
                    'excludeSwitches', ['enable-logging'])
                options.headless = True
                options.add_argument("--log-level=3")
                options.add_argument("user-agent={}".format(ua.random))
                webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {
                    'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
                webdriver.DesiredCapabilities.CHROME['proxy'] = {
                    "httpProxy": PROXY,
                    "ftpProxy": PROXY,
                    "sslProxy": PROXY,

                    "proxyType": "MANUAL",
                }

                driver = webdriver.Chrome(
                    executable_path=driver_path, options=options)

                driver.get(url)

                if method == 1:
                    play = WebDriverWait(driver, 50).until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "button.ytp-large-play-button.ytp-button")))
                    play.send_keys(Keys.ENTER)

                else:
                    find_video = WebDriverWait(driver, 50).until(EC.element_to_be_clickable(
                        (By.XPATH, f'//*[@title="{query[1]}"]')))
                    find_video.click()

                try:
                    video_len = duration_dict[url]
                except KeyError:
                    WebDriverWait(driver, 50).until(
                        EC.element_to_be_clickable((By.ID, 'movie_player')))
                        
                    video_len = driver.execute_script(
                        "return document.getElementById('movie_player').getDuration()")

                    duration_dict[url] = video_len

                # Randomizing watch duration between 85% to 95% of total video duration
                # to avoid pattern and youtube next suggested video
                video_len = video_len*random.uniform(.85, .95)

                duration = time.strftime("%Hh:%Mm:%Ss", time.gmtime(video_len))
                print(bcolors.OKBLUE + "Tried {} |".format(position) + bcolors.OKGREEN +
                      ' {} --> Video Found : {} | Watch Duration : {} '.format(PROXY, url, duration) + bcolors.ENDC)

                time.sleep(video_len)
                driver.quit()

                view.append(position)
                print(bcolors.OKCYAN +
                      'View added : {}'.format(len(view)) + bcolors.ENDC)
                status = 400

            except Exception as e:
                print(bcolors.FAIL + "Tried {} |".format(position) +
                      str(e) + bcolors.ENDC)
                driver.quit()
                status = 400
                pass

    except:
        print(bcolors.OKBLUE + "Tried {} |".format(position) + bcolors.FAIL +
              ' {} --> Bad proxy '.format(PROXY) + bcolors.ENDC)
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
                        bcolors.WARNING + 'Amount of views added : {} | Stopping program...But this will take some time to close all threads.'.format(views) + bcolors.ENDC)
                    executor._threads.clear()
                    concurrent.futures.thread._threads_queues.clear()
                    break
                future.result()

        except KeyboardInterrupt:
            executor._threads.clear()
            concurrent.futures.thread._threads_queues.clear()


if __name__ == '__main__':

    OSNAME = platform.system()
    if OSNAME == 'Windows':
        driver_path = 'chromedriver_win32/chromedriver.exe'
    elif OSNAME == 'Linux':
        driver_path = 'chromedriver_linux64/chromedriver'
    else:
        print('{} OS is not supported.'.format(OSNAME))
        sys.exit()

    urls = load_url()
    queries = load_search()

    views = int(input(bcolors.OKBLUE + 'Amount of views : ' + bcolors.ENDC))

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
    print(bcolors.OKCYAN + 'Total proxies : {}'.format(total_proxies) + bcolors.ENDC)

    check = 0
    while len(view) < views:
        try:
            check += 1
            if check == 1:
                main()
            else:
                sleeping()
                print(bcolors.WARNING +
                      'Total Checked : {} times'.format(check) + bcolors.ENDC)
                main()
        except KeyboardInterrupt:
            sys.exit()
