# 🎬 YouTube Viewer Bot

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.7--3.11-blue">
  <img alt="OS" src="https://img.shields.io/badge/OS-Windows%20|%20Linux%20|%20macOS-success">
  <img alt="Chrome" src="https://img.shields.io/badge/Chrome-Latest-green">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow">
</p>

<p align="center">
  <strong>🚀 Updated & Compatible with Modern Chrome Versions (2025)</strong>
</p>

```
    Yb  dP  dP"Yb  88   88 888888 88   88 88""Yb 888888
     YbdP  dP   Yb 88   88   88   88   88 88__dP 88__   
      8P   Yb   dP Y8   8P   88   Y8   8P 88""Yb 88""   
     dP     YbodP  `YbodP'   88   `YbodP' 88oodP 888888 

                         Yb    dP 88 888888 Yb        dP 888888 88""Yb 
                          Yb  dP  88 88__    Yb  db  dP  88__   88__dP 
                           YbdP   88 88""     YbdPYbdP   88""   88"Yb  
                            YP    88 888888    YP  YP    888888 88  Yb
```

## 📊 Overview

An advanced YouTube view automation tool that simulates real user behavior to generate organic-looking views. This updated version includes modern Chrome compatibility fixes and enhanced stealth features.

## ⚠️ Legal Disclaimer

> **FOR EDUCATIONAL PURPOSES ONLY**
> 
> This tool is provided for educational and research purposes only. Using this tool to artificially inflate YouTube views violates YouTube's Terms of Service and may result in penalties including video removal or channel termination. Use at your own risk.

## ✨ Features

### 🔥 Core Functionality
- **Multi-threaded view generation** with configurable worker count
- **Real browser automation** using undetected ChromeDriver
- **Smart proxy rotation** with geo-location spoofing
- **Anti-detection measures** including fingerprint spoofing
- **Live stream support** for real-time view generation
- **YouTube Music compatibility** for music videos

### 🛡️ Stealth & Security
- **Canvas fingerprint defender** to mask browser fingerprints
- **WebRTC leak prevention** to hide real IP addresses
- **User agent randomization** across multiple browsers and OS
- **Timezone spoofing** to match proxy locations
- **Audio fingerprint defense** against audio-based tracking

### 📱 Platform Support
- **Desktop browsers**: Chrome, Firefox, Opera
- **Operating systems**: Windows, macOS, Linux
- **Multiple architectures**: x64, x86, ARM (where supported)

### 🌐 Traffic Source Simulation
- YouTube Search results
- Suggested/Recommended videos
- External referrals (Google, Twitter, etc.)
- Direct links
- Channel page visits
- End screen clicks

### 📈 Monitoring & Analytics
- **Real-time web dashboard** at `localhost:5000`
- **SQLite database logging** for view tracking
- **Live geographic distribution** of generated views
- **Performance metrics** and success rates

## 🔧 Requirements

- **Python 3.7 - 3.11** (Python 3.13+ not supported)
- **Google Chrome** (latest version)
- **High-speed internet connection**
- **Proxy list** (HTTP/HTTPS/SOCKS4/SOCKS5)

## 📦 Installation

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/YouTube-Viewer.git
   cd YouTube-Viewer
   ```

2. **Create virtual environment** (Python 3.11 recommended)
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your setup**
   - Add video URLs to `urls.txt`
   - Add search terms to `search.txt`
   - Configure proxies in the script interface

5. **Run the application**
   ```bash
   python youtube_viewer.py
   ```

## ⚙️ Configuration

### URLs Configuration (`urls.txt`)
```
https://www.youtube.com/watch?v=VIDEO_ID_1
https://www.youtube.com/watch?v=VIDEO_ID_2
https://music.youtube.com/watch?v=MUSIC_ID
```

### Search Configuration (`search.txt`)
```
python tutorial :::: Learn Python in 2025
music video :::: Best Songs 2025
gaming :::: Epic Gaming Moments
```

### Proxy Configuration
Supported formats:
- `ip:port`
- `username:password@ip:port`
- `ip:port:username:password`

## 🚀 Advanced Features

### Web Dashboard
Access the real-time dashboard at `http://localhost:5000` to monitor:
- Active workers and their status
- Geographic distribution of views
- Success/failure rates
- View count statistics

### Database Logging
All activities are logged to SQLite database for analysis:
- View timestamps and durations
- Proxy performance metrics
- Geographic data
- Error tracking

### Bandwidth Optimization
- Automatic video quality reduction
- Smart ad skipping
- Efficient resource management

## 🔒 Security Features

### Anti-Detection
- **Browser fingerprint randomization**
- **Canvas and WebGL spoofing**
- **Font fingerprint variation**
- **Screen resolution randomization**
- **Timezone synchronization with proxy location**

### Privacy Protection
- **WebRTC leak prevention**
- **DNS leak protection**
- **Real IP masking**
- **Secure proxy chain management**

## 📊 Performance Optimization

### Threading Configuration
- Minimum threads: 2
- Maximum threads: 5 (configurable)
- Dynamic thread scaling based on performance

### Watch Duration
- Minimum: 45% of video length
- Maximum: 50% of video length
- Randomized for organic appearance

### Proxy Management
- Automatic proxy validation
- Health checking and rotation
- Geographic distribution tracking

## 🛠️ Troubleshooting

### Common Issues

**Chrome Driver Compatibility**
```bash
# If you encounter ChromeDriver issues:
pip install --upgrade undetected-chromedriver webdriver-manager
```

**Python Version Issues**
```bash
# Check your Python version:
python --version

# Must be between 3.7 and 3.11
```

**Proxy Connection Problems**
- Verify proxy credentials
- Test proxy connectivity manually
- Check firewall settings

### Error Messages
- `WebDriverException`: Usually indicates Chrome compatibility issues
- `ProxyError`: Check proxy configuration and connectivity
- `TimeoutError`: Increase timeout values in config

## 📈 Best Practices

1. **Use quality proxies** - Residential proxies work best
2. **Rotate proxy pools** - Don't reuse the same proxies repeatedly
3. **Moderate view counts** - Don't generate excessive views quickly
4. **Monitor geographic distribution** - Ensure realistic geographic spread
5. **Use multiple video sources** - Mix direct URLs and search terms

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original YouTube Viewer by [MShawon](https://github.com/MShawon/YouTube-Viewer)
- Undetected ChromeDriver project
- WebDriver Manager for automated driver management

## 💰 Support

If this project helps you, consider supporting development:

**PayPal**: [paypal.me/mshawon1](https://paypal.me/mshawon1)  
**Bitcoin**: `1Jh8KZ6khuHayNDeVV9tEzYSq9FPExKCAH`

---

<p align="center">
  <strong>⚡ Updated for 2025 with modern Chrome compatibility</strong>
</p>
