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

import time
import os
import platform
import shutil
import subprocess
import sys
import requests
import urllib.request
import zipfile
from selenium import webdriver
import undetected_chromedriver as uc
from packaging.version import parse as parse_version

from .colors import *

CHROME_KEYS = [
    "{8A69D345-D564-463c-AFF1-A69D9E530F96}",
    "{8237E44A-0054-442C-B6B6-EA0509993955}",
    "{401C381F-E0DE-4B85-8BD8-3F3F14FBDA57}",
    "{4ea16ac7-fd5a-47c3-875b-dbf4a2008c20}",
]


def get_chrome_version(osname):
    """
    Detects the installed version of Google Chrome based on the operating system.
    Returns the Chrome version as a string.
    """
    try:
        if osname == "Linux":
            version = None
            for browser in ["google-chrome", "google-chrome-stable"]:
                try:
                    process = subprocess.Popen(
                        [browser, "--version"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    output = process.communicate()[0]
                    if output:
                        version = (
                            output.decode("utf-8").replace("Google Chrome", "").strip()
                        )
                        break
                except:
                    continue

            if not version:
                raise ValueError("Chrome not found on Linux system")
        elif osname == "Darwin":
            process = subprocess.Popen(
                [
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "--version",
                ],
                stdout=subprocess.PIPE,
            )
            version = (
                process.communicate()[0]
                .decode("UTF-8")
                .replace("Google Chrome", "")
                .strip()
            )
        elif osname == "Windows":
            version = detect_chrome_version_windows()
        else:
            raise OSError(f"Unsupported operating system: {osname}")

        if not version:
            raise ValueError("Failed to detect Google Chrome version.")
        return version

    except Exception as e:
        print(bcolors.FAIL + f"Error detecting Chrome version: {e}" + bcolors.ENDC)
        sys.exit("Ensure Google Chrome is installed and accessible.")


def detect_chrome_version_windows():
    """
    Detects the installed version of Google Chrome on Windows using the registry.
    Returns the Chrome version as a string. If manual input is needed, saves it for future use.
    """
    # First try registry
    for key in CHROME_KEYS:
        for subkey in ["opv", "pv"]:
            try:
                process = subprocess.Popen(
                    [
                        "reg",
                        "query",
                        f"HKEY_LOCAL_MACHINE\\Software\\Google\\Update\\Clients\\{key}",
                        "/v",
                        subkey,
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                )
                version = process.communicate()[0].decode("utf-8").strip().split()[-1]
                if version:
                    return version
            except Exception:
                continue

    # Try to load saved version
    version_file = os.path.join(
        os.path.expanduser("~"), ".youtube_viewer_chrome_version"
    )
    try:
        with open(version_file, "r") as f:
            saved_version = f.read().strip()
            print(
                bcolors.OKGREEN
                + f"Using saved Chrome version: {saved_version}"
                + bcolors.ENDC
            )
            return saved_version
    except FileNotFoundError:
        pass

    # If no saved version, ask user
    print(bcolors.WARNING + "Couldn't find Chrome version in registry." + bcolors.ENDC)
    version = input(
        bcolors.WARNING
        + "Please input your Google Chrome version (e.g., 91.0.4472.114): "
        + bcolors.ENDC
    )

    # Save the manually entered version
    try:
        with open(version_file, "w") as f:
            f.write(version)
        print(bcolors.OKGREEN + "Chrome version saved for future use." + bcolors.ENDC)
    except Exception as e:
        print(bcolors.WARNING + f"Could not save Chrome version: {e}" + bcolors.ENDC)

    return version


def download_driver(patched_drivers):
    """Downloads ChromeDriver and sets it up."""
    try:
        # Determine OS and executable name
        if sys.platform.startswith("linux"):
            osname = "Linux"
        elif sys.platform == "darwin":
            osname = "Darwin"
        elif sys.platform.startswith("win"):
            osname = "Windows"
        else:
            raise OSError("Unknown OS Type")

        exe_name = ".exe" if osname == "Windows" else ""

        print("Getting Chrome Driver...")

        # Check if chromedriver exists
        current_driver_path = os.path.join(os.getcwd(), f"chromedriver{exe_name}")
        if not os.path.exists(current_driver_path):
            print("ChromeDriver not found, downloading...")
            # Proceed to download the driver
            driver_path = download_driver_alternative(osname.lower(), exe_name)
        else:
            driver_path = current_driver_path

        # Get Chrome version
        chrome_version = get_chrome_version(osname)
        if chrome_version:
            major_version = chrome_version.split(".")[0]
            print(f"Detected Chrome version: {chrome_version}")
        else:
            print("Could not detect Chrome version, using default configuration")
            major_version = None

        try:
            # Try using undetected-chromedriver
            options = uc.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            driver = uc.Chrome(
                version_main=int(major_version) if major_version else None,
                options=options,
            )

            # Get driver path before quitting
            if hasattr(driver, "browser_executable_path"):
                driver_path = driver.browser_executable_path
            else:
                driver_path = os.path.join(os.getcwd(), f"chromedriver{exe_name}")

            driver.quit()

        except Exception as e:
            print(f"Error with undetected-chromedriver: {e}")
            print("Falling back to direct ChromeDriver download...")

        # Create patched drivers directory
        os.makedirs(patched_drivers, exist_ok=True)

        return osname, exe_name, driver_path

    except Exception as e:
        print(f"Error in download_driver: {e}")
        sys.exit(1)


def download_driver_alternative(osname, exe_name):
    """Alternative direct download from Chrome for Testing."""
    try:
        # Define the stable version and corresponding URLs
        stable_version = "133.0.6943.53"
        os_map = {
            "linux": f"https://storage.googleapis.com/chrome-for-testing-public/{stable_version}/linux64/chromedriver-linux64.zip",
            "windows": f"https://storage.googleapis.com/chrome-for-testing-public/{stable_version}/win64/chromedriver-win64.zip",
            "darwin": (
                f"https://storage.googleapis.com/chrome-for-testing-public/{stable_version}/mac-x64/chromedriver-mac-x64.zip"
                if platform.machine() == "x86_64"
                else f"https://storage.googleapis.com/chrome-for-testing-public/{stable_version}/mac-arm64/chromedriver-mac-arm64.zip"
            ),
        }

        if osname not in os_map:
            raise ValueError(f"Unsupported OS: {osname}")

        driver_url = os_map[osname]
        print(f"Downloading ChromeDriver from: {driver_url}")

        # Download and extract
        local_zip = "chromedriver.zip"
        response = requests.get(driver_url)
        response.raise_for_status()  # Raise an error for bad status codes

        with open(local_zip, "wb") as f:
            f.write(response.content)

        # Extract the ZIP file
        with zipfile.ZipFile(local_zip, "r") as zip_ref:
            zip_ref.extractall()  # Extract to the current working directory

        # Move driver to final location
        # The extracted folder name is based on the OS and version
        extracted_folder = (
            f"chromedriver-{osname}" if osname == "darwin" else "chromedriver-win64"
        )
        src_path = os.path.join(extracted_folder, f"chromedriver{exe_name}")
        dst_path = f"chromedriver{exe_name}"

        if os.path.exists(dst_path):
            os.remove(dst_path)

        shutil.move(src_path, dst_path)

        # Set permissions for non-Windows
        if osname != "windows":
            os.chmod(dst_path, 0o755)

        # Cleanup
        os.remove(local_zip)

        return os.path.abspath(dst_path)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        sys.exit(1)
    except Exception as e:
        print(f"Alternative driver download failed: {str(e)}")
        sys.exit(1)


def get_driver_options(background, bandwidth):
    options = uc.ChromeOptions()

    options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_settings.cookies": 1,
            "profile.block_third_party_cookies": False,
            "profile.cookie_controls_mode": 0,
            "profile.default_content_setting_values": {
                "cookies": 1,
                "notifications": 2,
                "automatic_downloads": 1,
                "plugins": 1,
                "popups": 2,
            },
            "profile.managed_default_content_settings": {
                "cookies": 1,
                "images": 1,
                "javascript": 1,
                "plugins": 1,
                "popups": 2,
                "geolocation": 2,
                "notifications": 2,
                "auto_select_certificate": 2,
                "fullscreen": 2,
                "mouselock": 2,
                "mixed_script": 2,
                "media_stream": 2,
                "media_stream_mic": 2,
                "media_stream_camera": 2,
                "protocol_handlers": 2,
                "ppapi_broker": 2,
                "automatic_downloads": 1,
                "midi_sysex": 2,
                "push_messaging": 2,
                "ssl_cert_decisions": 2,
                "metro_switch_to_desktop": 2,
                "protected_media_identifier": 2,
                "app_banner": 2,
                "site_engagement": 2,
                "durable_storage": 2,
            },
        },
    )

    if background:
        options.add_argument("--headless=new")

    if bandwidth:
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--disable-site-isolation-trials")

    return options


def copy_drivers(cwd, patched_drivers, exe, total):
    """
    Copies the downloaded ChromeDriver to multiple destinations for use by different workers.
    """
    try:
        current = os.path.join(cwd, f"chromedriver{exe}")

        # Ensure source driver exists
        if not os.path.exists(current):
            raise FileNotFoundError(f"Source driver not found at {current}")

        # Create patched_drivers directory
        os.makedirs(patched_drivers, exist_ok=True)

        for i in range(total + 1):
            destination = os.path.join(patched_drivers, f"chromedriver_{i}{exe}")

            if os.path.abspath(current) == os.path.abspath(destination):
                continue

            try:
                if os.path.exists(destination):
                    try:
                        os.remove(destination)
                    except (FileExistsError, PermissionError):
                        pass

                shutil.copy2(current, destination)

                if exe == "":
                    os.chmod(destination, 0o755)

            except Exception as e:
                print(
                    f"{bcolors.WARNING}Failed to copy driver to {destination}: {str(e)}{bcolors.ENDC}"
                )
                continue

    except Exception as e:
        print(f"{bcolors.FAIL}Error in copy_drivers: {str(e)}{bcolors.ENDC}")
        sys.exit(1)
