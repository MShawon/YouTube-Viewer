import os
import zipfile
from glob import glob

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from .features import *


WEBRTC = os.path.join('extension', 'webrtc_control.zip')
ACTIVE = os.path.join('extension', 'always_active.zip')
FINGERPRINT = os.path.join('extension', 'fingerprint_defender.zip')
TIMEZONE = os.path.join('extension', 'spoof_timezone.zip')
CUSTOM_EXTENSIONS = glob(os.path.join('extension', 'custom_extension', '*.zip')) + \
    glob(os.path.join('extension', 'custom_extension', '*.crx'))


def get_driver(background, viewports, agent, auth_required, path, proxy, proxy_type, pluginfile):
    options = webdriver.ChromeOptions()
    options.headless = background
    options.add_argument(f"--window-size={choice(viewports)}")
    options.add_argument("--log-level=3")
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option(
        'prefs', {'intl.accept_languages': 'en_US,en'})
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

    driver = webdriver.Chrome(executable_path=path, options=options)

    return driver


def play_video(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, '[title^="Pause (k)"]')
    except:
        try:
            driver.find_element(
                By.CSS_SELECTOR, 'button.ytp-large-play-button.ytp-button').send_keys(Keys.ENTER)
        except:
            try:
                driver.find_element(
                    By.CSS_SELECTOR, '[title^="Play (k)"]').click()
            except:
                try:
                    driver.execute_script(
                        "document.querySelector('button.ytp-play-button.ytp-button').click()")
                except:
                    pass

    try:
        skip_ad = driver.find_element(
            By.CLASS_NAME, "ytp-ad-skip-button-container")
        skip_ad.click()
    except:
        pass


def play_music(driver):
    try:
        driver.find_element(
            By.XPATH, '//*[@id="play-pause-button" and @title="Pause"]')
    except:
        try:
            driver.find_element(
                By.XPATH, '//*[@id="play-pause-button" and @title="Play"]').click()
        except:
            driver.execute_script(
                'document.querySelector("#play-pause-button").click()')


def type_keyword(driver, keyword, retry=False):
    input_keyword = driver.find_element(By.CSS_SELECTOR, 'input#search')

    if retry:
        for _ in range(10):
            try:
                input_keyword.click()
                break
            except:
                sleep(5)
                pass

    input_keyword.clear()
    for letter in keyword:
        input_keyword.send_keys(letter)
        sleep(uniform(.1, .4))

    method = randint(1, 2)
    if method == 1:
        input_keyword.send_keys(Keys.ENTER)
    else:
        try:
            driver.find_element(
                By.XPATH, '//*[@id="search-icon-legacy"]').click()
        except:
            driver.execute_script(
                'document.querySelector("#search-icon-legacy").click()')


def search_video(driver, keyword, video_title):
    i = 0
    try:
        type_keyword(driver, keyword)
    except:
        try:
            bypass_popup(driver)
            type_keyword(driver, keyword, retry=True)
        except:
            return i

    for i in range(1, 11):
        try:
            section = WebDriverWait(driver, 60).until(EC.visibility_of_element_located(
                (By.XPATH, f'//ytd-item-section-renderer[{i}]')))
            find_video = section.find_element(
                By.XPATH, f'//*[@title="{video_title}"]')
            driver.execute_script(
                "arguments[0].scrollIntoViewIfNeeded();", find_video)
            sleep(1)
            bypass_popup(driver)
            try:
                find_video.click()
            except:
                driver.execute_script(
                    "arguments[0].click();", find_video)
            break
        except NoSuchElementException:
            sleep(5)
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                (By.TAG_NAME, 'body'))).send_keys(Keys.CONTROL, Keys.END)

    return i
