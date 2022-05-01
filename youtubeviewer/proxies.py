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
import sys
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

        if '\r\n' in output:
            proxy = output.split('\r\n')
        else:
            proxy = output.split('\n')

        for lines in proxy:
            for line in lines.split('\n'):
                proxies.append(line)

        print(bcolors.BOLD + f'{len(proxy)}' + bcolors.OKBLUE +
              ' proxies gathered from ' + bcolors.OKCYAN + f'{link}' + bcolors.ENDC)

    proxies = list(set(filter(None, proxies)))
    shuffle(proxies)

    return proxies


def load_proxy(filename):
    proxies = []

    if not os.path.isfile(filename) and filename[-4:] != '.txt':
        filename = f'{filename}.txt'

    try:
        with open(filename, encoding="utf-8") as fh:
            loaded = [x.strip() for x in fh if x.strip() != '']
    except Exception as e:
        print(bcolors.FAIL + str(e) + bcolors.ENDC)
        input('')
        sys.exit()

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

    try:
        response = requests.get(link)
        output = response.content.decode()
    except Exception as e:
        print(bcolors.FAIL + str(e) + bcolors.ENDC)
        input('')
        sys.exit()

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