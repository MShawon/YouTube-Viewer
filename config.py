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
    print(bcolors.WARNING + 'Just Hit Enter to accept default or recommended values without typing anything' + bcolors.ENDC)

    config = {}
    port = 5000
    auth_required = False

    http_api = str(input(
        bcolors.OKBLUE + 'Do you want to enable a HTTP api on local server? (default=Yes) [Yes/no] : ' + bcolors.ENDC)).lower()

    if http_api == 'y' or http_api == 'yes' or http_api == '':
        enabled = True
        port = input(bcolors.OKCYAN +
                     'Enter a free port (default=5000) : ' + bcolors.ENDC)
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
        bcolors.OKBLUE + 'Do you want to store your daily generated view counts in a Database ? (default=Yes) [Yes/no] : ' + bcolors.ENDC)).lower()

    if database == 'y' or database == 'yes':
        database = True
    else:
        database = False
    config["database"] = database

    views = int(input(bcolors.WARNING + 'Amount of views : ' + bcolors.ENDC))
    config["views"] = views

    category = input(bcolors.OKCYAN + "What's your proxy category? " +
                     "[F = Free (without user:pass), P = Premium (with user:pass), R = Rotating Proxy] : " + bcolors.ENDC).lower()

    if category == 'f':
        handle_proxy = str(input(
            bcolors.OKBLUE + 'Let YouTube Viewer handle proxies ? (recommended=No) [No/yes] : ' + bcolors.ENDC)).lower()

        if handle_proxy == 'y' or handle_proxy == 'yes':
            filename = False
            proxy_type = False
        else:
            filename = input(bcolors.OKCYAN +
                             'Enter your proxy file name: ' + bcolors.ENDC)
            handle_proxy = str(input(
                bcolors.OKBLUE + "Select proxy type [1 = HTTP , 2 = SOCKS4, 3 = SOCKS5, 4 = ALL] : " + bcolors.ENDC)).lower()

            if handle_proxy == '1':
                proxy_type = 'http'
            elif handle_proxy == '2':
                proxy_type = 'socks4'
            elif handle_proxy == '3':
                proxy_type = 'socks5'
            elif handle_proxy == '4':
                proxy_type = False
            else:
                print(
                    'Please input 1 for HTTP, 2 for SOCKS4, 3 for SOCKS5 and 4 for ALL proxy type')
                sys.exit()

    elif category == 'p' or category == 'r':
        if category == 'r':
            filename = input(bcolors.OKCYAN +
                             'Enter your Rotating Proxy service Main Gateway : ' + bcolors.ENDC)

            if '@' in filename:
                auth_required = True
                proxy_type = 'http'
            else:
                handle_proxy = str(input(
                    bcolors.OKBLUE + "Select proxy type [1 = HTTP , 2 = SOCKS4, 3 = SOCKS5] : " + bcolors.ENDC)).lower()

                if handle_proxy == '1':
                    proxy_type = 'http'
                elif handle_proxy == '2':
                    proxy_type = 'socks4'
                elif handle_proxy == '3':
                    proxy_type = 'socks5'
                else:
                    print(
                        'Please input 1 for HTTP, 2 for SOCKS4 and 3 for SOCKS5 proxy type')
                    sys.exit()
        else:
            filename = input(bcolors.OKCYAN +
                             'Enter your proxy file name: ' + bcolors.ENDC)
            auth_required = True
            proxy_type = 'http'

    else:
        print('Please input F for Free, P for Premium and R for Rotating proxy')
        sys.exit()

    config["proxy"] = {
        "category": category,
        "proxy_type": proxy_type,
        "filename": filename,
        "authentication": auth_required,
    }

    gui = str(input(
        bcolors.OKCYAN + 'Do you want to run in headless(background) mode? (recommended=No) [No/yes] : ' + bcolors.ENDC)).lower()

    if gui == 'y' or gui == 'yes':
        background = True
    else:
        background = False

    bandwidth = str(input(
        bcolors.OKBLUE + 'Reduce video quality to save Bandwidth? (recommended=No) [No/yes] : ' + bcolors.ENDC)).lower()

    if bandwidth == 'y' or bandwidth == 'yes':
        bandwidth = True
    else:
        bandwidth = False

    threads = input(
        bcolors.OKCYAN+'Threads (recommended = 5): ' + bcolors.ENDC)
    if threads == '':
        threads = 5
    else:
        threads = int(threads)

    if enabled:
        threads += 1

    config["background"] = background
    config["bandwidth"] = bandwidth
    config["threads"] = threads

    json_object = json.dumps(config, indent=4)

    # Writing to sample.json
    with open("config.json", "w") as outfile:
        outfile.write(json_object)

    print(bcolors.OKGREEN + 'Your preferences are saved in config.json. You can always create a new config file from youtube_viewer.py' + bcolors.ENDC)
    print(bcolors.OKGREEN + 'Or by running `python config.py` ' + bcolors.ENDC)


if __name__ == '__main__':
    create_config()
