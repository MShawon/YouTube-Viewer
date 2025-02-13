"""
MIT License

Copyright (c) 2021-2023 MShawon

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

import random
from random import choice, choices, randint, shuffle, uniform
from time import sleep
from datetime import datetime
from .colors import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def ensure_click(driver, element):
    try:
        element.click()
    except WebDriverException:
        driver.execute_script("arguments[0].click();", element)


def personalization(driver):
    search = driver.find_element(
        By.XPATH,
        f'//button[@aria-label="Turn {choice(["on","off"])} Search customization"]',
    )
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", search)
    search.click()

    history = driver.find_element(
        By.XPATH, f'//button[@aria-label="Turn {choice(["on","off"])} YouTube History"]'
    )
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", history)
    history.click()

    ad = driver.find_element(
        By.XPATH,
        f'//button[@aria-label="Turn {choice(["on","off"])} Ad personalization"]',
    )
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", ad)
    ad.click()

    confirm = driver.find_element(By.XPATH, '//button[@jsname="j6LnYe"]')
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", confirm)
    confirm.click()


def bypass_consent(driver):
    try:
        if "consent.youtube.com" in driver.current_url:
            driver.execute_script(
                """
                const consentOverlay = document.querySelector('div[role="dialog"]');
                if(consentOverlay) consentOverlay.remove();
                
                const cookies = {
                    'CONSENT': 'YES+yt.432951.en+FX+' + Math.floor(Date.now()/1000),
                    'SOCS': 'CAISNAlYLmlOX19pZC4yMDIzLTAyLTA0LTE4LTEwLnByb2QtZmluYWwtZXUtd2VzdC0xLmxpZ2h0',
                    '__Secure-YEC': Math.floor(Date.now()/1000),
                };
                
                Object.entries(cookies).forEach(([name, value]) => {
                    document.cookie = `${name}=${value}; domain=.youtube.com; path=/; secure; SameSite=None`;
                });
            """
            )

            consent_buttons = [
                "button[jsname='j6LnYe']",
                "button[jsname='tHlp8d']",
                "#accept-button",
                "button.VfPpkd-LgbsSe",
                "[aria-label*='Accept']",
                "button:has-text('Accept all')",
                "form[action*='consent'] button",
                "button[jsname='b3VHJd']",
            ]

            for selector in consent_buttons:
                try:
                    buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        if button.is_displayed():
                            driver.execute_script("arguments[0].click();", button)
                            sleep(0.5)
                except:
                    continue

            if "consent.youtube.com" in driver.current_url:
                original_url = driver.current_url.split("continue=")[1].split("&")[0]
                if original_url:
                    driver.get(original_url)

    except Exception as e:
        print(f"Consent bypass error: {str(e)}")


def bypass_ads(driver):
    try:
        if not driver.execute_script(
            "return document.querySelector('.ad-showing') !== null"
        ):
            return

        try:
            skip_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".ytp-ad-skip-button"))
            )
            driver.execute_script("arguments[0].click();", skip_button)
            return
        except:
            pass

        driver.execute_script(
            """
            const video = document.querySelector('video');
            if(video && document.querySelector('.ad-showing')) {
                const duration = video.duration;
                if (duration && isFinite(duration)) {
                    video.currentTime = duration;
                }
            }
        """
        )

    except Exception:
        pass


def bypass_other_popups(driver):
    try:
        popup_selectors = {
            "consent": "button[aria-label='Accept all']",
            "no_thanks": "button[aria-label='No thanks']",
            "dismiss": "button[aria-label='Dismiss']",
            "maybe_later": "button[aria-label='Maybe later']",
            "close": "button[aria-label='Close']",
            "got_it": "button[aria-label='Got it']",
            "reject": "button[aria-label='Reject all']",
            "skip_trial": "button[aria-label='Skip trial']",
            "not_now": "button[aria-label='Not now']",
        }

        for purpose, selector in popup_selectors.items():
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if (
                        "player" in element.get_attribute("class").lower()
                        or "player" in element.get_attribute("id").lower()
                        or not element.is_displayed()
                    ):
                        continue

                    driver.execute_script("arguments[0].click();", element)
                    sleep(3)
                    return True
            except:
                continue

        return False

    except Exception:
        return False


def bypass_other_popups(driver):
    try:
        common_buttons = [
            "button[aria-label='No thanks']",
            "button[aria-label='Dismiss']",
            ".yt-spec-button-shape-next--filled",
        ]

        for selector in common_buttons:
            try:
                button = driver.find_element(By.CSS_SELECTOR, selector)
                if button.is_displayed():
                    driver.execute_script("arguments[0].click();", button)
                    sleep(1)
            except:
                continue

    except Exception:
        pass


def click_popup(driver, element):
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", element)
    sleep(1)
    element.click()


def bypass_popup(driver):
    for _ in range(3):
        try:
            agree = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//*[@aria-label="Agree to the use of cookies and other data for the purposes described"]',
                    )
                )
            )
            click_popup(driver=driver, element=agree)
            return
        except WebDriverException:
            pass

        try:
            agree = driver.find_element(
                By.XPATH,
                f'//*[@aria-label="{choice(["Accept", "Reject"])} the use of cookies and other data for the purposes described"]',
            )
            click_popup(driver=driver, element=agree)
            return
        except WebDriverException:
            pass


def bypass_other_popup(driver):
    popups = ["Got it", "Skip trial", "No thanks", "Dismiss", "Not now"]
    shuffle(popups)

    for popup in popups:
        try:
            driver.find_element(
                By.XPATH, f"//*[@id='button' and @aria-label='{popup}']"
            ).click()
        except WebDriverException:
            pass

    try:
        driver.find_element(
            By.XPATH, '//*[@id="dismiss-button"]/yt-button-shape/button'
        ).click()
    except WebDriverException:
        pass


def bypass_stuck_page(driver, urls, position):
    try:
        if not urls:
            return None

        current_url = driver.current_url

        if (
            current_url == "https://www.youtube.com/"
            or "accounts.google.com" in current_url
        ):
            shuffled_urls = list(urls)
            random.shuffle(shuffled_urls)

            for url in shuffled_urls:
                driver.get(url)
                sleep(2)

                if "accounts.google.com" not in driver.current_url:
                    return url
                else:
                    continue

            return None

        return current_url

    except Exception:
        return None
