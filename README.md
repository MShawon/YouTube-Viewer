<p align="center">
<img alt="ViewCount" src="https://views.whatilearened.today/views/github/MShawon/YouTube-Viewer.svg">
<img alt="OS" src="https://img.shields.io/badge/OS-Windows%20/%20Linux / Mac-success">
<a href="https://github.com/MShawon/YouTube-Viewer/releases"><img alt="Downloads" src="https://img.shields.io/github/downloads/MShawon/YouTube-Viewer/total?label=Downloads&color=success"></a>
<a href="https://github.com/MShawon/YouTube-Viewer/issues?q=is%3Aissue+is%3Aclosed"><img alt="Closed issues" src="https://img.shields.io/github/issues-closed/MShawon/YouTube-Viewer.svg"></a>
<a href="https://github.com/MShawon/YouTube-Viewer/issues?q=is%3Aissue+is%3Aopen"><img alt="Open issues" src="https://img.shields.io/github/issues/MShawon/YouTube-Viewer"></a>
</p>
<p align="center">
  <a href="https://github.com/MShawon/YouTube-Viewer/releases/latest"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/MShawon/YouTube-Viewer?color=success"></a>
  <a href="https://github.com/MShawon/YouTube-Viewer/releases/latest"><img alt="GitHub Release Date" src="https://img.shields.io/github/release-date/MShawon/YouTube-Viewer?color=success"></a>
</p>

    Yb  dP  dP"Yb  88   88 888888 88   88 88""Yb 888888
     YbdP  dP   Yb 88   88   88   88   88 88__dP 88__   
      8P   Yb   dP Y8   8P   88   Y8   8P 88""Yb 88""   
     dP     YbodP  `YbodP'   88   `YbodP' 88oodP 888888 

                         Yb    dP 88 888888 Yb        dP 888888 88""Yb 
                          Yb  dP  88 88__    Yb  db  dP  88__   88__dP 
                           YbdP   88 88""     YbdPYbdP   88""   88"Yb  
                            YP    88 888888    YP  YP    888888 88  Yb

# YouTube Viewer
Simple program to increase YouTube views written in Python.

**Disclaimer:** This has been developed for educational purposes only. Any action you take using this script is strictly at your own risk. I will not be liable for any losses or damages you face using this script.

**Cons:** Try not to use this script every day. Run this once or twice a week with newer proxies. Guess this will reduce the view decrease issue.

# View Decrease
 If you see views are getting deleted after a while, make sure you're using good proxies. Here https://github.com/MShawon/YouTube-Viewer/issues/46#issuecomment-806399397 a user confirmed about view stability with good proxies 

# Issues
 Before opening an issue, please read this page thoroughly. Maybe someone already faced the same problem you have right now. So it's always a good idea to check the answer from issues first. If your problem isn't there, feel free to open an issue.

# Requirements
 * Python 3.6+
 * High speed Internet Connection
 * Good proxy list (http, https, socks4, socks5)
 * Google Chrome installed on your OS (not Chromium)
 * Chrome driver will be downloaded automatically by undetected-chromedriver

# Proxies
* ## Free Proxy
   Try not to use free proxies. But if you have a paid subscription and you want to use authenticated IP feature, then you can use free proxy category.

* ## Premium Proxy
   Proxies with authentication can also be done. To do so put your proxies in this format **username:password@ipaddress:port** in a text file. Every single line will contain a single proxy. Provide your text file path when script asks for proxy file name.

* ## Rotating Proxy
   You can also use rotating proxies service like webshare, storm proxies and so on. Make sure to authenticate your IP on their website and use the Main Gateway (ipaddress:port) they provide you.

# Urls
  Put video links in the urls.txt. For multiple videos place urls in multple lines.
  1) To find video link in YouTube click share and copy.
  2) If you have any external link which will redirect to your youtube video you can use that too. Example : when you post a YouTube video link in **twitter** and you hit play on twitter, you will get a link like this `https://t.co/xxxxxxxxxx?amp=1`. This is helpful because YouTube will see that views are coming from External Source like twitter in this example.

# Search
  Program can search youtube with keyword and find video with video title. To do this you need to know what keyword can find your video on youtube search engine. Also you need to provide **exact** video title.Put keyword and title like this format `keyword : video title` in **search.txt** 

# Windows
* ## Binary Release

  For windows you can download binary releases from **[Binary releases](https://github.com/MShawon/YouTube-Viewer/releases)** or you can install it from source. To do so keep reading. 
  
* ## Installation 
 
  Open command prompt and type
  ```bash
  $ git clone https://github.com/MShawon/YouTube-Viewer.git

  $ cd YouTube-Viewer

  $ pip install -r requirements.txt
  ```
  If something goes wrong, try again after installing latest version pip.

* ## Important
   * If you've got a large proxy collection, you should run this command to filter Good proxies. Then use **GoodProxy.txt** for proxy in **youtube_viewer.py**
      ```
      $ python proxy_check.py
      ```

   * After closing program, if chromedrivers are still running. You may want to double click **killdrive.bat** to close all chrome instances.

   * *urls.txt* or *search.txt* can't be empty. Otherwise you will see errors.

* ## Usage
   * Open command prompt in YouTube-Viewer folder and run
        ```
        $ python youtube_viewer.py
        ```
   * Rest is self explanatory.

    ![alt text](demo_windows.png "Demo Windows")

# Linux / Mac
* ## Installation 
 
  Open your favourite terminal and run
  ```bash
  $ git clone https://github.com/MShawon/YouTube-Viewer.git

  $ cd YouTube-Viewer

  $ pip3 install -r requirements.txt
  ```
  If something goes wrong, try again after installing latest version pip.

* ## Important
   * If you've got a large proxy collection, you should run this command to filter Good proxies. Then use **GoodProxy.txt** for proxy in **youtube_viewer.py**
        ```
        $ python3 proxy_check.py
        ```

   * After closing program, if chromedrivers are still running. Open your terminal and run 
      ```
      ps aux | awk '/chrome/ { print $2 } ' | xargs kill -9
      ```
   * *urls.txt* or *search.txt* can't be empty. Otherwise you will see errors.

* ## Usage
   * Open command prompt in YouTube-Viewer folder and run
        ```
        $ python3 youtube_viewer.py
        ```
   * Rest is self explanatory.

   ![alt text](demo_linux.png "Demo Linux")

# Donation
 **BTC**
 `1Jh8KZ6khuHayNDeVV9tEzYSq9FPExKCAH`
 
# Credits
I want to thank all of you who have opened an issue or shared your ideas with me! 
