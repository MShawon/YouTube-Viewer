# Contributing to YouTube Viewer

We love your input! We want to make contributing to YouTube Viewer as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `master`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/yourusername/YouTube-Viewer/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/YouTube-Viewer/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Setup

### Prerequisites

- Python 3.7-3.11 (3.11 recommended)
- Google Chrome (latest version)
- Git

### Setup Instructions

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/YouTube-Viewer.git
   cd YouTube-Viewer
   ```

2. **Create a virtual environment**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements-updated.txt
   ```

4. **Install development dependencies** (if applicable)
   ```bash
   pip install pytest black flake8 mypy
   ```

## Code Style

We use several tools to maintain code quality:

### Formatting
- **Black** for code formatting
- **isort** for import sorting

```bash
black youtube_viewer.py youtubeviewer/
isort youtube_viewer.py youtubeviewer/
```

### Linting
- **flake8** for style guide enforcement
- **mypy** for type checking (optional)

```bash
flake8 youtube_viewer.py youtubeviewer/
mypy youtube_viewer.py youtubeviewer/
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_basics.py

# Run with coverage
pytest --cov=youtubeviewer
```

### Writing Tests

- Write tests for new features
- Ensure existing tests pass
- Aim for good test coverage
- Use descriptive test names

Example test structure:
```python
def test_get_driver_creation():
    """Test that Chrome driver can be created successfully."""
    # Test implementation
    pass
```

## Project Structure

```
YouTube-Viewer/
├── youtube_viewer.py          # Main application entry point
├── youtubeviewer/            # Core package
│   ├── __init__.py
│   ├── basics.py             # Basic utilities and driver management
│   ├── bypass.py             # Anti-detection and bypass methods
│   ├── colors.py             # Terminal color utilities
│   ├── config.py             # Configuration management
│   ├── database.py           # Database operations
│   ├── download_driver.py    # ChromeDriver management
│   ├── features.py           # Advanced features and automation
│   ├── load_files.py         # File loading utilities
│   ├── proxies.py            # Proxy management
│   └── website.py            # Web dashboard
├── extension/                # Browser extensions
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── tests/                    # Test files (if applicable)
```

## Feature Development Guidelines

### Adding New Features

1. **Design First**: Create an issue describing the feature
2. **Discuss**: Get feedback from maintainers and community
3. **Implement**: Write clean, well-documented code
4. **Test**: Ensure thorough testing
5. **Document**: Update README and relevant documentation

### Code Guidelines

- **Modularity**: Keep functions small and focused
- **Documentation**: Use clear docstrings and comments
- **Error Handling**: Implement proper exception handling
- **Logging**: Use appropriate logging levels
- **Performance**: Consider performance implications

### Example Code Style

```python
def create_driver(proxy: str, headless: bool = False) -> webdriver.Chrome:
    """
    Create a Chrome WebDriver instance with specified configuration.
    
    Args:
        proxy: Proxy string in format 'ip:port' or 'user:pass@ip:port'
        headless: Whether to run browser in headless mode
        
    Returns:
        Configured Chrome WebDriver instance
        
    Raises:
        WebDriverException: If driver creation fails
    """
    try:
        options = setup_chrome_options(proxy, headless)
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        logger.error(f"Failed to create driver: {e}")
        raise WebDriverException(f"Driver creation failed: {e}")
```

## Compatibility Guidelines

### Python Versions
- Support Python 3.7-3.11
- Test against multiple Python versions
- Use type hints where appropriate
- Avoid Python 3.12+ specific features

### Browser Compatibility
- Primary focus: Chrome/Chromium
- Test with latest Chrome versions
- Maintain compatibility with ChromeDriver updates
- Handle version mismatches gracefully

### Operating Systems
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+, CentOS 7+)

## Security Considerations

When contributing, please consider:

- **No hardcoded credentials** in code
- **Secure proxy handling** - don't log sensitive data
- **Input validation** for user-provided data
- **Safe file operations** - avoid path traversal
- **Memory management** - clean up resources properly

## Legal and Ethical Guidelines

- Code should be for **educational purposes**
- Include appropriate **disclaimers**
- Respect **terms of service** discussions
- Consider **rate limiting** and **abuse prevention**
- Document **responsible usage** patterns

## Questions?

Don't hesitate to ask questions in:
- GitHub Issues
- Pull Request discussions
- Community forums

## Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes
- CHANGELOG.md

Thank you for contributing to YouTube Viewer! 🎉
