<p align="center">
<img alt="ViewCount" src="https://views.whatilearened.today/views/github/MShawon/YouTube-Viewer.svg">
<img alt="OS" src="https://img.shields.io/badge/OS-Windows%20/%20Linux-success">
<a href="https://github.com/MShawon/YouTube-Viewer/issues?q=is%3Aissue+is%3Aclosed"><img alt="Closed issues" src="https://img.shields.io/github/issues-closed/MShawon/YouTube-Viewer.svg"></a>
<a href="https://github.com/MShawon/YouTube-Viewer/issues?q=is%3Aissue+is%3Aopen"><img alt="Open issues" src="https://img.shields.io/github/issues/MShawon/YouTube-Viewer"></a>
<a href="https://saythanks.io/to/as2robot143@gmail.com"><img alt="SayThanks" src="https://img.shields.io/badge/Say-thanks!-1EAEDB.svg"></a>
<a href="https://paypal.me/shawon107"><img alt="Donate" src="https://img.shields.io/badge/Donate-PayPal-green.svg"></a>
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

**Discalimer:** This has been developed for educational purposes only.
# Requirements
 * Python 3.x
 * High speed Internet Connection
 * Good proxy list

# New feature
 Now program can search youtube with keyword and find video with video title. To do this you need to know what keyword can find your video on youtube search engine. Also you need to provide **exact** video title.
 Put keyword and title like this format `keyword : video title` in **search.txt** 

# Windows
* ## Installation 
 
  Open command prompt and type
  ```bash
  $ git clone https://github.com/MShawon/YouTube-Viewer.git

  $ cd YouTube-Viewer

  $ pip install -r requirements.txt
  ```
* ## Important
   * You need to have Google Chrome installed on your device.
   * Check your Google Chrome version and download same version **chromedriver.exe** from https://chromedriver.chromium.org/downloads here and place it in the **chromedriver_win32** folder.

   * If you've got a large proxy collection, you should run this command to filter Good proxies. Then use **GoodProxy.txt** for proxy in **youtube_viewer.py**
      ```
      $ python proxy_check.py
      ```

   * After closing program, if chromedrivers are still running. You may want to double click **killdrive.bat** to close all chrome instances.

* ## Test
  This will clear your confusion as main program will run in the background.
   ```
   $ python test.py
   ``` 

* ## Usage
   * Put youtube video links in the urls.txt. For multiple videos place urls in multple lines. (To find video link in YouTube click share and copy)
   * Open command prompt in YouTube-Viewer folder and run
        ```
        $ python youtube_viewer.py
        ```
   * Enter amount of views you want.
   * Provide number of threads. 
   * Input proxy list or let program to handle proxies automatically.

    ![alt text](demo_windows.png "Demo Windows")

# Linux
* ## Installation 
 
  Open your favourite terminal and run
  ```bash
  $ git clone https://github.com/MShawon/YouTube-Viewer.git

  $ cd YouTube-Viewer

  $ pip3 install -r requirements.txt
  ```
* ## Important
   * You need to have Google Chrome installed on your device.
   * Check your Google Chrome version and download same version **chromedriver** from https://chromedriver.chromium.org/downloads here and place it in the  **chromedriver_linux64** folder.

   * If you've got a large proxy collection, you should run this command to filter Good proxies. Then use **GoodProxy.txt** for proxy in **youtube_viewer.py**
        ```
        $ python3 proxy_check.py
        ```

   * After closing program, if chromedrivers are still running. Open your terminal and run 
      ```
      ps aux | awk '/chrome/ { print $2 } ' | xargs kill -9
      ```
* ## Test
  This will clear your confusion as main program will run in the background.
   ```
   $ python3 test.py
   ``` 

* ## Usage
   * Put youtube video links in the urls.txt. For multiple videos place urls in multple lines. (To find video link in YouTube click share and copy)
   * Open command prompt in YouTube-Viewer folder and run
        ```
        $ python3 youtube_viewer.py
        ```
   * Enter amount of views you want.
   * Provide number of threads. 
   * Input proxy list or let program to handle proxies automatically.

   ![alt text](demo_linux.png "Demo Linux")

