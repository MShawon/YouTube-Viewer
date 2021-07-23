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
import json
import logging
import os
import platform
import shutil
import sqlite3
import subprocess
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import closing
from datetime import datetime
from random import choice, choices, randint, uniform
from time import gmtime, sleep, strftime

import requests
import undetected_chromedriver as uc
from fake_headers import Headers, browsers
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import website
from config import create_config

log = logging.getLogger('werkzeug')
log.disabled = True

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

SCRIPT_VERSION = '1.4.9'

proxy = None
driver = None
status = None
server_running = False

view = []
duration_dict = {}
checked = {}
console = []
completed = 0

WEBRTC = os.path.join('extension', 'webrtc_control.zip')
ACTIVE = os.path.join('extension', 'always_active.zip')
FINGERPRINT = os.path.join('extension', 'fingerprint_defender.zip')
TIMEZONE = os.path.join('extension', 'spoof_timezone.zip')
DATABASE = 'database.db'
DATABASE_BACKUP = 'database_backup.db'

WIDTH = 0
VIEWPORT = ['2560,1440', '1920,1080', '1440,900',
            '1536,864', '1366,768', '1280,1024', '1024,768']

CHROME = ['{8A69D345-D564-463c-AFF1-A69D9E530F96}',
          '{8237E44A-0054-442C-B6B6-EA0509993955}',
          '{401C381F-E0DE-4B85-8BD8-3F3F14FBDA57}',
          '{4ea16ac7-fd5a-47c3-875b-dbf4a2008c20}']

website.console = console
website.database = DATABASE

link = 'https://gist.githubusercontent.com/MShawon/29e185038f22e6ac5eac822a1e422e9d/raw/versions.txt'

output = requests.get(link, timeout=60).text
chrome_versions = output.split('\n')

browsers.chrome_ver += chrome_versions


class UrlsError(Exception):
    pass


class SearchError(Exception):
    pass


class CaptchaError(Exception):
    pass


class QueryError(Exception):
    pass


def timestamp():
    date_fmt = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    return bcolors.OKGREEN + f'[{date_fmt}] '


def check_update():
    api_url = 'https://api.github.com/repos/MShawon/YouTube-Viewer/releases/latest'
    response = requests.get(api_url, timeout=30)

    RELEASE_VERSION = response.json()['tag_name']

    if SCRIPT_VERSION != RELEASE_VERSION:
        print(bcolors.BOLD + 'Update Available!!! ' +
              f'YouTube Viewer version {SCRIPT_VERSION} needs to update to {RELEASE_VERSION} version.' + bcolors.ENDC)


def download_driver():
    OSNAME = platform.system()

    print(bcolors.WARNING + 'Getting Chrome Driver...' + bcolors.ENDC)

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
        version = None
        try:
            process = subprocess.Popen(
                ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
            )
            version = process.communicate()[0].decode(
                'UTF-8').strip().split()[-1]
        except:
            for i in CHROME:
                for j in ['opv', 'pv']:
                    try:
                        command = [
                            'reg', 'query', f'HKEY_LOCAL_MACHINE\\Software\\Google\\Update\\Clients\\{i}', '/v', f'{j}', '/reg:32']
                        process = subprocess.Popen(
                            command,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
                        )
                        version = process.communicate()[0].decode(
                            'UTF-8').strip().split()[-1]
                    except:
                        pass

        if not version:
            version = input(bcolors.WARNING +
                            'Please input your google chrome version (91.0.4472.114) : ' + bcolors.ENDC)
    else:
        print('{} OS is not supported.'.format(OSNAME))
        sys.exit()

    major_version = version.split('.')[0]

    uc.TARGET_VERSION = major_version

    uc.install()

    return OSNAME


def create_database():
    with closing(sqlite3.connect(DATABASE)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS
            statistics (date TEXT, view INTEGER)""")

            connection.commit()

    try:
        # remove previous backup if exists
        os.remove(DATABASE_BACKUP)
    except:
        pass

    try:
        # backup latest database
        shutil.copy(DATABASE, DATABASE_BACKUP)
    except:
        pass


def update_database():
    today = str(datetime.today().date())
    with closing(sqlite3.connect(DATABASE, timeout=threads*10)) as connection:
        with closing(connection.cursor()) as cursor:
            try:
                cursor.execute(
                    "SELECT view FROM statistics WHERE date = ?", (today,))
                previous_count = cursor.fetchone()[0]
                cursor.execute("UPDATE statistics SET view = ? WHERE date = ?",
                               (previous_count + 1, today))
            except:
                cursor.execute(
                    "INSERT INTO statistics VALUES (?, ?)", (today, 0),)

            connection.commit()


def create_html(text_dict):
    global console

    if len(console) > 50:
        console.pop(0)

    date_fmt = f'<span style="color:#23d18b"> [{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}] </span>'
    str_fmt = ''.join(
        [f'<span style="color:{key}"> {value} </span>' for key, value in text_dict.items()])
    html = date_fmt + str_fmt

    console.append(html)


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
    try:
        filename = 'search.txt'
        load = open(filename, encoding="utf-8")
        loaded = [items.rstrip().strip() for items in load]
        loaded = [[i.strip() for i in items.split('::::')] for items in loaded]
        load.close()

        for lines in loaded:
            search.append(lines)
    except:
        pass

    print(bcolors.OKGREEN +
          f'{len(search)} query loaded from search.txt' + bcolors.ENDC)

    return search


def gather_proxy():
    proxies = []
    print(bcolors.OKGREEN + 'Scraping proxies ...' + bcolors.ENDC)

    link_list = ['https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
                 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
                 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt',
                 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt',
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


def load_proxy(filename):
    proxies = []

    load = open(filename)
    loaded = [items.rstrip().strip() for items in load]
    load.close()

    for lines in loaded:
        if lines.count(':') == 3:
            split = lines.split(':')
            lines = f'{split[2]}:{split[-1]}@{split[0]}:{split[1]}'
        proxies.append(lines)

    return proxies


def check_proxy(agent, proxy, proxy_type):
    if category == 'f':
        headers = {
            'User-Agent': f'{agent}',
        }

        proxy_dict = {
            "http": f"{proxy_type}://{proxy}",
            "https": f"{proxy_type}://{proxy}",
        }
        response = requests.get(
            'https://www.youtube.com/', headers=headers, proxies=proxy_dict, timeout=30)
        status = response.status_code

    else:
        status = 200

    return status


def get_driver(agent, proxy, proxy_type, pluginfile):
    options = webdriver.ChromeOptions()
    options.headless = background
    options.add_argument(f"--window-size={choice(VIEWPORT)}")
    options.add_argument("--log-level=3")
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--lang=en-US")
    options.add_argument(f"user-agent={agent}")
    options.add_argument("--mute-audio")
    options.add_argument('--disable-features=UserAgentClientHint')
    webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {
        'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

    if not background:
        options.add_extension(WEBRTC)
        options.add_extension(FINGERPRINT)
        options.add_extension(TIMEZONE)
        options.add_extension(ACTIVE)

    if auth_required:
        proxy = proxy.replace('@', ':')
        proxy = proxy.split(':')
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (proxy[2], proxy[-1], proxy[0], proxy[1])

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        options.add_extension(pluginfile)

    else:
        options.add_argument(f'--proxy-server={proxy_type}://{proxy}')

    driver = webdriver.Chrome(options=options)

    return driver


def personalization(driver):
    search = driver.find_element_by_xpath(
        f'//button[@aria-label="Turn {choice(["on","off"])} Search customization"]')
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", search)
    search.click()

    history = driver.find_element_by_xpath(
        f'//button[@aria-label="Turn {choice(["on","off"])} YouTube History"]')
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", history)
    history.click()

    ad = driver.find_element_by_xpath(
        f'//button[@aria-label="Turn {choice(["on","off"])} Ad personalization"]')
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", ad)
    ad.click()

    confirm = driver.find_element_by_xpath('//button[@jsname="j6LnYe"]')
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", confirm)
    confirm.click()


def bypass_consent(driver):
    try:
        consent = driver.find_element_by_xpath("//button[@jsname='higCR']")
        driver.execute_script("arguments[0].scrollIntoView();", consent)
        consent.click()
        if 'consent' in driver.current_url:
            personalization(driver)
    except:
        consent = driver.find_element_by_xpath(
            "//input[@type='submit' and @value='I agree']")
        driver.execute_script("arguments[0].scrollIntoView();", consent)
        consent.submit()
        if 'consent' in driver.current_url:
            personalization(driver)


def bypass_signin(driver):
    for _ in range(10):
        sleep(2)
        try:
            nothanks = driver.find_element_by_class_name(
                "style-scope.yt-button-renderer.style-text.size-small")
            nothanks.click()
            sleep(1)
            driver.switch_to.frame(driver.find_element_by_id("iframe"))
            iagree = driver.find_element_by_id('introAgreeButton')
            iagree.click()
            driver.switch_to.default_content()
        except:
            try:
                driver.switch_to.frame(driver.find_element_by_id("iframe"))
                iagree = driver.find_element_by_id('introAgreeButton')
                iagree.click()
                driver.switch_to.default_content()
            except:
                pass


def skip_initial_ad(driver, position, video):
    try:
        video_len = duration_dict[video]
        if video_len > 30:
            skip_ad = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                (By.CLASS_NAME, "ytp-ad-skip-button-container")))

            print(timestamp() + bcolors.OKBLUE +
                  f"Tried {position} | Skipping Ads..." + bcolors.ENDC)

            create_html({"#23d18b": f"Tried {position} | Skipping Ads..."})

            ad_duration = driver.find_element_by_class_name(
                'ytp-time-duration').get_attribute('innerText')
            ad_duration = sum(x * int(t)
                              for x, t in zip([60, 1], ad_duration.split(":")))
            ad_duration = ad_duration * uniform(.01, .1)
            sleep(ad_duration)
            skip_ad.click()
    except:
        pass


def search_video(driver, keyword, video_title):
    i = 0
    try:
        input_keyword = driver.find_element_by_css_selector('input#search')

        for letter in keyword:
            input_keyword.send_keys(letter)
            sleep(uniform(.1, .4))

        method = randint(1, 2)
        if method == 1:
            input_keyword.send_keys(Keys.ENTER)
        else:
            try:
                driver.find_element_by_xpath(
                    '//*[@id="search-icon-legacy"]').click()
            except:
                driver.execute_script(
                    'document.querySelector("#search-icon-legacy").click()')

    except:
        return i

    for i in range(1, 11):
        try:
            section = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
                (By.XPATH, f'//ytd-item-section-renderer[{i}]')))
            find_video = section.find_element_by_xpath(
                f'//*[@title="{video_title}"]')
            driver.execute_script(
                "arguments[0].scrollIntoViewIfNeeded();", find_video)
            sleep(1)
            find_video.click()
            break
        except NoSuchElementException:
            sleep(5)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
                (By.TAG_NAME, 'body'))).send_keys(Keys.CONTROL, Keys.END)

    return i


def play_video(driver):
    try:
        driver.find_element_by_css_selector('[title^="Pause (k)"]')
    except:
        try:
            driver.find_element_by_css_selector(
                'button.ytp-large-play-button.ytp-button').send_keys(Keys.ENTER)
        except:
            try:
                driver.find_element_by_css_selector(
                    '[title^="Play (k)"]').click()
            except:
                driver.execute_script(
                    "document.querySelector('button.ytp-play-button.ytp-button').click()")


def play_music(driver):
    try:
        driver.find_element_by_xpath(
            '//*[@id="play-pause-button" and @title="Pause"]')
    except:
        try:
            driver.find_element_by_xpath(
                '//*[@id="play-pause-button" and @title="Play"]').click()
        except:
            driver.execute_script(
                'document.querySelector("#play-pause-button").click()')


def save_bandwidth(driver):
    try:
        driver.find_element_by_css_selector(
            "button.ytp-button.ytp-settings-button").click()
        driver.find_element_by_xpath(
            "//div[contains(text(),'Quality')]").click()

        random_quality = choices(
            ['144p', '240p', '360p'], cum_weights=(0.7, 0.9, 1.00), k=1)[0]
        quality = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"//span[contains(string(),'{random_quality}')]")))
        driver.execute_script(
            "arguments[0].scrollIntoViewIfNeeded();", quality)
        quality.click()

    except:
        try:
            driver.find_element_by_xpath(
                '//*[@id="container"]/h1/yt-formatted-string').click()
        except:
            pass


def quit_driver(driver, pluginfile):
    try:
        os.remove(pluginfile)
    except:
        pass

    driver.quit()
    status = 400
    return status


def sleeping():
    sleep(5)


def main_viewer(proxy_type, proxy, position):
    try:
        global WIDTH
        global VIEWPORT

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
                print(timestamp() + bcolors.OKBLUE + f"Tried {position} | " + bcolors.OKGREEN +
                      f"{proxy} | {proxy_type} --> Good Proxy | Opening a new driver..." + bcolors.ENDC)

                create_html({"#3b8eea": f"Tried {position} | ",
                             "#23d18b": f"{proxy} | {proxy_type} --> Good Proxy | Opening a new driver..."})

                pluginfile = os.path.join(
                    'extension', f'proxy_auth_plugin{position}.zip')

                url = ''

                if position % 2:
                    try:
                        method = 1
                        url = choice(urls)
                        output = url
                        if 'music.youtube.com' in url:
                            youtube = 'Music'
                        else:
                            youtube = 'Video'
                    except:
                        raise UrlsError

                else:
                    try:
                        method = 2
                        query = choice(queries)
                        keyword = query[0]
                        video_title = query[1]
                        url = "https://www.youtube.com"
                        output = video_title
                        youtube = 'Video'
                    except:
                        url = choice(urls)
                        output = url
                        if 'music.youtube.com' in url:
                            youtube = 'Music'
                        else:
                            raise SearchError

                driver = get_driver(agent, proxy, proxy_type, pluginfile)

                # driver.get('http://httpbin.org/ip')
                # sleep(30)

                sleep(2)

                try:
                    proxy_dict = {
                        "http": f"{proxy_type}://{proxy}",
                        "https": f"{proxy_type}://{proxy}",
                    }
                    location = requests.get(
                        "http://ip-api.com/json", proxies=proxy_dict, timeout=30).json()
                    params = {
                        "latitude": location['lat'],
                        "longitude": location['lon'],
                        "accuracy": randint(20, 100)
                    }
                    driver.execute_cdp_cmd(
                        "Emulation.setGeolocationOverride", params)
                except:
                    pass

                driver.get(url)

                if 'consent' in driver.current_url:
                    print(timestamp() + bcolors.OKBLUE +
                          f"Tried {position} | Bypassing consent..." + bcolors.ENDC)

                    create_html(
                        {"#3b8eea": f"Tried {position} | Bypassing consent..."})

                    bypass_consent(driver)

                if youtube == 'Video':
                    if method == 1:
                        skip_initial_ad(driver, position, output)

                    else:
                        scroll = search_video(driver, keyword, video_title)
                        if scroll == 0:
                            raise CaptchaError
                        elif scroll == 10:
                            raise QueryError
                        else:
                            pass

                        skip_initial_ad(driver, position, output)

                    try:
                        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                            (By.XPATH, '//ytd-player[@id="ytd-player"]')))
                    except:
                        raise CaptchaError

                    play_video(driver)

                    if bandwidth:
                        save_bandwidth(driver)

                    play_video(driver)

                    view_stat = WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                        (By.XPATH, '//span[@class="view-count style-scope ytd-video-view-count-renderer"]'))).text

                else:
                    try:
                        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="player-page"]')))
                    except:
                        raise CaptchaError

                    play_music(driver)

                    view_stat = 'music'

                if WIDTH == 0:
                    WIDTH = driver.execute_script('return screen.width')
                    VIEWPORT = [i for i in VIEWPORT if int(i[:4]) <= WIDTH]

                if 'watching' in view_stat:
                    error = 0
                    while True:
                        view_stat = driver.find_element_by_xpath(
                            '//span[@class="view-count style-scope ytd-video-view-count-renderer"]').text
                        if 'watching' in view_stat:
                            print(timestamp() + bcolors.OKBLUE + f"Tried {position} | " + bcolors.OKGREEN +
                                  f"{proxy} | {output} | " + bcolors.OKCYAN + f"{view_stat} " + bcolors.ENDC)

                            create_html({"#3b8eea": f"Tried {position} | ",
                                         "#23d18b": f"{proxy} | {output} | ", "#29b2d3": f"{view_stat} "})
                        else:
                            error += 1
                        if error == 5:
                            break
                        sleep(60)

                else:
                    try:
                        video_len = duration_dict[output]
                    except KeyError:
                        video_len = 0
                        while video_len == 0:
                            video_len = driver.execute_script(
                                "return document.getElementById('movie_player').getDuration()")

                        duration_dict[output] = video_len

                    video_len = video_len*uniform(minimum, maximum)

                    duration = strftime("%Hh:%Mm:%Ss", gmtime(video_len))
                    print(timestamp() + bcolors.OKBLUE + f"Tried {position} | " + bcolors.OKGREEN +
                          f"{proxy} --> {youtube} Found : {output} | Watch Duration : {duration} " + bcolors.ENDC)

                    create_html({"#3b8eea": f"Tried {position} | ",
                                 "#23d18b": f"{proxy} --> {youtube} Found : {output} | Watch Duration : {duration} "})

                    loop = int(video_len/4)
                    for _ in range(loop):
                        sleep(5)
                        current_time = driver.execute_script(
                            "return document.getElementById('movie_player').getCurrentTime()")
                        if current_time > video_len:
                            break

                view.append(position)

                view_count = len(view)
                print(timestamp() + bcolors.OKCYAN +
                      f'View added : {view_count}' + bcolors.ENDC)

                create_html({"#29b2d3": f'View added : {view_count}'})

                if database:
                    try:
                        update_database()
                    except:
                        pass

                status = quit_driver(driver, pluginfile)

            except UrlsError:
                print(timestamp() + bcolors.FAIL +
                      f"Tried {position} | Your urls.txt is empty!" + bcolors.ENDC)

                create_html(
                    {"#f14c4c": f"Tried {position} | Your urls.txt is empty!"})

                status = 400
                pass

            except SearchError:
                print(timestamp() + bcolors.FAIL +
                      f"Tried {position} | Your search.txt is empty!" + bcolors.ENDC)

                create_html(
                    {"#f14c4c": f"Tried {position} | Your search.txt is empty!"})

                status = 400
                pass

            except CaptchaError:
                print(timestamp() + bcolors.FAIL +
                      f"Tried {position} | Slow internet speed or Stuck at recaptcha! Can't load YouTube..." + bcolors.ENDC)

                create_html(
                    {"#f14c4c": f"Tried {position} | Slow internet speed or Stuck at recaptcha! Can't load YouTube..."})

                status = quit_driver(driver, pluginfile)
                pass

            except QueryError:
                print(timestamp() + bcolors.FAIL +
                      f"Tried {position} | Can't find this [{video_title}] video with this keyword [{keyword}]" + bcolors.ENDC)

                create_html(
                    {"#f14c4c": f"Tried {position} | Can't find this [{video_title}] video with this keyword [{keyword}]"})

                status = quit_driver(driver, pluginfile)
                pass

            except Exception as e:
                *_, exc_tb = sys.exc_info()
                print(timestamp() + bcolors.FAIL +
                      f"Tried {position} | Line : {exc_tb.tb_lineno} | " + str(e) + bcolors.ENDC)

                create_html(
                    {"#f14c4c": f"Tried {position} | Line : {exc_tb.tb_lineno} | " + str(e)})

                status = quit_driver(driver, pluginfile)
                pass

    except:
        print(timestamp() + bcolors.OKBLUE + f"Tried {position} | " +
              bcolors.FAIL + f"{proxy} | {proxy_type} --> Bad proxy " + bcolors.ENDC)

        create_html({"#3b8eea": f"Tried {position} | ",
                     "#f14c4c": f"{proxy} | {proxy_type} --> Bad proxy "})

        checked[position] = proxy_type
        pass


def view_video(position):
    global completed
    global server_running

    if position == 0:
        if api and not server_running:
            server_running = True
            website.start_server(host=host, port=port)

    elif position == total_proxies - 1:
        if api and server_running:
            while completed != total_proxies - 2:
                sleep(5)

            completed = -2
            server_running = False
            requests.post(f'http://127.0.0.1:{port}/shutdown')

    else:
        proxy = proxy_list[position]

        if proxy_type:
            main_viewer(proxy_type, proxy, position)
        else:
            main_viewer('http', proxy, position)
            if checked[position] == 'http':
                main_viewer('socks4', proxy, position)
            if checked[position] == 'socks4':
                main_viewer('socks5', proxy, position)


def main():
    global completed
    pool_number = [i for i in range(total_proxies)]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(view_video, position)
                   for position in pool_number]

        try:
            for future in as_completed(futures):
                completed += 1
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

    check_update()
    OSNAME = download_driver()
    create_database()
    urls = load_url()
    queries = load_search()

    if os.path.isfile('config.json'):
        with open('config.json', 'r') as openfile:
            config = json.load(openfile)

        if len(config) == 9:
            print(json.dumps(config, indent=4))
            previous = str(input(
                bcolors.OKBLUE + 'Config file exists! Do you want to continue with previous saved preferences ? [Yes/No] : ' + bcolors.ENDC)).lower()
            if previous == 'n' or previous == 'no':
                create_config()
            else:
                pass
        else:
            print(bcolors.FAIL + 'Previous config file is not compatible with the latest script! Create a new one...' + bcolors.ENDC)
            create_config()
    else:
        create_config()

    with open('config.json', 'r') as openfile:
        config = json.load(openfile)

    api = config["http_api"]["enabled"]
    host = config["http_api"]["host"]
    port = config["http_api"]["port"]
    database = config["database"]
    views = config["views"]
    minimum = config["minimum"] / 100
    maximum = config["maximum"] / 100
    category = config["proxy"]["category"]
    proxy_type = config["proxy"]["proxy_type"]
    filename = config["proxy"]["filename"]
    auth_required = config["proxy"]["authentication"]
    background = config["background"]
    bandwidth = config["bandwidth"]
    threads = config["threads"]

    if auth_required and background:
        print(bcolors.FAIL +
              "Premium proxy needs extension to work. Chrome doesn't support extension in Headless mode." + bcolors.ENDC)
        print(bcolors.WARNING +
              f"Either use proxy without username & password or disable headless mode" + bcolors.ENDC)
        sys.exit()

    if filename:
        if category == 'r':
            proxy_list = [filename]
            proxy_list = proxy_list * 100000
        else:
            proxy_list = load_proxy(filename)
    else:
        proxy_list = gather_proxy()

    proxy_list = list(filter(None, proxy_list))  # removing empty lines

    total_proxies = len(proxy_list)
    if category != 'r':
        print(bcolors.OKCYAN +
              f'Total proxies : {total_proxies}' + bcolors.ENDC)

    proxy_list.insert(0, 'dummy')
    proxy_list.append('dummy')

    total_proxies += 2

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
