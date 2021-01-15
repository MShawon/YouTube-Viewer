![ViewCount](https://views.whatilearened.today/views/github/MShawon/YouTube-Viewer.svg)

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
  
# Installation 
 Open command prompt and type
 ```bash
 $ git clone https://github.com/MShawon/YouTube-Viewer.git

 $ cd YouTube-Viewer

 $ pip install -r requirements.txt
 ```
## Important
 * You need to have Google Chrome installed on your device.
 * Check your Google Chrome version and download same versions **chromedriver.exe** from https://chromedriver.chromium.org/downloads here and place it in the **chromedriver_win32** and **chromedriver_linux64** folder respectively for Windows and Linux.

 * If you've got a large proxy collection, you should run this command to filter Good proxies. Then use `GoodProxy.txt` for proxy in `youtube_viewer.py`
      ### Windows
      ```
      $ python proxy_check.py
      ```
      ### Linux
      ```
      $ python3 proxy_check.py
      ```

 * After closing program, if chromedrivers are still running . 
 For Windows, you may want to double click `killdrive.bat` to close all chrome instances.
 For Linux, in terminal run `ps aux | awk '/chrome/ { print $2 } ' | xargs kill -9`

# Usage
 * Put youtube video links in the urls.txt. For multiple videos place urls in multple lines. (To find video link in YouTube click share and copy)
 * Open command prompt in YouTube-Viewer folder and run
    ### Windows
      ```
      $ python youtube_viewer.py
      ```
    ### Linux
      ```
      $ python3 youtube_viewer.py
      ```
 * Enter amount of views you want.
 * Provide number of threads. 
 * Input proxy list or let program to automatically handle proxies.

 ![alt text](demo_windows.png "Demo Windows")
 ![alt text](demo_linux.png "Demo Linux")

