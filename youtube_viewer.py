import json
import re
import textwrap
from concurrent.futures import ThreadPoolExecutor, wait
from time import time as get_time, sleep, strftime, gmtime
from datetime import datetime

import logging
import psutil
import undetected_chromedriver as uc
from fake_headers import Headers, browsers
from faker import Faker
from requests.exceptions import RequestException
from tabulate import tabulate

from youtubeviewer import website
from youtubeviewer.basics import *
from youtubeviewer.config import create_config
from youtubeviewer.database import *
from youtubeviewer.download_driver import *
from youtubeviewer.load_files import *
from youtubeviewer.proxies import *

log = logging.getLogger("werkzeug")
log.disabled = True

SCRIPT_VERSION = "1.9.0"

print(
    bcolors.OKGREEN
    + """

Yb  dP  dP"Yb  88   88 888888 88   88 88""Yb 888888
 YbdP  dP   Yb 88   88   88   88   88 88__dP 88__
  8P   Yb   dP Y8   8P   88   Y8   8P 88""Yb 88""
 dP     YbodP  `YbodP'   88   `YbodP' 88oodP 888888

                        Yb    dP 88 888888 Yb        dP 888888 88""Yb
                         Yb  dP  88 88__    Yb  db  dP  88__   88__dP
                          YbdP   88 88""     YbdPYbdP   88""   88"Yb
                           YP    88 888888    YP  YP    888888 88  Yb
"""
    + bcolors.ENDC
)

print(
    bcolors.OKCYAN
    + """
           [ GitHub : https://github.com/MShawon/YouTube-Viewer ]
           [ Maintained by : Leaske ]
"""
    + bcolors.ENDC
)

print(
    bcolors.WARNING
    + f"""
+{'-'*26} Version: {SCRIPT_VERSION} {'-'*26}+
"""
    + bcolors.ENDC
)


proxy = None
status = None
start_time = None
cancel_all = False

urls = []
queries = []
suggested = []

hash_urls = None
hash_queries = None
hash_config = None

driver_dict = {}
duration_dict = {}
checked = {}
summary = {}
video_statistics = {}
view = []
bad_proxies = []
used_proxies = []
temp_folders = []
console = []

threads = 0
views = 100

fake = Faker()
cwd = os.getcwd()
patched_drivers = os.path.join(cwd, "patched_drivers")
config_path = os.path.join(cwd, "config.json")

DATABASE = os.path.join(cwd, "database.db")
DATABASE_BACKUP = os.path.join(cwd, "database_backup.db")

animation = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
headers_1 = ["Worker", "Video Title", "Watch / Actual Duration"]
headers_2 = ["Index", "Video Title", "Views"]

width = 0
viewports = [
    "2560,1440",
    "1920,1080",
    "1440,900",
    "1536,864",
    "1366,768",
    "1280,1024",
    "1024,768",
]

referers = [
    "https://search.yahoo.com/",
    "https://duckduckgo.com/",
    "https://www.google.com/",
    "https://www.bing.com/",
]

referers = choices(referers, k=len(referers) * 3)

website.console = console
website.database = DATABASE


def timestamp():
    global date_fmt
    date_fmt = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    return bcolors.OKGREEN + f"[{date_fmt}] | " + bcolors.OKCYAN + f"{cpu_usage} | "


def clean_exe_temp(folder):
    temp_name = None
    if hasattr(sys, "_MEIPASS"):
        temp_name = sys._MEIPASS.split("\\")[-1]
    else:
        if sys.version_info.major == 3 and (
            sys.version_info.minor < 7 or sys.version_info.minor > 13
        ):
            print(f"Your current python version is not compatible: {sys.version}")
            print(f"Install Python version between 3.7.x to 3.13.x to run this script")
            input("")
            sys.exit()

    for f in glob(os.path.join("temp", folder, "*")):
        if temp_name not in f:
            shutil.rmtree(f, ignore_errors=True)


def update_chrome_version():
    link = "https://gist.githubusercontent.com/MShawon/29e185038f22e6ac5eac822a1e422e9d/raw/versions.txt"

    output = requests.get(link, timeout=60).text
    chrome_versions = output.split("\n")

    browsers.chrome_ver = chrome_versions


def check_update():
    api_url = "https://api.github.com/repos/MShawon/YouTube-Viewer/releases/latest"
    try:
        response = requests.get(api_url, timeout=30)

        RELEASE_VERSION = response.json()["tag_name"]

        if RELEASE_VERSION > SCRIPT_VERSION:
            print(bcolors.OKCYAN + "#" * 100 + bcolors.ENDC)
            print(
                bcolors.OKCYAN
                + "Update Available!!! "
                + f"YouTube Viewer version {SCRIPT_VERSION} needs to update to {RELEASE_VERSION} version."
                + bcolors.ENDC
            )

            try:
                notes = response.json()["body"].split("SHA256")[0].split("\r\n")
                for note in notes:
                    if note:
                        print(bcolors.HEADER + note + bcolors.ENDC)
            except Exception:
                pass
            print(bcolors.OKCYAN + "#" * 100 + "\n" + bcolors.ENDC)
    except Exception:
        pass


def create_html(text_dict):
    if len(console) > 250:
        console.pop()

    date = f'<span style="color:#23d18b"> [{date_fmt}] | </span>'
    cpu = f'<span style="color:#29b2d3"> {cpu_usage} | </span>'
    str_fmt = "".join(
        [
            f'<span style="color:{key}"> {value} </span>'
            for key, value in text_dict.items()
        ]
    )
    html = date + cpu + str_fmt

    console.insert(0, html)


def detect_file_change():
    global hash_urls, hash_queries, urls, queries

    if hash_urls != get_hash("urls.txt"):
        hash_urls = get_hash("urls.txt")
        urls = load_url()
        suggested.clear()

    if hash_queries != get_hash("search.txt"):
        hash_queries = get_hash("search.txt")
        queries = load_search()
        suggested.clear()


def direct_or_search(position):
    keyword = None
    video_title = None
    if position % 2:
        try:
            method = 1
            url = choice(urls)
            if "music.youtube.com" in url:
                youtube = "Music"
            else:
                youtube = "Video"
        except IndexError:
            raise Exception("Your urls.txt is empty!")

    else:
        try:
            method = 2
            query = choice(queries)
            keyword = query[0]
            video_title = query[1]
            url = "https://www.youtube.com"
            youtube = "Video"
        except IndexError:
            try:
                youtube = "Music"
                url = choice(urls)
                if "music.youtube.com" not in url:
                    raise Exception
            except Exception:
                raise Exception("Your search.txt is empty!")

    return url, method, youtube, keyword, video_title


def features(driver):
    if bandwidth:
        save_bandwidth(driver)

    bypass_popup(driver)

    bypass_other_popup(driver)

    play_video(driver)

    change_playback_speed(driver, playback_speed)


def update_view_count(position):
    view.append(position)
    view_count = len(view)
    print(
        timestamp()
        + bcolors.OKCYAN
        + f"Worker {position} | View added : {view_count}"
        + bcolors.ENDC
    )

    create_html({"#29b2d3": f"Worker {position} | View added : {view_count}"})

    if database:
        try:
            update_database(database=DATABASE, threads=max_threads)
        except Exception:
            pass


def set_referer(position, url, method, driver):
    output = None  # Initialize output variable
    referer = choice(referers)
    if referer:
        if method == 2 and "t.co/" in referer:
            driver.get(url)
        else:
            if "search.yahoo.com" in referer:
                driver.get("https://duckduckgo.com/")
                driver.execute_script(
                    "window.history.pushState('page2', 'Title', arguments[0]);", referer
                )
            else:
                driver.get(referer)

            driver.execute_script("window.location.href = '{}';".format(url))

        print(
            timestamp()
            + bcolors.OKBLUE
            + f"Worker {position} | Referer used : {referer}"
            + bcolors.ENDC
        )

        create_html({"#3b8eea": f"Worker {position} | Referer used : {referer}"})

    else:
        driver.get(url)

    try:
        output = driver.title.replace(" - YouTube", "")
    except:
        output = "Unknown Title"

    return output


def youtube_normal(method, keyword, video_title, driver, output):
    if method == 2:
        msg = search_video(driver, keyword, video_title)
        if msg == "failed":
            raise Exception(
                f"Can't find this [{video_title}] video with this keyword [{keyword}]"
            )

    skip_initial_ad(driver, output, duration_dict)

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "movie_player"))
        )
    except WebDriverException:
        raise Exception(
            "Slow internet speed or Stuck at reCAPTCHA! Can't load YouTube..."
        )

    features(driver)

    try:
        view_stat = (
            WebDriverWait(driver, 30)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "#count span")))
            .text
        )
        if not view_stat:
            raise WebDriverException
    except WebDriverException:
        view_stat = driver.find_element(By.XPATH, '//*[@id="info"]/span[1]').text

    return view_stat


def youtube_music(driver):
    if "coming-soon" in driver.title or "not available" in driver.title:
        raise Exception("YouTube Music is not available in your area!")
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="player-page"]'))
        )
    except WebDriverException:
        raise Exception(
            "Slow internet speed or Stuck at reCAPTCHA! Can't load YouTube..."
        )

    bypass_popup(driver)

    play_music(driver)

    output = driver.find_element(
        By.XPATH, "//ytmusic-player-bar//yt-formatted-string"
    ).text
    view_stat = "music"

    return view_stat, output


def spoof_timezone_geolocation(proxy_type, proxy, driver):
    try:
        proxy_dict = {
            "http": f"{proxy_type}://{proxy}",
            "https": f"{proxy_type}://{proxy}",
        }
        resp = requests.get("http://ip-api.com/json", proxies=proxy_dict, timeout=30)

        if resp.status_code == 200:
            location = resp.json()
            tz_params = {"timezoneId": location["timezone"]}
            latlng_params = {
                "latitude": location["lat"],
                "longitude": location["lon"],
                "accuracy": randint(20, 100),
            }
            info = f"ip-api.com | Lat : {location['lat']} | Lon : {location['lon']} | TZ: {location['timezone']}"
        else:
            raise RequestException

    except RequestException:
        location = fake.location_on_land()
        tz_params = {"timezoneId": location[-1]}
        latlng_params = {
            "latitude": location[0],
            "longitude": location[1],
            "accuracy": randint(20, 100),
        }
        info = (
            f"Random | Lat : {location[0]} | Lon : {location[1]} | TZ: {location[-1]}"
        )

    try:
        driver.execute_cdp_cmd("Emulation.setTimezoneOverride", tz_params)

        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", latlng_params)

    except WebDriverException:
        pass

    return info


def control_player(driver, output, position, proxy, youtube, collect_id=True):
    current_url = driver.current_url

    video_len = duration_dict.get(output, 0)
    for _ in range(90):
        if video_len != 0:
            duration_dict[output] = video_len
            break

        video_len = driver.execute_script(
            "return document.getElementById('movie_player').getDuration()"
        )
        sleep(1)

    if video_len == 0:
        raise Exception("Video player is not loading...")

    actual_duration = strftime("%Hh:%Mm:%Ss", gmtime(video_len)).lstrip("0h:0m:")
    video_len = video_len * uniform(minimum, maximum)
    duration = strftime("%Hh:%Mm:%Ss", gmtime(video_len)).lstrip("0h:0m:")

    if len(output) == 11:
        output = driver.title[:-10]

    summary[position] = [position, output, f"{duration} / {actual_duration}"]
    website.summary_table = tabulate(
        summary.values(),
        headers=headers_1,
        numalign="center",
        stralign="center",
        tablefmt="html",
    )

    print(
        timestamp()
        + bcolors.OKBLUE
        + f"Worker {position} | "
        + bcolors.OKGREEN
        + f"{proxy} --> {youtube} Found : {output} | Watch Duration : {duration} "
        + bcolors.ENDC
    )

    create_html(
        {
            "#3b8eea": f"Worker {position} | ",
            "#23d18b": f"{proxy.split('@')[-1]} --> {youtube} Found : {output} | Watch Duration : {duration} ",
        }
    )

    if youtube == "Video" and collect_id:
        try:
            video_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", current_url).group(
                1
            )
            if video_id not in suggested and output in driver.title:
                suggested.append(video_id)
        except Exception:
            pass

    try:
        current_channel = driver.find_element(By.CSS_SELECTOR, "#upload-info a").text
    except WebDriverException:
        current_channel = "Unknown"

    error = 0
    loop = int(video_len / 4)
    for _ in range(loop):
        sleep(5)
        current_time = driver.execute_script(
            "return document.getElementById('movie_player').getCurrentTime()"
        )

        if youtube == "Video":
            play_video(driver)
            random_command(driver)
        elif youtube == "Music":
            play_music(driver)

        current_state = driver.execute_script(
            "return document.getElementById('movie_player').getPlayerState()"
        )
        if current_state in [-1, 3]:
            error += 1
        else:
            error = 0

        if error == 10:
            error_msg = f"Taking too long to play the video | Reason : buffering"
            if current_state == -1:
                error_msg = f"Failed to play the video | Possible Reason : {proxy.split('@')[-1]} not working anymore"
            raise Exception(error_msg)

        elif current_time > video_len or driver.current_url != current_url:
            break

    summary.pop(position, None)
    website.summary_table = tabulate(
        summary.values(),
        headers=headers_1,
        numalign="center",
        stralign="center",
        tablefmt="html",
    )

    output = textwrap.fill(text=output, width=75, break_on_hyphens=False)
    video_statistics[output] = video_statistics.get(output, 0) + 1
    website.html_table = tabulate(
        video_statistics.items(),
        headers=headers_2,
        showindex=True,
        numalign="center",
        stralign="center",
        tablefmt="html",
    )

    return current_url, current_channel


def youtube_live(proxy, position, driver, output):
    error = 0
    while True:
        try:
            view_stat = driver.find_element(By.CSS_SELECTOR, "#count span").text
            if not view_stat:
                raise WebDriverException
        except WebDriverException:
            view_stat = driver.find_element(By.XPATH, '//*[@id="info"]/span[1]').text
        if "watching" in view_stat:
            print(
                timestamp()
                + bcolors.OKBLUE
                + f"Worker {position} | "
                + bcolors.OKGREEN
                + f"{proxy} | {output} | "
                + bcolors.OKCYAN
                + f"{view_stat} "
                + bcolors.ENDC
            )

            create_html(
                {
                    "#3b8eea": f"Worker {position} | ",
                    "#23d18b": f"{proxy.split('@')[-1]} | {output} | ",
                    "#29b2d3": f"{view_stat} ",
                }
            )
        else:
            error += 1

        play_video(driver)

        random_command(driver)

        if error == 5:
            break
        sleep(60)

    update_view_count(position)


def music_and_video(proxy, position, youtube, driver, output, view_stat):
    try:
        current_url, current_channel = control_player(
            driver, output, position, proxy, youtube, collect_id=True
        )

        update_view_count(position)

        rand_choice = 1
        if len(suggested) > 1 and view_stat != "music":
            try:
                rand_choice = randint(1, 3)

                for i in range(1, rand_choice):
                    print(
                        timestamp()
                        + bcolors.OKBLUE
                        + f"Worker {position} | Suggested video loop : {i}"
                        + bcolors.ENDC
                    )

                    create_html(
                        {"#3b8eea": f"Worker {position} | Suggested video loop : {i}"}
                    )

                    try:
                        output = play_next_video(driver, suggested)

                        print(
                            timestamp()
                            + bcolors.OKBLUE
                            + f"Worker {position} | Found next suggested video : [{output}]"
                            + bcolors.ENDC
                        )

                        create_html(
                            {
                                "#3b8eea": f"Worker {position} | Found next suggested video : [{output}]"
                            }
                        )

                        skip_initial_ad(driver, output, duration_dict)
                        features(driver)
                        current_url, current_channel = control_player(
                            driver, output, position, proxy, youtube, collect_id=False
                        )
                        update_view_count(position)

                    except Exception as e:
                        print(
                            timestamp()
                            + bcolors.FAIL
                            + f"Worker {position} | Error playing suggested video: {str(e)}"
                            + bcolors.ENDC
                        )
                        break

            except Exception as e:
                print(
                    timestamp()
                    + bcolors.FAIL
                    + f"Worker {position} | Suggested video error: {str(e)}"
                    + bcolors.ENDC
                )

    except Exception as e:
        raise e

    return current_url, current_channel


def channel_or_endscreen(
    proxy, position, youtube, driver, view_stat, current_url, current_channel
):
    option = 1
    if view_stat != "music" and driver.current_url == current_url:
        option = choices([1, 2, 3], cum_weights=(0.5, 0.75, 1.00), k=1)[0]

        if option == 2:
            try:
                output, log, option = play_from_channel(driver, current_channel)
            except WebDriverException as e:
                raise Exception(
                    f"Error channel | {type(e).__name__} | {e.args[0] if e.args else ''}"
                )

            print(
                timestamp()
                + bcolors.OKBLUE
                + f"Worker {position} | {log}"
                + bcolors.ENDC
            )

            create_html({"#3b8eea": f"Worker {position} | {log}"})

        elif option == 3:
            try:
                output = play_end_screen_video(driver)
            except WebDriverException as e:
                raise Exception(
                    f"Error end screen | {type(e).__name__} | {e.args[0] if e.args else ''}"
                )

            print(
                timestamp()
                + bcolors.OKBLUE
                + f"Worker {position} | Video played from end screen : [{output}]"
                + bcolors.ENDC
            )

            create_html(
                {
                    "#3b8eea": f"Worker {position} | Video played from end screen : [{output}]"
                }
            )

        if option in [2, 3]:
            skip_initial_ad(driver, output, duration_dict)

            features(driver)

            current_url, current_channel = control_player(
                driver, output, position, proxy, youtube, collect_id=False
            )

        if option in [2, 3, 4]:
            update_view_count(position)


def windows_kill_drivers():
    for process in constructor.Win32_Process(["CommandLine", "ProcessId"]):
        try:
            if "UserAgentClientHint" in process.CommandLine:
                print(f"Killing PID : {process.ProcessId}", end="\r")
                subprocess.Popen(
                    ["taskkill", "/F", "/PID", f"{process.ProcessId}"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                )
        except Exception:
            pass
    print("\n")


def quit_driver(driver):
    try:
        if driver and driver in driver_dict:
            driver.quit()
    except Exception as e:
        print(f"Error while quitting driver: {e}")
    finally:
        proxy_folder = driver_dict.pop(driver, None)
        if proxy_folder:
            shutil.rmtree(proxy_folder, ignore_errors=True)
    return 400


def handle_cookie_consent(driver):
    for _ in range(3):
        try:
            consent_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Accept all')]")
                )
            )
            consent_button.click()
            print("Cookie consent accepted.")
            return
        except WebDriverException:
            print("No cookie consent popup found or clicking failed. Retrying...")
            sleep(1)
    print("Failed to handle cookie consent after multiple attempts.")


def main_viewer(proxy_type, proxy, position):
    global width, viewports
    driver = None

    if cancel_all:
        raise KeyboardInterrupt

    try:
        detect_file_change()

        checked[position] = None

        header = Headers(browser="chrome", os=osname, headers=False).generate()
        agent = header["User-Agent"]

        url, method, youtube, keyword, video_title = direct_or_search(position)

        if category == "r" and proxy_api:
            for _ in range(20):
                proxy = choice(proxies_from_api)
                if proxy not in used_proxies:
                    break
            used_proxies.append(proxy)

        status = check_proxy(category, agent, proxy, proxy_type)

        if status != 200:
            raise RequestException(status)

        try:
            print(
                timestamp()
                + bcolors.OKBLUE
                + f"Worker {position} | "
                + bcolors.OKBLUE
                + f"{proxy} | {proxy_type.upper()} | Good Proxy | Opening a new driver..."
                + bcolors.ENDC
            )

            create_html(
                {
                    "#3b8eea": f"Worker {position} | {proxy.split('@')[-1]} | {proxy_type.upper()} | Good Proxy | Opening a new driver..."  # Combined into single color
                }
            )

            while proxy in bad_proxies:
                bad_proxies.remove(proxy)
                sleep(1)

            options = uc.ChromeOptions()
            options.add_argument(f"user-agent={agent}")
            if background:
                options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--proxy-server='direct://'")
            options.add_argument("--proxy-bypass-list=*")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-infobars")
            options.add_argument("--lang=en")

            driver = uc.Chrome(options=options)
            driver_dict[driver] = None

            sleep(2)

            info = spoof_timezone_geolocation(proxy_type, proxy, driver)

            isdetected = driver.execute_script("return navigator.webdriver")

            print(
                timestamp()
                + bcolors.OKBLUE
                + f"Worker {position} | "
                + bcolors.OKBLUE
                + f"{proxy} | {proxy_type.upper()} | "
                + bcolors.OKBLUE
                + f"{info} | Detected? : {isdetected}"
                + bcolors.ENDC
            )

            create_html(
                {
                    "#3b8eea": f"Worker {position} | {proxy.split('@')[-1]} | {proxy_type.upper()} | {info} | Detected? : {isdetected}"
                }
            )

            if width == 0:
                width = driver.execute_script("return screen.width")
                height = driver.execute_script("return screen.height")
                print(f"Display resolution : {width}x{height}")
                viewports = [i for i in viewports if int(i[:4]) <= width]

            output = set_referer(position, url, method, driver)

            driver.get(url)

            direct_watch = False
            if (
                "Your YouTube history is off" in driver.page_source
                or "Try searching" in driver.page_source
            ):
                print(
                    timestamp()
                    + bcolors.OKBLUE
                    + f"Worker {position} | "
                    + bcolors.OKBLUE
                    + f"{proxy} | {proxy_type.upper()} | "
                    + bcolors.OKBLUE
                    + "Detected stuck page..."
                    + bcolors.ENDC
                )
                bypassed_url = bypass_stuck_page(driver, urls, position)
                if bypassed_url:
                    direct_watch = True
                    url = bypassed_url
                else:
                    print(
                        timestamp()
                        + bcolors.OKBLUE
                        + f"Worker {position} | "
                        + bcolors.OKBLUE
                        + f"{proxy} | {proxy_type.upper()} | Detected stuck page..."
                        + bcolors.ENDC
                    )
                    raise Exception("Could not bypass stuck page")
                sleep(2)

                if direct_watch:
                    video_title = driver.title.replace(" - YouTube", "")
                print(
                    timestamp()
                    + bcolors.OKBLUE
                    + f"Worker {position} | "
                    + bcolors.OKBLUE
                    + f"{proxy} | {proxy_type.upper()} | "
                    + bcolors.OKBLUE
                    + f"--> Video Found : {video_title}"
                    + bcolors.ENDC
                )
                output = video_title

                skip_initial_ad(driver, output, duration_dict)

                features(driver)

                try:
                    view_stat = (
                        WebDriverWait(driver, 30)
                        .until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, "#count span")
                            )
                        )
                        .text
                    )
                    if not view_stat:
                        raise WebDriverException
                except WebDriverException:
                    view_stat = driver.find_element(
                        By.XPATH, '//*[@id="info"]/span[1]'
                    ).text

                if "watching" in view_stat:
                    youtube_live(proxy, position, driver, output)
                else:
                    current_url, current_channel = music_and_video(
                        proxy, position, "Video", driver, output, view_stat
                    )

                    channel_or_endscreen(
                        proxy,
                        position,
                        "Video",
                        driver,
                        view_stat,
                        current_url,
                        current_channel,
                    )
            else:
                if youtube == "Video":
                    view_stat = youtube_normal(
                        method, keyword, video_title, driver, output
                    )
                else:
                    view_stat, output = youtube_music(driver)

                if "watching" in view_stat:
                    youtube_live(proxy, position, driver, output)
                else:
                    current_url, current_channel = music_and_video(
                        proxy, position, youtube, driver, output, view_stat
                    )

                    channel_or_endscreen(
                        proxy,
                        position,
                        youtube,
                        driver,
                        view_stat,
                        current_url,
                        current_channel,
                    )

            if video_title:
                output = video_title
            else:
                output = driver.title[:-10]

            if youtube == "Video":
                view_stat = youtube_normal(method, keyword, video_title, driver, output)
            else:
                view_stat, output = youtube_music(driver)

            if "watching" in view_stat:
                youtube_live(proxy, position, driver, output)

            else:
                current_url, current_channel = music_and_video(
                    proxy, position, youtube, driver, output, view_stat
                )

            channel_or_endscreen(
                proxy,
                position,
                youtube,
                driver,
                view_stat,
                current_url,
                current_channel,
            )

            if randint(1, 2) == 1:
                try:
                    driver.find_element(By.ID, "movie_player").send_keys("k")
                except WebDriverException:
                    pass

            status = quit_driver(driver=driver)

        except Exception as e:
            status = quit_driver(driver=driver)

            print(
                timestamp()
                + bcolors.FAIL
                + f"Worker {position} | Line : {e.__traceback__.tb_lineno} | {type(e).__name__} | {e.args[0] if e.args else ''}"
                + bcolors.ENDC
            )

            create_html(
                {
                    "#f14c4c": f"Worker {position} | Line : {e.__traceback__.tb_lineno} | {type(e).__name__} | {e.args[0] if e.args else ''}"
                }
            )

    except RequestException:
        print(
            timestamp()
            + bcolors.OKBLUE
            + f"Worker {position} | "
            + bcolors.FAIL
            + f"{proxy} | {proxy_type.upper()} | Bad proxy "
            + bcolors.ENDC
        )

        create_html(
            {
                "#3b8eea": f"Worker {position} | ",
                "#f14c4c": f"{proxy.split('@')[-1]} | {proxy_type.upper()} | Bad proxy ",
            }
        )

        checked[position] = proxy_type
        bad_proxies.append(proxy)

    except Exception as e:
        print(
            timestamp()
            + bcolors.FAIL
            + f"Worker {position} | Line : {e.__traceback__.tb_lineno} | {type(e).__name__} | {e.args[0] if e.args else ''}"
            + bcolors.ENDC
        )

        create_html(
            {
                "#f14c4c": f"Worker {position} | Line : {e.__traceback__.tb_lineno} | {type(e).__name__} | {e.args[0] if e.args else ''}"
            }
        )


def get_proxy_list():
    if filename:
        if category == "r":
            factor = max_threads if max_threads > 1000 else 1000
            proxy_list = [filename] * factor
        else:
            if proxy_api:
                proxy_list = scrape_api(filename)
            else:
                proxy_list = load_proxy(filename)

    else:
        proxy_list = gather_proxy()

    return proxy_list


def stop_server(immediate=False):
    if not immediate:
        print("Allowing a maximum of 15 minutes to finish all the running drivers...")
        for _ in range(180):
            sleep(5)
            if "state=running" not in str(futures[1:-1]):
                break

    if api:
        for _ in range(10):
            response = requests.post(f"http://127.0.0.1:{port}/shutdown")
            if response.status_code == 200:
                print("Server shut down successfully!")
                break
            else:
                print(f"Server shut down error : {response.status_code}")
                sleep(3)


def clean_exit():
    print(
        f"[{datetime.now().strftime('%d-%b-%Y %H:%M:%S')}] | "
        + f"{randint(10, 90):.1f}%  | "
        + bcolors.WARNING
        + "Cleaning up processes..."
        + bcolors.ENDC
    )
    create_html({"#f3f342": "Cleaning up processes..."})

    if osname == "win":
        for driver in list(driver_dict):
            try:
                driver.quit()
            except Exception:
                pass

        driver_dict.clear()

        try:
            windows_kill_drivers()
        except Exception:
            pass
    else:
        for driver in list(driver_dict):
            try:
                quit_driver(driver)
            except Exception:
                pass

    for folder in temp_folders:
        try:
            shutil.rmtree(folder, ignore_errors=True)
        except Exception as e:
            print(
                f"[{datetime.now().strftime('%d-%b-%Y %H:%M:%S')}] | "
                + f"{randint(10, 90):.1f}%  | "
                + bcolors.FAIL
                + f"Error while removing folder {folder}: {e}"
                + bcolors.ENDC
            )


def cancel_pending_task(not_done):
    global cancel_all

    cancel_all = True
    for future in not_done:
        _ = future.cancel()

    clean_exit()

    stop_server(immediate=True)
    _ = wait(not_done, timeout=None)

    clean_exit()


def view_video(position):
    if position == 0:
        if api:
            website.start_server(host=host, port=port)

    elif position == total_proxies - 1:
        stop_server(immediate=False)
        clean_exit()

    else:
        sleep(2)
        proxy = proxy_list[position]

        if proxy_type:
            main_viewer(proxy_type, proxy, position)
        elif "|" in proxy:
            splitted = proxy.split("|")
            main_viewer(splitted[-1], splitted[0], position)
        else:
            main_viewer("http", proxy, position)
            if checked[position] == "http":
                main_viewer("socks4", proxy, position)
            if checked[position] == "socks4":
                main_viewer("socks5", proxy, position)


def main():
    global cancel_all, proxy_list, total_proxies, proxies_from_api, threads, hash_config, futures, cpu_usage

    cancel_all = False
    start_time = get_time()
    hash_config = get_hash(config_path)

    proxy_list = get_proxy_list()
    if category != "r":
        print(bcolors.OKCYAN + f"Total proxies : {len(proxy_list)}" + bcolors.ENDC)

    proxy_list = [x for x in proxy_list if x not in bad_proxies]
    if len(proxy_list) == 0:
        bad_proxies.clear()
        proxy_list = get_proxy_list()
    if proxy_list[0] != "dummy":
        proxy_list.insert(0, "dummy")
    if proxy_list[-1] != "dummy":
        proxy_list.append("dummy")
    total_proxies = len(proxy_list)

    if category == "r" and proxy_api:
        proxies_from_api = scrape_api(link=filename)

    threads = randint(min_threads, max_threads)
    if api:
        threads += 1

    loop = 0
    pool_number = list(range(total_proxies))

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(view_video, position) for position in pool_number]

        done, not_done = wait(futures, timeout=0)
        try:
            while not_done:
                freshly_done, not_done = wait(not_done, timeout=1)
                done |= freshly_done

                loop += 1
                for _ in range(70):
                    cpu = str(psutil.cpu_percent(0.2))
                    cpu_usage = (
                        cpu + "%" + " " * (5 - len(cpu)) if cpu != "0.0" else cpu_usage
                    )

                if loop % 40 == 0:
                    print(
                        tabulate(
                            video_statistics.items(),
                            headers=headers_2,
                            showindex=True,
                            tablefmt="pretty",
                        )
                    )

                if category == "r" and proxy_api:
                    proxies_from_api = scrape_api(link=filename)

                if len(view) >= views:
                    print(
                        timestamp()
                        + bcolors.WARNING
                        + f"Amount of views added : {views} | Stopping program..."
                        + bcolors.ENDC
                    )
                    create_html(
                        {
                            "#f3f342": f"Amount of views added : {views} | Stopping program..."
                        }
                    )

                    cancel_pending_task(not_done=not_done)
                    break

                elif hash_config != get_hash(config_path):
                    hash_config = get_hash(config_path)
                    print(
                        timestamp()
                        + bcolors.WARNING
                        + "Modified config.json will be in effect soon..."
                        + bcolors.ENDC
                    )
                    create_html(
                        {"#f3f342": "Modified config.json will be in effect soon..."}
                    )

                    cancel_pending_task(not_done=not_done)
                    break

                elif refresh != 0 and category != "r":
                    if (get_time() - start_time) > refresh * 60:  # Changed from time()
                        start_time = get_time()  # Changed from time()

                        proxy_list_new = get_proxy_list()
                        proxy_list_new = [
                            x for x in proxy_list_new if x not in bad_proxies
                        ]

                        proxy_list_old = [
                            x for x in proxy_list[1:-1] if x not in bad_proxies
                        ]

                        if sorted(proxy_list_new) != sorted(proxy_list_old):
                            print(
                                timestamp()
                                + bcolors.WARNING
                                + f"Refresh {refresh} minute triggered. Proxies will be reloaded soon..."
                                + bcolors.ENDC
                            )
                            create_html(
                                {
                                    "#f3f342": f"Refresh {refresh} minute triggered. Proxies will be reloaded soon..."
                                }
                            )

                            cancel_pending_task(not_done=not_done)
                            break

        except KeyboardInterrupt:
            print(
                timestamp()
                + bcolors.WARNING
                + "Hold on!!! Allow me a moment to close all the running drivers."
                + bcolors.ENDC
            )
            create_html(
                {
                    "#f3f342": "Hold on!!! Allow me a moment to close all the running drivers."
                }
            )

            cancel_pending_task(not_done=not_done)
            raise KeyboardInterrupt


def setup_driver():
    try:
        cwd = os.getcwd()

        osname, exe_name, driver_path = download_driver(patched_drivers=patched_drivers)

        dst_path = os.path.join(cwd, f"chromedriver{exe_name}")

        if os.path.abspath(driver_path) != os.path.abspath(dst_path):
            if os.path.exists(dst_path):
                os.remove(dst_path)
            shutil.copy2(driver_path, dst_path)
            print(f"Copied driver to {dst_path}")

        if osname != "Windows":
            os.chmod(dst_path, 0o755)

        return osname, exe_name, dst_path

    except Exception as e:
        print(f"Error setting up driver: {e}")
        sys.exit(1)


if __name__ == "__main__":
    clean_exe_temp(folder="youtube_viewer")
    date_fmt = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    cpu_usage = str(psutil.cpu_percent(1))
    update_chrome_version()
    check_update()

    if os.path.isfile(config_path):
        with open(config_path, "r", encoding="utf-8-sig") as openfile:
            config = json.load(openfile)
        max_threads = config.get("max_threads", 10)

        if len(config) == 11:
            print(json.dumps(config, indent=4))
            print(
                bcolors.OKCYAN
                + "Config file exists! Program will start automatically after 10 seconds..."
                + bcolors.ENDC
            )
            print(
                bcolors.FAIL
                + "If you want to create a new config file PRESS CTRL+C within 10 seconds!"
                + bcolors.ENDC
            )
            start = get_time() + 10
            try:
                i = 0
                while get_time() < start:
                    remaining = start - get_time()
                    print(
                        bcolors.OKBLUE
                        + f"{remaining:.0f} seconds remaining "
                        + animation[i % len(animation)]
                        + bcolors.ENDC,
                        end="\r",
                    )
                    i += 1
                    sleep(0.2)
                print("\n")
            except KeyboardInterrupt:
                create_config(config_path=config_path)
        else:
            print(
                bcolors.FAIL
                + "Previous config file is not compatible with the latest script! Create a new one..."
                + bcolors.ENDC
            )
            create_config(config_path=config_path)
    else:
        create_config(config_path=config_path)

    osname, exe_name, driver_path = setup_driver()

    create_database(database=DATABASE, database_backup=DATABASE_BACKUP)

    if osname == "Windows":
        import wmi

        constructor = wmi.WMI()

    urls = load_url()
    queries = load_search()

    hash_urls = get_hash("urls.txt")
    hash_queries = get_hash("search.txt")
    hash_config = get_hash(config_path)

    while len(view) < views:
        try:
            with open(config_path, "r", encoding="utf-8-sig") as openfile:
                config = json.load(openfile)

            if cancel_all:
                print(json.dumps(config, indent=4))
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
            if minimum >= maximum:
                minimum = maximum - 5

            if min_threads >= max_threads:
                max_threads = min_threads

            if auth_required and background:
                print(
                    bcolors.FAIL
                    + "Premium proxy needs extension to work. Chrome doesn't support extension in Headless mode."
                    + bcolors.ENDC
                )
                input(
                    bcolors.WARNING
                    + f"Either use proxy without username & password or disable headless mode "
                    + bcolors.ENDC
                )
                sys.exit()

            copy_drivers(
                cwd=os.getcwd(),
                patched_drivers=patched_drivers,
                exe=exe_name,
                total=max_threads,
            )

            main()
        except KeyboardInterrupt:
            sys.exit()
