"""
MIT License

Copyright (c) 2021-2022 MShawon

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
import os
from glob import glob

from .features import *

WEBRTC = os.path.join('extension', 'webrtc_control.zip')
ACTIVE = os.path.join('extension', 'always_active.zip')
FINGERPRINT = os.path.join('extension', 'fingerprint_defender.zip')
TIMEZONE = os.path.join('extension', 'spoof_timezone.zip')
CUSTOM_EXTENSIONS = glob(os.path.join('extension', 'custom_extension', '*.zip')) + \
    glob(os.path.join('extension', 'custom_extension', '*.crx'))


def create_proxy_folder(proxy, folder_name):
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

    os.makedirs(folder_name, exist_ok=True)
    with open(os.path.join(folder_name, "manifest.json"), 'w') as fh:
        fh.write(manifest_json)

    with open(os.path.join(folder_name, "background.js"), 'w') as fh:
        fh.write(background_js)


def get_driver(background, viewports, agent, auth_required, path, proxy, proxy_type, proxy_folder):
    options = webdriver.ChromeOptions()
    options.headless = background
    if viewports:
        options.add_argument(f"--window-size={choice(viewports)}")
    options.add_argument("--log-level=3")
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    prefs = {"intl.accept_languages": 'en_US,en',
             "credentials_enable_service": False,
             "profile.password_manager_enabled": False,
             "profile.default_content_setting_values.notifications": 2,
             "download_restrictions": 3}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option('extensionLoadTimeout', 120000)
    options.add_argument(f"user-agent={agent}")
    options.add_argument("--mute-audio")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-features=UserAgentClientHint')
    options.add_argument("--disable-web-security")
    webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {
        'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

    if not background:
        options.add_extension(WEBRTC)
        options.add_extension(FINGERPRINT)
        options.add_extension(TIMEZONE)
        options.add_extension(ACTIVE)

        if CUSTOM_EXTENSIONS:
            for extension in CUSTOM_EXTENSIONS:
                options.add_extension(extension)

    if auth_required:
        create_proxy_folder(proxy, proxy_folder)
        options.add_argument(f"--load-extension={proxy_folder}")
    else:
        options.add_argument(f'--proxy-server={proxy_type}://{proxy}')

    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def play_video(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, '[title^="Pause (k)"]')
    except WebDriverException:
        try:
            driver.find_element(
                By.CSS_SELECTOR, 'button.ytp-large-play-button.ytp-button').send_keys(Keys.ENTER)
        except WebDriverException:
            try:
                driver.find_element(
                    By.CSS_SELECTOR, '[title^="Play (k)"]').click()
            except WebDriverException:
                try:
                    driver.execute_script(
                        "document.querySelector('button.ytp-play-button.ytp-button').click()")
                except WebDriverException:
                    pass

    skip_again(driver)


def play_music(driver):
    try:
        driver.find_element(
            By.XPATH, '//*[@id="play-pause-button" and @title="Pause"]')
    except WebDriverException:
        try:
            driver.find_element(
                By.XPATH, '//*[@id="play-pause-button" and @title="Play"]').click()
        except WebDriverException:
            driver.execute_script(
                'document.querySelector("#play-pause-button").click()')

    skip_again(driver)


def type_keyword(driver, keyword, retry=False):
    if retry:
        for _ in range(30):
            try:
                driver.find_element(By.CSS_SELECTOR, 'input#search').click()
                break
            except WebDriverException:
                sleep(3)

    input_keyword = driver.find_element(By.CSS_SELECTOR, 'input#search')
    input_keyword.clear()
    for letter in keyword:
        input_keyword.send_keys(letter)
        sleep(uniform(.1, .4))

    method = randint(1, 2)
    if method == 1:
        input_keyword.send_keys(Keys.ENTER)
    else:
        icon = driver.find_element(
            By.XPATH, '//button[@id="search-icon-legacy"]')
        ensure_click(driver, icon)


def scroll_search(driver, video_title):
    msg = None
    for i in range(1, 11):
        try:
            section = WebDriverWait(driver, 60).until(EC.visibility_of_element_located(
                (By.XPATH, f'//ytd-item-section-renderer[{i}]')))
            if driver.find_element(By.XPATH, f'//ytd-item-section-renderer[{i}]').text == 'No more results':
                msg = 'failed'
                break
            find_video = section.find_element(
                By.XPATH, f'//*[@title="{video_title}"]')
            driver.execute_script(
                "arguments[0].scrollIntoViewIfNeeded();", find_video)
            sleep(1)
            bypass_popup(driver)
            ensure_click(driver, find_video)
            msg = 'success'
            break
        except NoSuchElementException:
            sleep(randint(2, 5))
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                (By.TAG_NAME, 'body'))).send_keys(Keys.CONTROL, Keys.END)

    if i == 10:
        msg = 'failed'

    return msg


def search_video(driver, keyword, video_title):
    try:
        type_keyword(driver, keyword)
    except WebDriverException:
        try:
            bypass_popup(driver)
            type_keyword(driver, keyword, retry=True)
        except WebDriverException:
            raise Exception(
                "Slow internet speed or Stuck at recaptcha! Can't perfrom search keyword")

    msg = scroll_search(driver, video_title)

    if msg == 'failed':
        bypass_popup(driver)

        filters = driver.find_element(By.CSS_SELECTOR, '#filter-menu a')
        driver.execute_script('arguments[0].scrollIntoViewIfNeeded()', filters)
        sleep(randint(1, 3))
        ensure_click(driver, filters)

        sleep(randint(1, 3))
        sort = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@title="Sort by upload date"]')))
        ensure_click(driver, sort)

        msg = scroll_search(driver, video_title)

    return msg
