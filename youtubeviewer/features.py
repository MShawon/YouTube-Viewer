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
from .bypass import *

COMMANDS = [Keys.UP, Keys.DOWN, 'share', 'k', 'j', 'l', 't', 'c']

QUALITY = {
    1: ['144p', "tiny"],
    2: ['240p', "small"],
    3: ['360p', "medium"]
}


def skip_again(driver):
    try:
        skip_ad = driver.find_element(
            By.CLASS_NAME, "ytp-ad-skip-button-container")
        driver.execute_script("arguments[0].click();", skip_ad)
    except WebDriverException:
        pass


def skip_initial_ad(driver, video, duration_dict):
    video_len = duration_dict.get(video, 0)
    if video_len > 30:
        bypass_popup(driver)
        try:
            skip_ad = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                (By.CLASS_NAME, "ytp-ad-skip-button-container")))

            ad_duration = driver.find_element(
                By.CLASS_NAME, 'ytp-time-duration').get_attribute('innerText')
            ad_duration = sum(x * int(t)
                              for x, t in zip([60, 1], ad_duration.split(":")))
            ad_duration = ad_duration * uniform(.01, .1)
            sleep(ad_duration)
            skip_ad.click()
        except WebDriverException:
            skip_again(driver)


def save_bandwidth(driver):
    quality_index = choices([1, 2, 3], cum_weights=(0.7, 0.9, 1.00), k=1)[0]
    try:
        random_quality = QUALITY[quality_index][0]
        driver.find_element(
            By.CSS_SELECTOR, "button.ytp-button.ytp-settings-button").click()
        driver.find_element(
            By.XPATH, "//div[contains(text(),'Quality')]").click()

        quality = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"//span[contains(string(),'{random_quality}')]")))
        driver.execute_script(
            "arguments[0].scrollIntoViewIfNeeded();", quality)
        quality.click()

    except WebDriverException:
        try:
            random_quality = QUALITY[quality_index][1]
            driver.execute_script(
                f"document.getElementById('movie_player').setPlaybackQualityRange('{random_quality}')")
        except WebDriverException:
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
                    f'document.querySelector("#comments").{choice(["scrollIntoView", "scrollIntoViewIfNeeded"])}();')
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
    except WebDriverException:
        pass


def wait_for_new_page(driver, previous_url=False, previous_title=False):
    for _ in range(30):
        sleep(1)
        if previous_url:
            if driver.current_url != previous_url:
                break
        elif previous_title:
            if driver.title != previous_title:
                break


def play_next_video(driver, suggested):
    shuffle(suggested)
    video_id = choice(suggested)

    for _ in range(10):
        if video_id in driver.current_url:
            video_id = choice(suggested)
        else:
            break

    try:
        driver.execute_script(
            'document.querySelector("tp-yt-paper-button#expand").click()')
        js = f'''
        var html = '<a class="yt-simple-endpoint style-scope yt-formatted-string" ' +
        'spellcheck="false" href="/watch?v={video_id}&t=0s" ' +
        'dir="auto">https://www.youtube.com/watch?v={video_id}</a><br>'

        var element = document.querySelector("#description > ytd-text-inline-expander > yt-formatted-string");

        element.insertAdjacentHTML( 'afterbegin', html );
        '''
    except WebDriverException:
        js = f'''
        var html = '<a class="yt-simple-endpoint style-scope yt-formatted-string" ' +
        'spellcheck="false" href="/watch?v={video_id}&t=0s" ' +
        'dir="auto">https://www.youtube.com/watch?v={video_id}</a><br>'

        var elements = document.querySelectorAll("#description > yt-formatted-string");
        var element = elements[elements.length- 1];

        element.insertAdjacentHTML( 'afterbegin', html );
        '''

    driver.execute_script(js)

    find_video = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
        (By.XPATH, f'//a[@href="/watch?v={video_id}&t=0s"]')))
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", find_video)

    previous_title = driver.title
    driver.execute_script("arguments[0].click();", find_video)
    wait_for_new_page(driver=driver, previous_url=False,
                      previous_title=previous_title)

    return driver.title[:-10]


def play_from_channel(driver, actual_channel):
    channel = driver.find_elements(
        By.CSS_SELECTOR, 'ytd-video-owner-renderer a')[randint(0, 1)]
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", channel)
    previous_title = driver.title
    driver.execute_script("arguments[0].click();", channel)
    wait_for_new_page(driver=driver, previous_url=False,
                      previous_title=previous_title)

    channel_name = driver.title[:-10]

    if randint(1, 2) == 1:
        if channel_name != actual_channel:
            raise Exception(
                f"Accidentally opened another channel : {channel_name}. Closing it...")

        x = randint(30, 50)
        sleep(x)
        output = driver.find_element(
            By.XPATH, '//yt-formatted-string[@id="title"]/a').text
        log = f'Video [{output}] played for {x} seconds from channel home page : {channel_name}'
        option = 4
    else:
        sleep(randint(2, 5))
        previous_url = driver.current_url
        driver.find_element(By.XPATH, "//tp-yt-paper-tab[2]").click()
        wait_for_new_page(driver=driver, previous_url=previous_url,
                          previous_title=False)

        driver.refresh()
        videos = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@id='video-title']")))
        video = choice(videos)
        driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", video)
        sleep(randint(2, 5))
        previous_title = driver.title
        ensure_click(driver, video)
        wait_for_new_page(driver=driver, previous_url=False,
                          previous_title=previous_title)

        output = driver.title[:-10]
        log = f'Random video [{output}] played from channel : {channel_name}'
        option = 2

        channel_name = driver.find_element(
            By.CSS_SELECTOR, '#upload-info a').text
        if channel_name != actual_channel:
            raise Exception(
                f"Accidentally opened video {output} from another channel : {channel_name}. Closing it...")

    return output, log, option


def play_end_screen_video(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, '[title^="Pause (k)"]')
        driver.find_element(By.ID, 'movie_player').send_keys('k')
    except WebDriverException:
        pass

    total = driver.execute_script(
        "return document.getElementById('movie_player').getDuration()")
    driver.execute_script(
        f"document.querySelector('#movie_player').seekTo({total}-{randint(2,5)})")
    end_screen = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(
        (By.XPATH, "//*[@class='ytp-ce-covering-overlay']")))
    previous_title = driver.title
    sleep(randint(2, 5))
    if end_screen:
        ensure_click(driver, choice(end_screen))
    else:
        raise Exception(
            f'Unfortunately no end screen video found on this video : {previous_title[:-10]}')
    wait_for_new_page(driver=driver, previous_url=False,
                      previous_title=previous_title)

    return driver.title[:-10]
