#!/usr/bin/env python
"""
Setup script for YouTube Viewer
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
def read_requirements(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

install_requires = read_requirements('requirements-updated.txt')

setup(
    name="youtube-viewer-bot",
    version="2.0.0",
    author="Updated by AI Assistant",
    author_email="your-email@example.com",
    description="Advanced YouTube view automation tool with modern Chrome compatibility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/YouTube-Viewer",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/YouTube-Viewer/issues",
        "Source": "https://github.com/yourusername/YouTube-Viewer",
        "Documentation": "https://github.com/yourusername/YouTube-Viewer#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Environment :: Web Environment",
    ],
    python_requires=">=3.7,<3.12",
    install_requires=install_requires,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "isort>=5.10.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pytest-mock>=3.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "youtube-viewer=youtube_viewer:main",
        ],
    },
    include_package_data=True,
    package_data={
        "youtubeviewer": [
            "web/static/*",
            "web/templates/*",
        ],
        "": [
            "extension/**/*",
            "README.md",
            "LICENSE",
            "CHANGELOG.md",
        ],
    },
    zip_safe=False,
    keywords="youtube automation selenium chrome webdriver views bot",
    platforms=["Windows", "macOS", "Linux"],
)
