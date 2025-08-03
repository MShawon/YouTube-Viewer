"""
MIT License

Copyright (c) 2021-2023 MShawon

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
import platform
import shutil
import subprocess
import sys
import os

import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from .colors import *


def download_driver(patched_drivers):
    osname = platform.system()
    
    print(bcolors.WARNING + 'Getting Chrome Driver...' + bcolors.ENDC)
    
    # Set executable extension based on OS
    if osname == 'Windows':
        exe_name = ".exe"
        osname = 'win'
    elif osname == 'Darwin':
        exe_name = ""
        osname = 'mac'
    elif osname == 'Linux':
        exe_name = ""
        osname = 'lin'
    else:
        print(f'{osname} OS is not supported.')
        sys.exit()

    # Get Chrome version
    version = get_chrome_version()
    
    # Check if we need to update the driver
    try:
        with open('version.txt', 'r') as f:
            previous_version = f.read().strip()
    except Exception:
        previous_version = '0'

    # Write current version
    with open('version.txt', 'w') as f:
        f.write(version)

    # Clean up old drivers if version changed
    if version != previous_version:
        try:
            os.remove(f'chromedriver{exe_name}')
        except Exception:
            pass
        shutil.rmtree(patched_drivers, ignore_errors=True)

    # Download/get chromedriver using webdriver-manager
    try:
        print(bcolors.OKGREEN + 'Downloading ChromeDriver...' + bcolors.ENDC)
        driver_path = ChromeDriverManager().install()
        
        # Copy to local directory
        local_driver_path = f'chromedriver{exe_name}'
        if not os.path.exists(local_driver_path):
            shutil.copy(driver_path, local_driver_path)
            if osname != 'win':
                os.chmod(local_driver_path, 0o755)
        
        print(bcolors.OKGREEN + f'ChromeDriver ready at: {local_driver_path}' + bcolors.ENDC)
        
    except Exception as e:
        print(bcolors.FAIL + f'Error downloading ChromeDriver: {e}' + bcolors.ENDC)
        # Fallback to undetected-chromedriver's built-in download
        try:
            print(bcolors.WARNING + 'Trying fallback method...' + bcolors.ENDC)
            driver = uc.Chrome(version_main=int(version.split('.')[0]))
            driver.quit()
        except Exception as e2:
            print(bcolors.FAIL + f'Fallback also failed: {e2}' + bcolors.ENDC)

    return osname, exe_name


def get_chrome_version():
    """Get the installed Chrome version"""
    osname = platform.system()
    version = None
    
    try:
        if osname == 'Linux':
            process = subprocess.Popen(['google-chrome-stable', '--version'], 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            version = process.communicate()[0].decode('utf-8').replace('Google Chrome', '').strip()
        elif osname == 'Darwin':
            process = subprocess.Popen(
                ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            version = process.communicate()[0].decode('UTF-8').replace('Google Chrome', '').strip()
        elif osname == 'Windows':
            # Try multiple registry locations for Windows
            chrome_keys = ['{8A69D345-D564-463c-AFF1-A69D9E530F96}',
                          '{8237E44A-0054-442C-B6B6-EA0509993955}',
                          '{401C381F-E0DE-4B85-8BD8-3F3F14FBDA57}',
                          '{4ea16ac7-fd5a-47c3-875b-dbf4a2008c20}']
            
            try:
                process = subprocess.Popen(
                    ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
                )
                version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
            except Exception:
                for chrome_key in chrome_keys:
                    for value in ['opv', 'pv']:
                        try:
                            command = ['reg', 'query', 
                                     f'HKEY_LOCAL_MACHINE\\Software\\Google\\Update\\Clients\\{chrome_key}', 
                                     '/v', value, '/reg:32']
                            process = subprocess.Popen(command, stdout=subprocess.PIPE, 
                                                     stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
                            version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
                            if version:
                                break
                        except Exception:
                            continue
                    if version:
                        break

            if not version:
                print(bcolors.WARNING + "Couldn't find Chrome version automatically!" + bcolors.ENDC)
                version = input(bcolors.WARNING + 'Please input your Chrome version (ex: 138.0.6464.175): ' + bcolors.ENDC)
        
        if not version:
            raise Exception("Could not determine Chrome version")
            
        return version.strip()
        
    except Exception as e:
        print(bcolors.FAIL + f'Error getting Chrome version: {e}' + bcolors.ENDC)
        # Return a reasonable default for the current Chrome version
        return "138.0.6464.175"


def copy_drivers(cwd, patched_drivers, exe, total):
    current = os.path.join(cwd, f'chromedriver{exe}')
    os.makedirs(patched_drivers, exist_ok=True)
    for i in range(total+1):
        try:
            destination = os.path.join(
                patched_drivers, f'chromedriver_{i}{exe}')
            shutil.copy(current, destination)
        except Exception:
            pass
