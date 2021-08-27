import sys
import json
import os

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


def create_config():
    print(bcolors.WARNING + 'Your preferences will be saved so that you don\'t need to answer these questions again.' + bcolors.ENDC)
    print(bcolors.WARNING + 'Just Hit Enter to accept default or recommended values without typing anything.' + bcolors.ENDC)

    config = {}
    port = 5000
    auth_required = False
    proxy_api = False

    http_api = str(input(
        bcolors.OKBLUE + '\nDo you want to enable a HTTP API on local server? (default=Yes) [Yes/no] : ' + bcolors.ENDC)).lower()

    if http_api == 'y' or http_api == 'yes' or http_api == '':
        enabled = True
        port = input(bcolors.OKCYAN +
                     '\nEnter a free port (default=5000) : ' + bcolors.ENDC)
        if port == '':
            port = 5000
        else:
            port = int(port)

    else:
        enabled = False

    config["http_api"] = {
        "enabled": enabled,
        "host": "0.0.0.0",
        "port": port
    }

    database = str(input(
        bcolors.OKBLUE + '\nDo you want to store your daily generated view counts in a Database ? (default=Yes) [Yes/no] : ' + bcolors.ENDC)).lower()

    if database == 'y' or database == 'yes' or database == "":
        database = True
    else:
        database = False
    config["database"] = database

    views = int(input(bcolors.WARNING + '\nAmount of views : ' + bcolors.ENDC))
    config["views"] = views

    print(bcolors.WARNING + '\nMinimum and Maximum watch duration percentages have no impact on live streams.' + bcolors.ENDC)
    print(bcolors.WARNING + 'For live streaming, script will play the video until the stream is finished.' + bcolors.ENDC)
    
    minimum = input(
        bcolors.WARNING + '\nMinimum watch duration in percentage (default = 85) : ' + bcolors.ENDC)
    if minimum == '':
        minimum = 85.0
    else:
        minimum = float(minimum)
    config["minimum"] = minimum

    maximum = input(
        bcolors.WARNING + '\nMaximum watch duration in percentage (default = 95) : ' + bcolors.ENDC)
    if maximum == '':
        maximum = 95.0
    else:
        maximum = float(maximum)
    config["maximum"] = maximum

    category = input(bcolors.OKCYAN + "\nWhat's your proxy category? " +
                     "[F = Free (without user:pass), P = Premium (with user:pass), R = Rotating Proxy] : " + bcolors.ENDC).lower()

    if category == 'f':
        handle_proxy = str(input(
            bcolors.OKBLUE + '\nLet YouTube Viewer handle proxies ? (recommended=No) [No/yes] : ' + bcolors.ENDC)).lower()

        if handle_proxy == 'y' or handle_proxy == 'yes':
            filename = False
            proxy_type = False

        else:
            filename = input(bcolors.OKCYAN +
                             '\nEnter your proxy File Name or Proxy API link : ' + bcolors.ENDC)

            if 'http://' in filename or 'https://' in filename:
                proxy_api = True

            handle_proxy = str(input(
                bcolors.OKBLUE + "\nSelect proxy type [1 = HTTP , 2 = SOCKS4, 3 = SOCKS5, 4 = ALL] : " + bcolors.ENDC)).lower()

            if handle_proxy == '1':
                proxy_type = 'http'
            elif handle_proxy == '2':
                proxy_type = 'socks4'
            elif handle_proxy == '3':
                proxy_type = 'socks5'
            elif handle_proxy == '4':
                proxy_type = False
            else:
                input(
                    '\nPlease input 1 for HTTP, 2 for SOCKS4, 3 for SOCKS5 and 4 for ALL proxy type ')
                sys.exit()

    elif category == 'p' or category == 'r':
        if category == 'r':
            print(bcolors.WARNING + '\nIf you use the Proxy API link, script will scrape the proxy list on each thread start.' + bcolors.ENDC)
            print(bcolors.WARNING + 'And will use one proxy randomly from that list to ensure session management.' + bcolors.ENDC)
            filename = input(bcolors.OKCYAN +
                             '\nEnter your Rotating Proxy service Main Gateway or Proxy API link : ' + bcolors.ENDC)

            if 'http://' in filename or 'https://' in filename:
                proxy_api = True
                auth_required = input(bcolors.OKCYAN +
                                      '\nProxies need authentication? (default=No) [No/yes] : ' + bcolors.ENDC).lower()
                if auth_required == 'y' or auth_required == 'yes' or auth_required == "":
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

                if handle_proxy == '1':
                    proxy_type = 'http'
                elif handle_proxy == '2':
                    proxy_type = 'socks4'
                elif handle_proxy == '3':
                    proxy_type = 'socks5'
                else:
                    input(
                        '\nPlease input 1 for HTTP, 2 for SOCKS4 and 3 for SOCKS5 proxy type ')
                    sys.exit()

        else:
            filename = input(bcolors.OKCYAN +
                             '\nEnter your proxy File Name or Proxy API link : ' + bcolors.ENDC)
            auth_required = True
            proxy_type = 'http'
            if 'http://' in filename or 'https://' in filename:
                proxy_api = True
    else:
        input('\nPlease input F for Free, P for Premium and R for Rotating proxy ')
        sys.exit()

    refresh = -1
    if category != 'r':
        refresh = float(input(
            bcolors.OKCYAN+'\nEnter a interval to reload proxies from File or API (in minute) : ' + bcolors.ENDC))

    config["proxy"] = {
        "category": category,
        "proxy_type": proxy_type,
        "filename": filename,
        "authentication": auth_required,
        "proxy_api": proxy_api,
        "refresh": refresh
    }

    gui = str(input(
        bcolors.OKCYAN + '\nDo you want to run in headless(background) mode? (recommended=No) [No/yes] : ' + bcolors.ENDC)).lower()

    if gui == 'y' or gui == 'yes':
        background = True
    else:
        background = False

    bandwidth = str(input(
        bcolors.OKBLUE + '\nReduce video quality to save Bandwidth? (recommended=No) [No/yes] : ' + bcolors.ENDC)).lower()

    if bandwidth == 'y' or bandwidth == 'yes':
        bandwidth = True
    else:
        bandwidth = False

    playback_speed = input(
        bcolors.OKBLUE + '\nChoose Playback speed [1 = Normal(1x), 2 = Slow(random .25x, .5x, .75x), 3 = Fast(random 1.25x, 1.5x, 1.75x)] (default = 1) : ' + bcolors.ENDC)
    if playback_speed == "":
        playback_speed = 1
    else:
        playback_speed = int(playback_speed)

    print(bcolors.WARNING +
          '\nScript will dynamically update thread amount when proxy reload happens.' + bcolors.ENDC)
    print(bcolors.WARNING + 'If you wish to use the same amount of threads all the time, enter the same number in Maximum and Minimum threads.' + bcolors.ENDC)
    max_threads = input(
        bcolors.OKCYAN + '\nMaximum Threads [Amount of chrome driver you want to use] (recommended = 5): ' + bcolors.ENDC)
    if max_threads == '':
        max_threads = 5
    else:
        max_threads = int(max_threads)

    min_threads = input(
        bcolors.OKCYAN + '\nMinimum Threads [Amount of chrome driver you want to use] (recommended = 2): ' + bcolors.ENDC)
    if min_threads == '':
        min_threads = 2
    else:
        min_threads = int(min_threads)

    config["background"] = background
    config["bandwidth"] = bandwidth
    config["playback_speed"] = playback_speed
    config["max_threads"] = max_threads
    config["min_threads"] = min_threads

    json_object = json.dumps(config, indent=4)

    with open("config.json", "w") as outfile:
        outfile.write(json_object)

    print(bcolors.OKGREEN + '\nYour preferences are saved in config.json. You can always create a new config file from youtube_viewer.py' + bcolors.ENDC)
    print(bcolors.OKGREEN + 'Or by running `python config.py` ' + bcolors.ENDC)


if __name__ == '__main__':
    create_config()
