"""
MIT License

Copyright (c) 2022 MShawon

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
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from glob import glob

import requests
from fake_headers import Headers

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

print(bcolors.OKCYAN + """
[ GitHub : https://github.com/MShawon/YouTube-Viewer ]
""" + bcolors.ENDC)


try:
    os.remove('ProxyBackup.txt')
except:
    pass

try:
    shutil.copy('GoodProxy.txt', 'ProxyBackup.txt')
    print(bcolors.WARNING + 'GoodProxy.txt backed up in ProxyBackup.txt' + bcolors.ENDC)
    os.remove('GoodProxy.txt')
except:
    pass

checked = {}


def clean_exe_temp(folder):
    try:
        temp_name = sys._MEIPASS.split('\\')[-1]
    except:
        temp_name = None

    for f in glob(os.path.join('temp', folder, '*')):
        if temp_name not in f:
            shutil.rmtree(f, ignore_errors=True)


def load_proxy():
    proxies = []

    filename = input(bcolors.OKBLUE +
                     'Enter your proxy file name: ' + bcolors.ENDC)

    if not os.path.isfile(filename) and filename[-4:] != '.txt':
        filename = f'{filename}.txt'

    with open(filename, encoding="utf-8") as fh:
        loaded = [x.strip() for x in fh if x.strip() != '']

    for lines in loaded:
        if lines.count(':') == 3:
            split = lines.split(':')
            lines = f'{split[2]}:{split[-1]}@{split[0]}:{split[1]}'
        proxies.append(lines)

    return proxies


def main_checker(proxy_type, proxy, position):

    checked[position] = None

    proxyDict = {
        "http": f"{proxy_type}://{proxy}",
        "https": f"{proxy_type}://{proxy}",
    }

    try:

        header = Headers(
            headers=False
        ).generate()
        agent = header['User-Agent']

        headers = {
            'User-Agent': f'{agent}',
        }

        response = requests.get(
            'https://www.youtube.com/', headers=headers, proxies=proxyDict, timeout=30)
        status = response.status_code

        if status != 200:
            raise Exception

        print(bcolors.OKBLUE + f"Tried {position+1} |" + bcolors.OKGREEN +
              f' {proxy} | GOOD | Type : {proxy_type} | Response : {status}' + bcolors.ENDC)

        print(proxy, file=open('GoodProxy.txt', 'a'))

    except:
        print(bcolors.OKBLUE + f"Tried {position+1} |" + bcolors.FAIL +
              f' {proxy} | {proxy_type} | BAD ' + bcolors.ENDC)
        checked[position] = proxy_type
        pass


def proxy_check(position):

    proxy = proxy_list[position]

    main_checker('http', proxy, position)
    if checked[position] == 'http':
        main_checker('socks4', proxy, position)
    if checked[position] == 'socks4':
        main_checker('socks5', proxy, position)


def main():
    pool_number = [i for i in range(total_proxies)]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(proxy_check, position)
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
    
    clean_exe_temp(folder='proxy_check')
    threads = int(
        input(bcolors.OKBLUE+'Threads (recommended = 100): ' + bcolors.ENDC))

    proxy_list = load_proxy()
    proxy_list = list(set(proxy_list))  # removing duplicate proxies
    proxy_list = list(filter(None, proxy_list))  # removing empty proxies

    total_proxies = len(proxy_list)
    print(bcolors.OKCYAN + f'Total proxies : {total_proxies}' + bcolors.ENDC)

    main()
