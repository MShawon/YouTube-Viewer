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
    import undetected_chromedriver as uc
    
    # Use undetected-chromedriver options
    options = uc.ChromeOptions()
    
    # Basic stealth settings
    if viewports:
        options.add_argument(f"--window-size={choice(viewports)}")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Remove problematic excludeSwitches - this causes the error in newer Chrome
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # User preferences
    prefs = {
        "intl.accept_languages": 'en_US,en',
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "download_restrictions": 3,
        "profile.default_content_settings.popups": 0
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option('extensionLoadTimeout', 120000)
    
    # Additional stealth arguments
    options.add_argument(f"--user-agent={agent}")
    options.add_argument("--mute-audio")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-features=UserAgentClientHint')
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-automation")  # Alternative to excludeSwitches
    
    # Set headless mode if needed
    if background:
        options.add_argument("--headless=new")
    else:
        # Add extensions only in non-headless mode
        try:
            options.add_extension(WEBRTC)
            options.add_extension(FINGERPRINT)
            options.add_extension(ACTIVE)

            if CUSTOM_EXTENSIONS:
                for extension in CUSTOM_EXTENSIONS:
                    options.add_extension(extension)
        except Exception as e:
            print(f"Warning: Could not load extensions: {e}")

    # Proxy configuration
    if auth_required:
        create_proxy_folder(proxy, proxy_folder)
        options.add_argument(f"--load-extension={proxy_folder}")
    else:
        options.add_argument(f'--proxy-server={proxy_type}://{proxy}')

    try:
        # Use undetected-chromedriver directly
        major_version = int(get_chrome_version().split('.')[0])
        driver = uc.Chrome(
            options=options,
            driver_executable_path=path if os.path.exists(path) else None,
            version_main=major_version,
            headless=background
        )
        
        # Additional stealth measures
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": agent,
            "acceptLanguage": "en-US,en;q=0.9",
            "platform": "Win32"
        })
        
        return driver
        
    except Exception as e:
        print(f"Error creating undetected Chrome driver: {e}")
        # Fallback to regular selenium with simpler options
        try:
            from selenium.webdriver.chrome.service import Service
            regular_options = webdriver.ChromeOptions()
            regular_options.add_argument("--log-level=3")
            regular_options.add_argument(f"--user-agent={agent}")
            regular_options.add_argument("--disable-automation")
            regular_options.add_argument("--no-sandbox")
            regular_options.add_argument("--disable-dev-shm-usage")
            
            if background:
                regular_options.add_argument("--headless=new")
            if not auth_required:
                regular_options.add_argument(f'--proxy-server={proxy_type}://{proxy}')
            
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service, options=regular_options)
            return driver
        except Exception as e2:
            print(f"Fallback also failed: {e2}")
            # Last resort: try with regular ChromeOptions
            try:
                from selenium.webdriver.chrome.service import Service
                minimal_options = webdriver.ChromeOptions()
                minimal_options.add_argument("--log-level=3")
                minimal_options.add_argument("--no-sandbox")
                if background:
                    minimal_options.add_argument("--headless=new")
                
                service = Service(executable_path=path)
                driver = webdriver.Chrome(service=service, options=minimal_options)
                return driver
            except Exception as e3:
                print(f"All driver creation methods failed: {e3}")
                raise e3


def get_chrome_version():
    """Helper function to get Chrome version"""
    import platform
    import subprocess
    
    try:
        osname = platform.system()
        if osname == 'Darwin':
            process = subprocess.Popen(
                ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            version = process.communicate()[0].decode('UTF-8').replace('Google Chrome', '').strip()
            return version
        elif osname == 'Linux':
            process = subprocess.Popen(['google-chrome-stable', '--version'], 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            version = process.communicate()[0].decode('utf-8').replace('Google Chrome', '').strip()
            return version
        else:
            # Default for Windows or unknown OS
            return "138.0.6464.175"
    except Exception:
        return "138.0.6464.175"


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
    i = 0
    for i in range(1, 11):
        try:
            section = WebDriverWait(driver, 60).until(EC.visibility_of_element_located(
                (By.XPATH, f'//ytd-item-section-renderer[{i}]')))
            if driver.find_element(By.XPATH, f'//ytd-item-section-renderer[{i}]').text == 'No more results':
                msg = 'failed'
                break

            if len(video_title) == 11:
                find_video = section.find_element(
                    By.XPATH, f'//a[@id="video-title" and contains(@href, "{video_title}")]')
            else:
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
                "Slow internet speed or Stuck at recaptcha! Can't perform search keyword")

    msg = scroll_search(driver, video_title)

    if msg == 'failed':
        bypass_popup(driver)

        filters = driver.find_element(By.CSS_SELECTOR, '#filter-menu button')
        driver.execute_script('arguments[0].scrollIntoViewIfNeeded()', filters)
        sleep(randint(1, 3))
        ensure_click(driver, filters)

        sleep(randint(1, 3))
        sort = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@title="Sort by upload date"]')))
        ensure_click(driver, sort)

        msg = scroll_search(driver, video_title)

    return msg
