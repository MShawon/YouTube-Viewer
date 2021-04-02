"""
MIT License

Copyright (c) 2021 MShawon

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

import concurrent.futures.thread
import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from fake_useragent import UserAgent, UserAgentError

os.system("")


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(bcolors.OKGREEN + """
  ____                                    
 |  _ \ _ __ _____  ___   _               
 | |_) | '__/ _ \ \/ / | | |              
 |  __/| | | (_) >  <| |_| |              
 |_|   |_|_ \___/_/\_\\__, |_             
      / ___| |__   ___|___/| | _____ _ __ 
     | |   | '_ \ / _ \/ __| |/ / _ \ '__|
     | |___| | | |  __/ (__|   <  __/ |   
      \____|_| |_|\___|\___|_|\_\___|_|   
                                          
""" + bcolors.ENDC)

'''
Backup previous checked goodproxies
'''
try:
    os.remove('ProxyBackup.txt')
except:
    pass

try:
    shutil.copy('GoodProxy.txt', 'ProxyBackup.txt')
    print(bcolors.WARNING + 'GoodProxy backed up in ProxyBackup' + bcolors.ENDC)
    os.remove('GoodProxy.txt')
except:
    pass

try:
    ua = UserAgent(use_cache_server=False, verify_ssl=False)
except UserAgentError:
    ua = UserAgent(path='fake_useragent_0.1.11.json')

checked = {}


def load_proxy():
    proxies = []

    filename = input(bcolors.OKBLUE +
                     'Enter your proxy file name: ' + bcolors.ENDC)
    load = open(filename)
    loaded = [items.rstrip().strip() for items in load]
    load.close()

    for lines in loaded:
        proxies.append(lines)

    return proxies


def mainChecker(type1, type2, proxy, position):

    checked[position] = None

    proxyDict = {
        "http": f"{type1}://"+proxy,
        "https": f"{type2}://"+proxy,
    }

    # print(proxyDict)
    try:
        agent = ua.random

        headers = {
            'User-Agent': f'{agent}',
        }

        response = requests.get(
            'https://www.youtube.com/', headers=headers, proxies=proxyDict, timeout=30)
        status = response.status_code

        print(bcolors.OKBLUE + f"Tried {position} |" + bcolors.OKGREEN +
              f' {proxy} | GOOD | Type : {type2} | Response : {status}' + bcolors.ENDC)

        print(proxy, file=open('GoodProxy.txt', 'a'))

    except:
        print(bcolors.OKBLUE + f"Tried {position} |" + bcolors.FAIL +
              f' {proxy} | {type2} |BAD ' + bcolors.ENDC)
        checked[position] = type2
        pass


def proxyCheck(position):

    PROXY = proxy_list[position]

    mainChecker('http', 'https', PROXY, position)
    if checked[position] == 'https':
        mainChecker('socks4', 'socks4', PROXY, position)
    if checked[position] == 'socks4':
        mainChecker('socks5', 'socks5', PROXY, position)


def main():
    pool_number = [i for i in range(total_proxies)]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(proxyCheck, position)
                   for position in pool_number]

        try:
            for future in as_completed(futures):
                future.result()
        except KeyboardInterrupt:
            executor._threads.clear()
            concurrent.futures.thread._threads_queues.clear()
        except IndexError:
            print(bcolors.WARNING + 'Number of proxies are less than threads. Provide more proxies or less threads.' + bcolors.ENDC)
            pass


if __name__ == '__main__':
    threads = int(
        input(bcolors.OKBLUE+'Threads (recommended = 100): ' + bcolors.ENDC))

    proxy_list = load_proxy()
    proxy_list = list(set(proxy_list))  # removing duplicate proxies
    proxy_list = list(filter(None, proxy_list))  # removing empty proxies

    total_proxies = len(proxy_list)
    print(bcolors.OKCYAN + f'Total proxies : {total_proxies}' + bcolors.ENDC)

    main()
