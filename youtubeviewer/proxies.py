from random import shuffle

import requests

from .colors import *


def gather_proxy():
    proxies = []
    print(bcolors.OKGREEN + 'Scraping proxies ...' + bcolors.ENDC)

    link_list = ['https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
                 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
                 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt',
                 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt',
                 'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt',
                 'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt']

    for link in link_list:
        response = requests.get(link)
        output = response.content.decode()
        proxy = output.split('\n')
        proxies = proxies + proxy
        print(bcolors.OKGREEN +
              f'{len(proxy)} proxies gathered from {link}' + bcolors.ENDC)

    proxies = list(filter(None, proxies))
    shuffle(proxies)

    return proxies


def load_proxy(filename):
    proxies = []

    if not os.path.isfile(filename) and filename[-4:] != '.txt':
        filename = f'{filename}.txt'

    with open(filename, encoding="utf-8") as fh:
        loaded = [x.strip() for x in fh if x.strip() != '']

    for lines in loaded:
        if lines.count(':') == 3:
            split = lines.split(':')
            lines = f'{split[2]}:{split[-1]}@{split[0]}:{split[1]}'
        proxies.append(lines)

    proxies = list(filter(None, proxies))
    shuffle(proxies)

    return proxies


def scrape_api(link):
    proxies = []

    response = requests.get(link)
    output = response.content.decode()
    if '\r\n' in output:
        proxy = output.split('\r\n')
    else:
        proxy = output.split('\n')

    for lines in proxy:
        if lines.count(':') == 3:
            split = lines.split(':')
            lines = f'{split[2]}:{split[-1]}@{split[0]}:{split[1]}'
        proxies.append(lines)

    proxies = list(filter(None, proxies))
    shuffle(proxies)

    return proxies


def check_proxy(category, agent, proxy, proxy_type):
    if category == 'f':
        headers = {
            'User-Agent': f'{agent}',
        }

        proxy_dict = {
            "http": f"{proxy_type}://{proxy}",
            "https": f"{proxy_type}://{proxy}",
        }
        response = requests.get(
            'https://www.youtube.com/', headers=headers, proxies=proxy_dict, timeout=30)
        status = response.status_code

    else:
        status = 200

    return status