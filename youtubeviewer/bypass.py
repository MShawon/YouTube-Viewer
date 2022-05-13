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
from random import choice, choices, randint, shuffle, uniform
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        WebDriverException)
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
        By.XPATH, f'//button[@aria-label="Turn {choice(["on","off"])} Search customization"]')
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", search)
    search.click()

    history = driver.find_element(
        By.XPATH, f'//button[@aria-label="Turn {choice(["on","off"])} YouTube History"]')
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", history)
    history.click()

    ad = driver.find_element(
        By.XPATH, f'//button[@aria-label="Turn {choice(["on","off"])} Ad personalization"]')
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", ad)
    ad.click()

    confirm = driver.find_element(By.XPATH, '//button[@jsname="j6LnYe"]')
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", confirm)
    confirm.click()


def bypass_consent(driver):
    try:
        consent = driver.find_element(By.XPATH, "//button[@jsname='higCR']")
        driver.execute_script("arguments[0].scrollIntoView();", consent)
        consent.click()
        if 'consent' in driver.current_url:
            personalization(driver)
    except WebDriverException:
        consent = driver.find_element(
            By.XPATH, "//input[@type='submit' and @value='I agree']")
        driver.execute_script("arguments[0].scrollIntoView();", consent)
        consent.submit()
        if 'consent' in driver.current_url:
            personalization(driver)


def click_popup(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoViewIfNeeded();", element)
    sleep(1)
    element.click()


def bypass_popup(driver):
    try:
        agree = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@aria-label="Agree to the use of cookies and other data for the purposes described"]')))
        click_popup(driver=driver, element=agree)
    except WebDriverException:
        try:
            agree = driver.find_element(
                By.XPATH, f'//*[@aria-label="{choice(["Accept","Reject"])} the use of cookies and other data for the purposes described"]')
            click_popup(driver=driver, element=agree)
        except WebDriverException:
            pass


def bypass_other_popup(driver):
    popups = ['Got it', 'Skip trial', 'No thanks', 'Dismiss', 'Not now']
    shuffle(popups)

    for popup in popups:
        try:
            driver.find_element(
                By.XPATH, f"//*[@id='button' and @aria-label='{popup}']").click()
        except WebDriverException:
            pass
