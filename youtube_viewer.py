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
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import choice, randint, uniform
from time import gmtime, sleep, strftime

import requests
import undetected_chromedriver as uc
from fake_headers import Headers
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        ElementNotInteractableException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver

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

proxy = None
driver = None
status = None

view = []
duration_dict = {}
checked = {}
REFERER = ['https://www.youtube.com/', 'https://github.com/', 'https://www.facebook.com/', 'https://www.google.com/',
           'https://m.facebook.com/', 'https://yandex.com/', 'https://www.yahoo.com/', 'https://www.bing.com/', 'https://duckduckgo.com/']

VIEWPORT = ['2560,1440', '1920,1080', '1440,900',
            '1536,864', '1366,768', '1280,1024', '1024,768']

print(bcolors.WARNING + 'Getting Chrome Driver...' + bcolors.ENDC)

OSNAME = platform.system()

"""
Getting Chrome version code has been taken from 
https://github.com/yeongbin-jo/python-chromedriver-autoinstaller
Thanks goes to him.
"""
if OSNAME == 'Linux':
    OSNAME = 'lin'
    with subprocess.Popen(['google-chrome', '--version'], stdout=subprocess.PIPE) as proc:
        version = proc.stdout.read().decode('utf-8').replace('Google Chrome', '').strip()
elif OSNAME == 'Darwin':
    OSNAME = 'mac'
    process = subprocess.Popen(
        ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stdout=subprocess.PIPE)
    version = process.communicate()[0].decode(
        'UTF-8').replace('Google Chrome', '').strip()
elif OSNAME == 'Windows':
    OSNAME = 'win'
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
              f'{len(proxy)} proxies gathered from {link}' + bcolors.ENDC)

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


def check_proxy(agent, proxy, proxy_type):
    if category == 'f':
        headers = {
            'User-Agent': f'{agent}',
        }
        if proxy_type == 'https':
            proxyDict = {
                "http": f"http://{proxy}",
                "https": f"https://{proxy}",
            }
        else:
            proxyDict = {
                "http": f"{proxy_type}://{proxy}",
                "https": f"{proxy_type}://{proxy}",
            }
        response = requests.get(
            'https://www.youtube.com/', headers=headers, proxies=proxyDict, timeout=30)
        status = response.status_code

    else:
        status = 200

    return status


def get_driver(agent, proxy, proxy_type):
    options = webdriver.ChromeOptions()
    options.headless = background
    options.add_argument(f"--window-size={choice(VIEWPORT)}")
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
                'http': f'http://{proxy}',
                'https': f'https://{proxy}',
            }
        }
    else:
        sw_options = {
            'proxy': {
                'http': f'{proxy_type}://{proxy}',
                'https': f'{proxy_type}://{proxy}',
            }
        }

    driver = webdriver.Chrome(options=options, seleniumwire_options=sw_options)

    return driver


def bypass_consent(driver):
    try:
        consent = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@type='submit' and @value='I agree']")))
        consent.submit()
    except:
        try:
            consent = driver.find_element_by_css_selector(
                'button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.IIdkle')
            consent.click()
        except:
            pass


def search_video(driver, query):
    find_video = WebDriverWait(driver, 80).until(EC.element_to_be_clickable(
        (By.XPATH, f'//*[@title="{query[1]}"]')))
    find_video.click()


def bypass_agree(driver):
    frame = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.ID, "iframe")))
    driver._switch_to.frame(frame)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.ID, "introAgreeButton"))).click()
    driver.switch_to.default_content()


def bypass_signin(driver):
    sleep(1)
    nothanks = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "style-scope.yt-button-renderer.style-text.size-small")))
    nothanks.click()
    sleep(randint(1, 5))
    bypass_agree(driver)


def check_state(driver):
    try:
        driver.find_element_by_css_selector('[title^="Pause (k)"]')
    except:
        try:
            driver.find_element_by_css_selector('[title^="Play (k)"]').click()
        except:
            driver.find_element_by_css_selector(
                'button.ytp-large-play-button.ytp-button').send_keys(Keys.ENTER)


def sleeping():
    sleep(30)


def main_viewer(proxy_type, proxy, position):
    try:

        checked[position] = None

        header = Headers(
            browser="chrome",
            os=OSNAME,
            headers=False
        ).generate()
        agent = header['User-Agent']

        status = check_proxy(agent, proxy, proxy_type)

        if status == 200:
            try:
                print(bcolors.OKBLUE + f"Tried {position+1} | " +
                      bcolors.OKGREEN + f"{proxy} | {proxy_type} --> Good Proxy | Searching for videos..." + bcolors.ENDC)

                driver = get_driver(agent, proxy, proxy_type)

                if position % 2:
                    method = 1
                    url = choice(urls)
                    if 'youtu' in url:
                        def interceptor(request):
                            del request.headers['Referer']
                            request.headers['Referer'] = choice(REFERER)

                        driver.request_interceptor = interceptor
                else:
                    method = 2
                    query = choice(queries)
                    url = f"https://www.youtube.com/results?search_query={query[0].replace(' ', '%20')}"
               
            
                # driver.get('https://ipof.me')
                # sleep(30)
                
                driver.get(url)

                if 'consent' in driver.current_url:
                    print(bcolors.OKBLUE + f"Tried {position+1} | Bypassing consent..." + bcolors.ENDC)
                    bypass_consent(driver)

                try:
                    if method == 1:
                        play = WebDriverWait(driver, 80).until(EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "button.ytp-large-play-button.ytp-button")))
                        play.send_keys(Keys.ENTER)

                    else:
                        search_video(driver, query)

                    bypass_signin(driver)

                except ElementNotInteractableException:
                    try:
                        bypass_signin(driver)
                    except ElementClickInterceptedException:
                        bypass_agree(driver)
                        search_video(driver, query)
                    except:
                        pass

                except ElementClickInterceptedException:
                    bypass_agree(driver)
                    search_video(driver, query)

                except:
                    pass

                check_state(driver)

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
                print(bcolors.OKBLUE + f"Tried {position+1} | " + bcolors.OKGREEN +
                      f"{proxy} --> Video Found : {url} | Watch Duration : {duration} " + bcolors.ENDC)

                check_state(driver)

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
        print(bcolors.OKBLUE + f"Tried {position+1} | " + bcolors.FAIL +
              f"{proxy} | {proxy_type} --> Bad proxy " + bcolors.ENDC)
        checked[position] = proxy_type
        pass


def view_video(position):
    proxy = proxy_list[position]

    if category == 'f':
        main_viewer('https', proxy, position)
        if checked[position] == 'https':
            main_viewer('socks4', proxy, position)
        if checked[position] == 'socks4':
            main_viewer('socks5', proxy, position)

    else:
        main_viewer(proxy_type, proxy, position)


def main():
    pool_number = [i for i in range(total_proxies)]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(view_video, position)
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

    urls = load_url()
    queries = load_search()

    views = int(input(bcolors.OKBLUE + 'Amount of views : ' + bcolors.ENDC))

    category = input(bcolors.WARNING +
                     "What's your proxy category? [F = Free (without user:pass), P = Premium (with user:pass), R = Rotating Proxy] : " + bcolors.ENDC).lower()

    if category == 'f':
        handle_proxy = str(input(
            bcolors.OKBLUE + 'Let YouTube Viewer handle proxies ? [Y/n] : ' + bcolors.ENDC)).lower()

        if handle_proxy == 'y' or handle_proxy == 'yes' or handle_proxy == '':
            proxy_list = gather_proxy()
        else:
            proxy_list = load_proxy()

    elif category == 'p' or category == 'r':
        handle_proxy = str(input(
            bcolors.OKBLUE + "Select proxy type [1 = HTTPS , 2 = SOCKS4, 3 = SOCKS5] : " + bcolors.ENDC)).lower()

        if handle_proxy == '1':
            proxy_type = 'https'
        elif handle_proxy == '2':
            proxy_type = 'socks4'
        elif handle_proxy == '3':
            proxy_type = 'socks5'
        else:
            print('Please input 1 for HTTPS, 2 for SOCKS4 and 3 for SOCKS5 proxy type')
            sys.exit()

        if category == 'r':
            proxy = input(bcolors.OKBLUE +
                          'Enter your Rotating Proxy service Main Gateway : ' + bcolors.ENDC)
            proxy_list = [proxy]
            proxy_list = proxy_list * 100000
        else:
            proxy_list = load_proxy()

    else:
        print('Please input F for Free, P for Premium and R for Rotating proxy')
        sys.exit()

    if category != 'r':
        proxy_list = list(set(proxy_list))  # removing duplicate proxies
        proxy_list = list(filter(None, proxy_list))  # removing empty proxies

    total_proxies = len(proxy_list)
    print(bcolors.OKCYAN + f'Total proxies : {total_proxies}' + bcolors.ENDC)

    gui = str(input(
        bcolors.WARNING + 'Do you want to run in headless(background) mode? (recommended=No) [No/yes] : ' + bcolors.ENDC)).lower()

    if gui == 'n' or gui == 'no' or gui == '':
        background = False
    else:
        background = True

    threads = int(
        input(bcolors.OKBLUE+'Threads (recommended = 5): ' + bcolors.ENDC))

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
