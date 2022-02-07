from random import choice, shuffle
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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
    except:
        consent = driver.find_element(
            By.XPATH, "//input[@type='submit' and @value='I agree']")
        driver.execute_script("arguments[0].scrollIntoView();", consent)
        consent.submit()
        if 'consent' in driver.current_url:
            personalization(driver)


def bypass_signin(driver):
    for _ in range(10):
        sleep(2)
        try:
            nothanks = driver.find_element(
                By.CLASS_NAME, "style-scope.yt-button-renderer.style-text.size-small")
            nothanks.click()
            sleep(1)
            driver.switch_to.frame(driver.find_element(By.ID, "iframe"))
            iagree = driver.find_element(By.ID, 'introAgreeButton')
            iagree.click()
            driver.switch_to.default_content()
        except:
            try:
                driver.switch_to.frame(driver.find_element(By.ID, "iframe"))
                iagree = driver.find_element(By.ID, 'introAgreeButton')
                iagree.click()
                driver.switch_to.default_content()
            except:
                pass


def bypass_popup(driver):
    try:
        agree = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@aria-label="Agree to the use of cookies and other data for the purposes described"]')))
        driver.execute_script(
            "arguments[0].scrollIntoViewIfNeeded();", agree)
        sleep(1)
        agree.click()
    except:
        pass


def bypass_other_popup(driver):
    popups = ['Got it', 'Skip trial', 'No thanks', 'Dismiss', 'Not now']
    shuffle(popups)

    for popup in popups:
        try:
            driver.find_element(
                By.XPATH, f"//*[@id='button' and @aria-label='{popup}']").click()
        except:
            pass
