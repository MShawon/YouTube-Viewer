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
import time
from glob import glob
from random import choice, randint, uniform
from time import time, sleep
from .bypass import bypass_ads, bypass_other_popups, bypass_popup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .features import *

WEBRTC = os.path.join("extension", "webrtc_control.zip")
ACTIVE = os.path.join("extension", "always_active.zip")
FINGERPRINT = os.path.join("extension", "fingerprint_defender.zip")
CUSTOM_EXTENSIONS = glob(os.path.join("extension", "custom_extension", "*.zip")) + glob(
    os.path.join("extension", "custom_extension", "*.crx")
)


def create_proxy_folder(proxy, folder_name):
    proxy = proxy.replace("@", ":")
    proxy = proxy.split(":")
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
""" % (
        proxy[2],
        proxy[-1],
        proxy[0],
        proxy[1],
    )

    os.makedirs(folder_name, exist_ok=True)
    with open(os.path.join(folder_name, "manifest.json"), "w") as fh:
        fh.write(manifest_json)

    with open(os.path.join(folder_name, "background.js"), "w") as fh:
        fh.write(background_js)


def get_driver(
    background, viewports, agent, auth_required, path, proxy, proxy_type, proxy_folder
):
    options = Options()
    options.headless = background
    if viewports:
        options.add_argument(f"--window-size={choice(viewports)}")
    options.add_argument("--log-level=3")
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"]
    )
    options.add_experimental_option("useAutomationExtension", False)
    prefs = {
        "intl.accept_languages": "en_US,en",
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "download_restrictions": 3,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("extensionLoadTimeout", 120000)
    options.add_argument(f"user-agent={agent}")
    options.add_argument("--mute-audio")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-features=UserAgentClientHint")
    options.add_argument("--disable-web-security")

    if not background:
        options.add_extension(WEBRTC)
        options.add_extension(FINGERPRINT)
        options.add_extension(ACTIVE)

        if CUSTOM_EXTENSIONS:
            for extension in CUSTOM_EXTENSIONS:
                options.add_extension(extension)

    if auth_required:
        create_proxy_folder(proxy, proxy_folder)
        options.add_argument(f"--load-extension={proxy_folder}")
    else:
        options.add_argument(f"--proxy-server={proxy_type}://{proxy}")

    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def play_video(driver):
    try:
        if "consent.youtube.com" in driver.current_url:
            handle_consent_page(driver)
            sleep(2)

        bypass_other_popups(driver)

        if driver.execute_script("return document.querySelector('video') !== null"):
            bypass_ads(driver)

        for _ in range(5):
            video_duration = driver.execute_script(
                """
                const video = document.querySelector('video');
                return video && !isNaN(video.duration) ? video.duration : 0;
                """
            )
            if video_duration > 0:
                break
            sleep(1)

        if video_duration <= 0:
            return True

        try:
            import os
            import json

            config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
            with open(config_path, "r", encoding="utf-8-sig") as f:
                config = json.load(f)

            min_watch_percentage = float(config.get("minimum", 85))
            max_watch_percentage = float(config.get("maximum", 95))
        except Exception:
            min_watch_percentage = 85
            max_watch_percentage = 95

        min_watch_time = (video_duration * min_watch_percentage) / 100
        max_watch_time = (video_duration * max_watch_percentage) / 100

        start_time = time()
        last_popup_check = time()
        last_ad_check = time()
        popup_interval = 5
        ad_interval = 3

        from random import random

        while True:
            current_time = time()
            elapsed_time = current_time - start_time

            if elapsed_time >= max_watch_time:
                break

            if elapsed_time >= min_watch_time and random() < 0.1:
                break

            if current_time - last_popup_check >= popup_interval:
                bypass_other_popups(driver)
                last_popup_check = current_time

            if current_time - last_ad_check >= ad_interval:
                if driver.execute_script(
                    "return document.querySelector('video') !== null"
                ):
                    bypass_ads(driver)
                last_ad_check = current_time

            sleep(1)

        return True

    except Exception:
        return False


def handle_consent_page(driver):
    try:
        selectors = [
            "button[aria-label='Accept all']",
            "button.VfPpkd-LgbsSe-OWXEXe-k8QpJ",
            "form[action*='consent.youtube.com'] button",
        ]

        for selector in selectors:
            try:
                button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                button.click()
                sleep(2)
                return True
            except Exception:
                continue

        return False

    except Exception:
        return False


def play_music(driver):
    try:
        driver.find_element(By.XPATH, '//*[@id="play-pause-button" and @title="Pause"]')
    except WebDriverException:
        try:
            driver.find_element(
                By.XPATH, '//*[@id="play-pause-button" and @title="Play"]'
            ).click()
        except WebDriverException:
            driver.execute_script(
                'document.querySelector("#play-pause-button").click()'
            )

    skip_again(driver)


def type_keyword(driver, keyword, retry=False):
    if retry:
        for _ in range(30):
            try:
                driver.find_element(By.CSS_SELECTOR, "input#search").click()
                break
            except WebDriverException:
                sleep(3)

    input_keyword = driver.find_element(By.CSS_SELECTOR, "input#search")
    input_keyword.clear()
    for letter in keyword:
        input_keyword.send_keys(letter)
        sleep(uniform(0.1, 0.4))

    method = randint(1, 2)
    if method == 1:
        input_keyword.send_keys(Keys.ENTER)
    else:
        icon = driver.find_element(By.XPATH, '//button[@id="search-icon-legacy"]')
        ensure_click(driver, icon)


def scroll_search(driver, video_title):
    msg = None
    for i in range(1, 11):
        try:
            section = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//ytd-item-section-renderer[{i}]")
                )
            )
            if (
                driver.find_element(By.XPATH, f"//ytd-item-section-renderer[{i}]").text
                == "No more results"
            ):
                msg = "failed"
                break

            if len(video_title) == 11:
                find_video = section.find_element(
                    By.XPATH,
                    f'//a[@id="video-title" and contains(@href, "{video_title}")]',
                )
            else:
                find_video = section.find_element(
                    By.XPATH, f'//*[@title="{video_title}"]'
                )

            driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", find_video)
            sleep(1)
            bypass_popup(driver)
            ensure_click(driver, find_video)
            msg = "success"
            break
        except NoSuchElementException:
            sleep(randint(2, 5))
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.TAG_NAME, "body"))
            ).send_keys(Keys.CONTROL, Keys.END)

    if i == 10:
        msg = "failed"

    return msg


def search_video(driver, keyword, video_title):
    try:
        type_keyword(driver, keyword)
    except WebDriverException:
        try:
            bypass_popup(driver)
            type_keyword(driver, keyword, retry=True)
        except WebDriverException:
            return "failed"

    msg = scroll_search(driver, video_title)

    if msg == "failed":
        bypass_popup(driver)

        filters = driver.find_element(By.CSS_SELECTOR, "#filter-menu button")
        driver.execute_script("arguments[0].scrollIntoViewIfNeeded()", filters)
        sleep(randint(1, 3))
        ensure_click(driver, filters)

        sleep(randint(1, 3))
        sort = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[@title="Sort by upload date"]')
            )
        )
        ensure_click(driver, sort)

        msg = scroll_search(driver, video_title)

    return msg
