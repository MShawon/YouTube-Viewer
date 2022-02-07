"""
MIT License

Copyright (c) 2022 MShawon

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
import io
import json
import logging
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import gmtime, sleep, strftime, time

from fake_headers import Headers, browsers
from undetected_chromedriver.patcher import Patcher

from youtubeviewer import website
from youtubeviewer.config import create_config
from youtubeviewer.database import *
from youtubeviewer.download_driver import *
from youtubeviewer.basics import *
from youtubeviewer.load_files import *
from youtubeviewer.proxies import *

log = logging.getLogger('werkzeug')
log.disabled = True

os.system("")

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

SCRIPT_VERSION = '1.7.0'

proxy = None
driver = None
status = None
start_time = None
server_running = False

urls = []
queries = []
suggested = []

hash_urls = None
hash_queries = None

driver_list = []
view = []
duration_dict = {}
checked = {}
console = []
threads = 0

cwd = os.getcwd()
patched_drivers = os.path.join(cwd, 'patched_drivers')
config_path = os.path.join(cwd, 'config.json')

DATABASE = os.path.join(cwd, 'database.db')
DATABASE_BACKUP = os.path.join(cwd, 'database_backup.db')


width = 0
viewports = ['2560,1440', '1920,1080', '1440,900',
             '1536,864', '1366,768', '1280,1024', '1024,768']

REFERERS = ['https://search.yahoo.com/', 'https://duckduckgo.com/', 'https://www.google.com/',
            'https://www.bing.com/', 'https://t.co/', '']

website.console = console
website.database = DATABASE


class UrlsError(Exception):
    pass


class SearchError(Exception):
    pass


class CaptchaError(Exception):
    pass


class QueryError(Exception):
    pass


def monkey_patch_exe(self):
    linect = 0
    replacement = self.gen_random_cdc()
    replacement = f"  var key = '${replacement.decode()}_';\n".encode()
    with io.open(self.executable_path, "r+b") as fh:
        for line in iter(lambda: fh.readline(), b""):
            if b"var key = " in line:
                fh.seek(-len(line), 1)
                fh.write(replacement)
                linect += 1
        return linect


Patcher.patch_exe = monkey_patch_exe


def timestamp():
    date_fmt = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    return bcolors.OKGREEN + f'[{date_fmt}] '


def update_chrome_version():
    link = 'https://gist.githubusercontent.com/MShawon/29e185038f22e6ac5eac822a1e422e9d/raw/versions.txt'

    output = requests.get(link, timeout=60).text
    chrome_versions = output.split('\n')

    browsers.chrome_ver = chrome_versions


def check_update():
    api_url = 'https://api.github.com/repos/MShawon/YouTube-Viewer/releases/latest'
    response = requests.get(api_url, timeout=30)

    RELEASE_VERSION = response.json()['tag_name']

    if SCRIPT_VERSION != RELEASE_VERSION:
        print(bcolors.OKCYAN + '#'*100 + bcolors.ENDC)
        print(bcolors.OKCYAN + 'Update Available!!! ' +
              f'YouTube Viewer version {SCRIPT_VERSION} needs to update to {RELEASE_VERSION} version.' + bcolors.ENDC)

        try:
            notes = response.json()['body'].split('SHA256')[0].split('\r\n')
            for note in notes:
                if note:
                    print(bcolors.HEADER + note + bcolors.ENDC)
        except:
            pass
        print(bcolors.OKCYAN + '#'*100 + '\n' + bcolors.ENDC)


def create_html(text_dict):
    global console

    if len(console) > 50:
        console.pop(0)

    date_fmt = f'<span style="color:#23d18b"> [{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}] </span>'
    str_fmt = ''.join(
        [f'<span style="color:{key}"> {value} </span>' for key, value in text_dict.items()])
    html = date_fmt + str_fmt

    console.append(html)


def detect_file_change():
    global hash_urls, hash_queries, urls, queries, suggested

    new_hash = get_hash("urls.txt")
    if new_hash != hash_urls:
        hash_urls = new_hash
        urls = load_url()
        suggested = []

    new_hash = get_hash("search.txt")
    if new_hash != hash_queries:
        hash_queries = new_hash
        queries = load_search()
        suggested = []


def features(driver):
    bypass_popup(driver)

    bypass_other_popup(driver)

    play_video(driver)

    if bandwidth:
        save_bandwidth(driver)

    change_playback_speed(driver, playback_speed)


def control_player(driver, output, position, proxy, youtube):
    current_url = driver.current_url
    if not output:
        output = driver.title[:-10]

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

    video_id = driver.find_element(
        By.XPATH, '//*[@id="page-manager"]/ytd-watch-flexy').get_attribute('video-id')
    if video_id not in suggested:
        suggested.append(video_id)

    loop = int(video_len/4)
    for _ in range(loop):
        sleep(5)
        current_time = driver.execute_script(
            "return document.getElementById('movie_player').getCurrentTime()")

        if youtube == 'Video':
            play_video(driver)
            random_command(driver)
        elif youtube == 'Music':
            play_music(driver)

        if current_time > video_len or driver.current_url != current_url:
            break

    return current_url


def quit_driver(driver, pluginfile):
    try:
        driver_list.remove(driver)
    except:
        pass

    driver.quit()

    try:
        os.remove(pluginfile)
    except:
        pass

    status = 400
    return status


def sleeping():
    sleep(5)


def main_viewer(proxy_type, proxy, position):
    try:
        global width, viewports

        detect_file_change()

        checked[position] = None

        header = Headers(
            browser="chrome",
            os=osname,
            headers=False
        ).generate()
        agent = header['User-Agent']

        url = ''

        if position % 2:
            try:
                method = 1
                url = choice(urls)
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
                youtube = 'Video'
            except:
                url = choice(urls)
                if 'music.youtube.com' in url:
                    youtube = 'Music'
                else:
                    raise SearchError

        if category == 'r' and proxy_api:
            proxies = scrape_api(link=proxy)
            proxy = choice(proxies)

        status = check_proxy(category, agent, proxy, proxy_type)

        if status == 200:
            try:
                print(timestamp() + bcolors.OKBLUE + f"Tried {position} | " + bcolors.OKGREEN +
                      f"{proxy} | {proxy_type.upper()} | Good Proxy | Opening a new driver..." + bcolors.ENDC)

                create_html({"#3b8eea": f"Tried {position} | ",
                             "#23d18b": f"{proxy} | {proxy_type.upper()} | Good Proxy | Opening a new driver..."})

                patched_driver = os.path.join(
                    patched_drivers, f'chromedriver_{position%threads}{exe_name}')

                try:
                    Patcher(executable_path=patched_driver).patch_exe()
                except:
                    pass

                pluginfile = os.path.join(
                    'extension', f'proxy_auth_plugin{position}.zip')

                factor = int(threads/6)
                sleep_time = int((str(position)[-1])) * factor
                sleep(sleep_time)

                driver = get_driver(background, viewports, agent, auth_required,
                                    patched_driver, proxy, proxy_type, pluginfile)

                driver_list.append(driver)

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

                referer = choice(REFERERS)
                if referer:
                    if method == 2 and 't.co/' in referer:
                        driver.get(url)
                    else:
                        driver.get(referer)
                        if 'consent.yahoo.com' in driver.current_url:
                            try:
                                consent = driver.find_element(
                                    By.XPATH, "//button[@name='agree']")
                                driver.execute_script(
                                    "arguments[0].scrollIntoView();", consent)
                                consent.click()
                                driver.get(referer)
                            except:
                                pass
                        driver.execute_script(
                            "window.location.href = '{}';".format(url))

                    print(timestamp() + bcolors.OKBLUE +
                          f"Tried {position} | Referer used : {referer}" + bcolors.ENDC)

                    create_html(
                        {"#3b8eea": f"Tried {position} | Referer used : {referer}"})

                else:
                    driver.get(url)

                if 'consent' in driver.current_url:
                    print(timestamp() + bcolors.OKBLUE +
                          f"Tried {position} | Bypassing consent..." + bcolors.ENDC)

                    create_html(
                        {"#3b8eea": f"Tried {position} | Bypassing consent..."})

                    bypass_consent(driver)

                output = driver.title[:-10]

                if youtube == 'Video':
                    if method == 1:
                        skip_initial_ad(driver, output, duration_dict)

                    else:
                        scroll = search_video(driver, keyword, video_title)
                        if scroll == 0:
                            raise CaptchaError
                        elif scroll == 10:
                            raise QueryError
                        else:
                            pass

                        skip_initial_ad(driver, output, duration_dict)

                    try:
                        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                            (By.XPATH, '//ytd-player[@id="ytd-player"]')))
                    except:
                        raise CaptchaError

                    features(driver)

                    view_stat = WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                        (By.XPATH, '//span[@class="view-count style-scope ytd-video-view-count-renderer"]'))).text

                else:
                    try:
                        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                            (By.XPATH, '//*[@id="player-page"]')))
                    except:
                        raise CaptchaError

                    bypass_popup(driver)

                    play_music(driver)

                    view_stat = 'music'

                if width == 0:
                    width = driver.execute_script('return screen.width')
                    viewports = [i for i in viewports if int(i[:4]) <= width]

                if 'watching' in view_stat:
                    error = 0
                    while True:
                        view_stat = driver.find_element(
                            By.XPATH, '//span[@class="view-count style-scope ytd-video-view-count-renderer"]').text
                        if 'watching' in view_stat:
                            print(timestamp() + bcolors.OKBLUE + f"Tried {position} | " + bcolors.OKGREEN +
                                  f"{proxy} | {output} | " + bcolors.OKCYAN + f"{view_stat} " + bcolors.ENDC)

                            create_html({"#3b8eea": f"Tried {position} | ",
                                         "#23d18b": f"{proxy} | {output} | ", "#29b2d3": f"{view_stat} "})
                        else:
                            error += 1

                        play_video(driver)
                        random_command(driver)

                        if error == 5:
                            break
                        sleep(60)

                else:
                    rand_choice = 1
                    if len(suggested) > 1 and view_stat != 'music':
                        rand_choice = randint(1, 3)

                    increment = 0
                    for i in range(rand_choice):
                        if i == 0:
                            control_player(
                                driver, output, position, proxy, youtube)

                            view.append(position)
                            increment = i + 1

                        else:
                            print(timestamp() + bcolors.OKBLUE +
                                  f"Tried {position} | Suggested video loop : {i}" + bcolors.ENDC)

                            create_html(
                                {"#3b8eea": f"Tried {position} | Suggested video loop : {i}"})

                            output = play_next_video(driver, suggested)

                            print(timestamp() + bcolors.OKBLUE +
                                  f"Tried {position} | Found next suggested video : [{output}]" + bcolors.ENDC)

                            create_html(
                                {"#3b8eea": f"Tried {position} | Found next suggested video : [{output}]"})

                            skip_initial_ad(driver, output, duration_dict)

                            features(driver)

                            control_player(
                                driver, output, position, proxy, youtube)

                            view.append(position)
                            increment = i + 1

                if randint(1, 2) == 1:
                    driver.find_element(By.ID, 'movie_player').send_keys('k')

                view_count = len(view)
                print(timestamp() + bcolors.OKCYAN +
                      f'View added : {view_count}' + bcolors.ENDC)

                create_html({"#29b2d3": f'View added : {view_count}'})

                if database:
                    try:
                        update_database(
                            database=DATABASE, threads=max_threads, increment=increment)
                    except:
                        pass

                status = quit_driver(driver, pluginfile)

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
                      f"Tried {position} | Line : {exc_tb.tb_lineno} | " + str(e.args[0]) + bcolors.ENDC)

                create_html(
                    {"#f14c4c": f"Tried {position} | Line : {exc_tb.tb_lineno} | " + str(e.args[0])})

                status = quit_driver(driver, pluginfile)
                pass

    except UrlsError:
        print(timestamp() + bcolors.FAIL +
              f"Tried {position} | Your urls.txt is empty!" + bcolors.ENDC)

        create_html(
            {"#f14c4c": f"Tried {position} | Your urls.txt is empty!"})
        pass

    except SearchError:
        print(timestamp() + bcolors.FAIL +
              f"Tried {position} | Your search.txt is empty!" + bcolors.ENDC)

        create_html(
            {"#f14c4c": f"Tried {position} | Your search.txt is empty!"})
        pass

    except:
        print(timestamp() + bcolors.OKBLUE + f"Tried {position} | " +
              bcolors.FAIL + f"{proxy} | {proxy_type.upper()} | Bad proxy " + bcolors.ENDC)

        create_html({"#3b8eea": f"Tried {position} | ",
                     "#f14c4c": f"{proxy} | {proxy_type.upper()} | Bad proxy "})

        checked[position] = proxy_type
        pass


def stop_server(immediate=False):
    global server_running

    if api and server_running:
        if not immediate:
            while 'state=running' in str(futures[1:-1]):
                sleep(5)

        server_running = False
        requests.post(f'http://127.0.0.1:{port}/shutdown')


def view_video(position):
    global server_running

    if position == 0:
        if api and not server_running:
            server_running = True
            website.start_server(host=host, port=port)

    elif position == total_proxies - 1:
        stop_server()

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


def clean_exit(executor):
    executor.shutdown(wait=False)

    driver_list_ = list(driver_list)
    for driver in driver_list_:
        quit_driver(driver, None)

    while True:
        try:
            work_item = executor._work_queue.get_nowait()
        except queue.Empty:
            break

        if work_item is not None:
            work_item.future.cancel()


def main():
    global start_time, total_proxies, proxy_list, threads, futures

    start_time = time()
    threads = randint(min_threads, max_threads)
    if api:
        threads += 1

    pool_number = [i for i in range(total_proxies)]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(view_video, position)
                   for position in pool_number]

        try:
            for future in as_completed(futures):

                if len(view) >= views:
                    print(
                        bcolors.WARNING + f'Amount of views added : {views} | Stopping program...' + bcolors.ENDC)

                    clean_exit(executor)
                    stop_server()
                    break

                elif refresh != 0:

                    if (time() - start_time) > refresh*60:

                        if filename:
                            if proxy_api:
                                proxy_list = scrape_api(filename)
                            else:
                                proxy_list = load_proxy(filename)
                        else:
                            proxy_list = gather_proxy()

                        print(bcolors.WARNING +
                              f'Proxy reloaded from : {filename}' + bcolors.ENDC)

                        total_proxies = len(proxy_list)
                        print(bcolors.OKCYAN +
                              f'Total proxies : {total_proxies}' + bcolors.ENDC)

                        proxy_list.insert(0, 'dummy')
                        proxy_list.append('dummy')

                        total_proxies += 2

                        clean_exit(executor)
                        stop_server()
                        break

                future.result()

        except KeyboardInterrupt:
            clean_exit(executor)
            executor._threads.clear()
            concurrent.futures.thread._threads_queues.clear()
            stop_server(immediate=True)
            sys.exit()


if __name__ == '__main__':

    update_chrome_version()
    check_update()
    osname, exe_name = download_driver(patched_drivers=patched_drivers)
    create_database(database=DATABASE, database_backup=DATABASE_BACKUP)

    urls = load_url()
    queries = load_search()

    hash_urls = get_hash("urls.txt")
    hash_queries = get_hash("search.txt")

    if os.path.isfile(config_path):
        with open(config_path, 'r') as openfile:
            config = json.load(openfile)

        if len(config) == 11:
            print(json.dumps(config, indent=4))
            previous = str(input(
                bcolors.OKBLUE + 'Config file exists! Do you want to continue with previous saved preferences ? [Yes/No] : ' + bcolors.ENDC)).lower()
            if previous == 'n' or previous == 'no':
                create_config(config_path=config_path)
            else:
                pass
        else:
            print(bcolors.FAIL + 'Previous config file is not compatible with the latest script! Create a new one...' + bcolors.ENDC)
            create_config(config_path=config_path)
    else:
        create_config(config_path=config_path)

    with open(config_path, 'r') as openfile:
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
    proxy_api = config["proxy"]["proxy_api"]
    refresh = config["proxy"]["refresh"]
    background = config["background"]
    bandwidth = config["bandwidth"]
    playback_speed = config["playback_speed"]
    max_threads = config["max_threads"]
    min_threads = config["min_threads"]

    if auth_required and background:
        print(bcolors.FAIL +
              "Premium proxy needs extension to work. Chrome doesn't support extension in Headless mode." + bcolors.ENDC)
        input(bcolors.WARNING +
              f"Either use proxy without username & password or disable headless mode " + bcolors.ENDC)
        sys.exit()

    copy_drivers(cwd=cwd, patched_drivers=patched_drivers,
                 exe=exe_name, total=max_threads)

    if filename:
        if category == 'r':
            proxy_list = [filename]
            proxy_list = proxy_list * 1000
        else:
            if proxy_api:
                proxy_list = scrape_api(filename)
            else:
                proxy_list = load_proxy(filename)

    else:
        proxy_list = gather_proxy()

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
