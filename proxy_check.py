import concurrent.futures.thread
import os
import random
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
    agent_link = 'https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt'
    response = requests.get(agent_link).content
    ua = response.decode().split('\n')
    ua = list(filter(None, ua))

proxy_list = []


def load_proxy():
    global proxy_list

    filename = input(bcolors.OKBLUE +
                     'Enter your proxy file name: ' + bcolors.ENDC)
    load = open(filename)
    loaded = [items.rstrip().strip() for items in load]
    load.close()

    for lines in loaded:
        proxy_list.append(lines)

    return proxy_list


def proxyCheck(position):

    PROXY = proxy_list[position]

    proxyDict = {
        "http": "http://"+PROXY,
        "https": "https://"+PROXY,
        "ftp": "ftp://"+PROXY,
    }

    # print(proxyDict)
    try:
        headers = {
            'User-Agent': '{}'.format(ua.random),
        }

        response = requests.get(
            'https://www.youtube.com/', headers=headers, proxies=proxyDict, timeout=30)
        status = response.status_code

        print(bcolors.OKBLUE + "Tried {} |".format(position) + bcolors.OKGREEN +
              ' {} GOOD | Response : {}'.format(PROXY, status) + bcolors.ENDC)

        print(PROXY, file=open('GoodProxy.txt', 'a'))

    except:
        print(bcolors.OKBLUE + "Tried {} |".format(position) + bcolors.FAIL +
              ' {} BAD '.format(PROXY) + bcolors.ENDC)
        pass


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
            print(bcolors.WARNING+ 'Number of proxies are less than threads. Provide more proxies or less threads.' +bcolors.ENDC)
            pass

if __name__ == '__main__':
    threads = int(
        input(bcolors.OKBLUE+'Threads (recommended = 100): ' + bcolors.ENDC))

    load_proxy()
    proxy_list = list(set(proxy_list))
    total_proxies = len(proxy_list)
    print(bcolors.OKCYAN + 'Total proxies : {}'.format(total_proxies) + bcolors.ENDC)

    main()
