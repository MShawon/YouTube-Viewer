from random import choices, randint, uniform

from selenium.webdriver.common.keys import Keys

from .bypass import *

COMMANDS = [Keys.UP, Keys.DOWN, 'share', 'k', 'j', 'l', 't', 'c']


def skip_initial_ad(driver, video, duration_dict):
    try:
        video_len = duration_dict[video]
        if video_len > 30:
            bypass_popup(driver)
            skip_ad = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                (By.CLASS_NAME, "ytp-ad-skip-button-container")))

            ad_duration = driver.find_element(
                By.CLASS_NAME, 'ytp-time-duration').get_attribute('innerText')
            ad_duration = sum(x * int(t)
                              for x, t in zip([60, 1], ad_duration.split(":")))
            ad_duration = ad_duration * uniform(.01, .1)
            sleep(ad_duration)
            skip_ad.click()
    except:
        pass


def save_bandwidth(driver):
    try:
        driver.find_element(
            By.CSS_SELECTOR, "button.ytp-button.ytp-settings-button").click()
        driver.find_element(
            By.XPATH, "//div[contains(text(),'Quality')]").click()

        random_quality = choices(
            ['144p', '240p', '360p'], cum_weights=(0.7, 0.9, 1.00), k=1)[0]
        quality = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"//span[contains(string(),'{random_quality}')]")))
        driver.execute_script(
            "arguments[0].scrollIntoViewIfNeeded();", quality)
        quality.click()

    except:
        try:
            driver.find_element(
                By.XPATH, '//*[@id="container"]/h1/yt-formatted-string').click()
        except:
            pass


def change_playback_speed(driver, playback_speed):
    if playback_speed == 2:
        driver.find_element(By.ID, 'movie_player').send_keys('<'*randint(1, 3))
    elif playback_speed == 3:
        driver.find_element(By.ID, 'movie_player').send_keys('>'*randint(1, 3))


def random_command(driver):
    try:
        bypass_other_popup(driver)

        option = choices([1, 2], cum_weights=(0.7, 1.00), k=1)[0]
        if option == 2:
            command = choice(COMMANDS)
            if command in ['m', 't', 'c']:
                driver.find_element(By.ID, 'movie_player').send_keys(command)
            elif command == 'k':
                if randint(1, 2) == 1:
                    driver.find_element(
                        By.ID, 'movie_player').send_keys(command)
                driver.execute_script(
                    f'document.querySelector("#comments"){choices(["scrollIntoView", "scrollIntoViewIfNeeded"])}();')
                sleep(uniform(4, 10))
                driver.execute_script(
                    'document.querySelector("#movie_player").scrollIntoViewIfNeeded();')
            elif command == 'share':
                driver.find_element(
                    By.XPATH, "//button[@id='button' and @aria-label='Share']").click()
                sleep(uniform(2, 5))
                if randint(1, 2) == 1:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, "//*[@id='button' and @aria-label='Copy']"))).click()
                driver.find_element(
                    By.XPATH, "//*[@id='close-button']/button[@aria-label='Cancel']").click()
            else:
                driver.find_element(By.ID,
                                    'movie_player').send_keys(command*randint(1, 5))
    except:
        pass


def play_next_video(driver, suggested):
    shuffle(suggested)
    video_id = choice(suggested)

    for _ in range(10):
        if video_id in driver.current_url:
            video_id = choice(suggested)
        else:
            break

    js = f'''
    var html = '<a class="yt-simple-endpoint style-scope yt-formatted-string" ' +
    'spellcheck="false" href="/watch?v={video_id}&t=0s" ' +
    'dir="auto">https://www.youtube.com/watch?v={video_id}</a><br>'

    var element = document.querySelector("#description > yt-formatted-string")

    element.insertAdjacentHTML( 'afterbegin', html );
    '''

    driver.execute_script(js)

    find_video = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
        (By.XPATH, f'//a[@href="/watch?v={video_id}&t=0s"]')))
    driver.execute_script(
        "arguments[0].scrollIntoViewIfNeeded();", find_video)

    try:
        find_video.click()
    except:
        driver.execute_script(
            "arguments[0].click();", find_video)

    sleep(10)
    video_title = driver.title[:-10]

    return video_title