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
import json

PROXY_TYPES = {
    '1': 'http',
    '2': 'socks4',
    '3': 'socks5',
    '4': False
}


def config_api(config):
    port = 5000
    http_api = str(input(
        bcolors.OKBLUE + '\nDo you want to enable a HTTP API on local server? (default=Yes) [Yes/no] : ' + bcolors.ENDC)).lower()

    if http_api == 'n' or http_api == 'no':
        enabled = False
    else:
        enabled = True
        port = input(bcolors.OKCYAN +
                     '\nEnter a free port (default=5000) : ' + bcolors.ENDC)
        try:
            port = int(port)
        except Exception:
            port = 5000

    config["http_api"] = {
        "enabled": enabled,
        "host": "0.0.0.0",
        "port": port
    }
    return config


def config_database(config):
    database = str(input(
        bcolors.OKBLUE + '\nDo you want to store your daily generated view counts in a Database ? (default=Yes) [Yes/no] : ' + bcolors.ENDC)).lower()

    if database == 'n' or database == 'no':
        database = False
    else:
        database = True

    config["database"] = database
    return config


def config_views(config):
    for _ in range(10):
        try:
            views = float(
                input(bcolors.WARNING + '\nAmount of views you want : ' + bcolors.ENDC))
            break
        except Exception as e:
            print(bcolors.FAIL + e.args[0] + bcolors.ENDC)
            print(bcolors.BOLD + 'Type a number like 1000 ' + bcolors.ENDC)
    try:
        config["views"] = int(views)
    except Exception:
        config["views"] = 100
    return config


def config_min_max(config):
    print(bcolors.WARNING +
          '\n--> Minimum and Maximum watch duration percentages have no impact on live streams.' + bcolors.ENDC)
    print(bcolors.WARNING +
          '--> For live streaming, script will play the video until the stream is finished.' + bcolors.ENDC)

    minimum = input(
        bcolors.WARNING + '\nMinimum watch duration in percentage (default = 85) : ' + bcolors.ENDC)
    try:
        minimum = float(minimum)
    except Exception:
        minimum = 85.0

    maximum = input(
        bcolors.WARNING + '\nMaximum watch duration in percentage (default = 95) : ' + bcolors.ENDC)
    try:
        maximum = float(maximum)
    except Exception:
        maximum = 95.0

    if minimum >= maximum:
        minimum = maximum - 5

    config["minimum"] = minimum
    config["maximum"] = maximum
    return config


def config_free_proxy(category):
    auth_required = False
    proxy_api = False

    handle_proxy = str(input(
        bcolors.OKBLUE + '\nLet YouTube Viewer handle proxies ? (recommended=No) [No/yes] : ' + bcolors.ENDC)).lower()

    if handle_proxy == 'y' or handle_proxy == 'yes':
        proxy_type = False
        filename = False

    else:
        filename = ""
        while not filename:
            filename = str(input(
                bcolors.OKCYAN + '\nEnter your proxy File Name or Proxy API link : ' + bcolors.ENDC))

        if 'http://' in filename or 'https://' in filename:
            proxy_api = True

        handle_proxy = str(input(
            bcolors.OKBLUE + "\nSelect proxy type [1 = HTTP , 2 = SOCKS4, 3 = SOCKS5, 4 = ALL] : " + bcolors.ENDC)).lower()
        while handle_proxy not in ['1', '2', '3', '4']:
            handle_proxy = str(input(
                '\nPlease input 1 for HTTP, 2 for SOCKS4, 3 for SOCKS5 and 4 for ALL proxy type : ')).lower()

        proxy_type = PROXY_TYPES[handle_proxy]

    return proxy_type, filename, auth_required, proxy_api


def config_premium_proxy(category):
    auth_required = False
    proxy_api = False

    if category == 'r':
        print(bcolors.WARNING + '\n--> If you use the Proxy API link, script will scrape the proxy list on each thread start.' + bcolors.ENDC)
        print(bcolors.WARNING + '--> And will use one proxy randomly from that list to ensure session management.' + bcolors.ENDC)

        filename = ""
        while not filename:
            filename = str(input(
                bcolors.OKCYAN + '\nEnter your Rotating Proxy service Main Gateway or Proxy API link : ' + bcolors.ENDC))

        if 'http://' in filename or 'https://' in filename:
            proxy_api = True
            auth_required = input(bcolors.OKCYAN +
                                  '\nProxies need authentication? (default=No) [No/yes] : ' + bcolors.ENDC).lower()
            if auth_required == 'y' or auth_required == 'yes':
                auth_required = True
                proxy_type = 'http'
            else:
                auth_required = False

        else:
            if '@' in filename:
                auth_required = True
                proxy_type = 'http'
            elif filename.count(':') == 3:
                split = filename.split(':')
                filename = f'{split[2]}:{split[-1]}@{split[0]}:{split[1]}'
                auth_required = True
                proxy_type = 'http'

        if not auth_required:
            handle_proxy = str(input(
                bcolors.OKBLUE + "\nSelect proxy type [1 = HTTP , 2 = SOCKS4, 3 = SOCKS5] : " + bcolors.ENDC)).lower()
            while handle_proxy not in ['1', '2', '3']:
                handle_proxy = str(input(
                    '\nPlease input 1 for HTTP, 2 for SOCKS4 and 3 for SOCKS5 proxy type : ')).lower()

            proxy_type = PROXY_TYPES[handle_proxy]

    else:
        filename = ""
        while not filename:
            filename = str(input(
                bcolors.OKCYAN + '\nEnter your proxy File Name or Proxy API link : ' + bcolors.ENDC))
        auth_required = True
        proxy_type = 'http'
        if 'http://' in filename or 'https://' in filename:
            proxy_api = True

    return proxy_type, filename, auth_required, proxy_api


def config_proxy(config):
    print(bcolors.WARNING +
          '\n--> Free proxy : NO authentication required | Format : [IP:PORT] | Type : HTTP/SOCKS4/SOCKS5' + bcolors.ENDC)
    print(bcolors.WARNING +
          '--> Premium proxy : authentication required | Format : [USER:PASS@IP:PORT] or [IP:PORT:USER:PASS] | Type : HTTP only' + bcolors.ENDC)
    print(bcolors.WARNING + '--> Rotating proxy : follows Free proxy for no authentication and vice versa' + bcolors.ENDC)
    category = input(bcolors.OKCYAN + "\nWhat's your proxy category? " +
                     "[F = Free, P = Premium, R = Rotating Proxy] : " + bcolors.ENDC).lower()
    while category not in ['f', 'p', 'r']:
        category = input(
            '\nPlease input F for Free, P for Premium and R for Rotating proxy : ').lower()

    if category == 'f':
        proxy_type, filename, auth_required, proxy_api = config_free_proxy(
            category)

    elif category == 'p' or category == 'r':
        proxy_type, filename, auth_required, proxy_api = config_premium_proxy(
            category)

    refresh = 0.0
    if category != 'r' and filename:
        print(bcolors.WARNING + '\n--> Refresh interval means after every X minutes, program will reload proxies from your File or API' + bcolors.ENDC)
        print(bcolors.WARNING + '--> You should use this if and only if there will be new proxies in your File or API after every X minutes.' + bcolors.ENDC)
        print(bcolors.WARNING +
              '--> Otherwise just enter 0 as the interval.' + bcolors.ENDC)
        try:
            refresh = abs(float(input(
                bcolors.OKCYAN+'\nEnter a interval to reload proxies from File or API (in minute) [default=0]: ' + bcolors.ENDC)))
        except Exception:
            refresh = 0.0

    config["proxy"] = {
        "category": category,
        "proxy_type": proxy_type,
        "filename": filename,
        "authentication": auth_required,
        "proxy_api": proxy_api,
        "refresh": refresh
    }
    return config


def config_gui(config):
    gui = str(input(
        bcolors.OKCYAN + '\nDo you want to run in headless(background) mode? (recommended=No) [No/yes] : ' + bcolors.ENDC)).lower()

    if gui == 'y' or gui == 'yes':
        background = True
    else:
        background = False

    config["background"] = background
    return config


def config_bandwidth(config):
    bandwidth = str(input(
        bcolors.OKBLUE + '\nReduce video quality to save Bandwidth? (recommended=No) [No/yes] : ' + bcolors.ENDC)).lower()

    if bandwidth == 'y' or bandwidth == 'yes':
        bandwidth = True
    else:
        bandwidth = False

    config["bandwidth"] = bandwidth
    return config


def config_playback(config):
    playback_speed = input(
        bcolors.OKBLUE + '\nChoose Playback speed [1 = Normal(1x), 2 = Slow(random .25x, .5x, .75x), 3 = Fast(random 1.25x, 1.5x, 1.75x)] (default = 1) : ' + bcolors.ENDC)
    try:
        playback_speed = int(playback_speed) if playback_speed in [
            '2', '3'] else 1
    except Exception:
        playback_speed = 1

    config["playback_speed"] = playback_speed
    return config


def config_threads(config):
    print(bcolors.WARNING +
          '\n--> Script will dynamically update thread amount when proxy reload happens.' + bcolors.ENDC)
    print(bcolors.WARNING +
          '--> If you wish to use the same amount of threads all the time, enter the same number in Maximum and Minimum threads.' + bcolors.ENDC)

    max_threads = input(
        bcolors.OKCYAN + '\nMaximum Threads [Amount of chrome driver you want to use] (recommended = 5): ' + bcolors.ENDC)
    try:
        max_threads = int(max_threads)
    except Exception:
        max_threads = 5

    min_threads = input(
        bcolors.OKCYAN + '\nMinimum Threads [Amount of chrome driver you want to use] (recommended = 2): ' + bcolors.ENDC)
    try:
        min_threads = int(min_threads)
    except Exception:
        min_threads = 2

    if min_threads >= max_threads:
        max_threads = min_threads

    config["max_threads"] = max_threads
    config["min_threads"] = min_threads
    return config


def create_config(config_path):
    print(bcolors.WARNING + '\n--> Your preferences will be saved so that you don\'t need to answer these questions again.' + bcolors.ENDC)
    print(bcolors.WARNING + '--> Just Hit Enter to accept default or recommended values without typing anything.' + bcolors.ENDC)

    config = {}

    config = config_api(config=config)

    config = config_database(config=config)

    config = config_views(config=config)

    config = config_min_max(config=config)

    config = config_proxy(config=config)

    config = config_gui(config=config)

    config = config_bandwidth(config=config)

    config = config_playback(config=config)

    config = config_threads(config=config)

    json_object = json.dumps(config, indent=4)

    with open(config_path, "w", encoding='utf-8-sig') as outfile:
        outfile.write(json_object)

    print(bcolors.OKGREEN + '\n--> Your preferences are saved in config.json. You can always create a new config file from youtube_viewer.py' + bcolors.ENDC)
    print(bcolors.OKGREEN +
          '--> Or by running `python youtubeviewer/config.py` ' + bcolors.ENDC)


if __name__ == '__main__':
    from colors import *
    create_config(config_path='config.json')
else:
    from .colors import *
