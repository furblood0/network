#!/usr/bin/env python3
"""
BeQuickChat - UDP Tabanlı Çok Kullanıcılı Sohbet Uygulaması
Kurulum dosyası
"""

from setuptools import setup, find_packages
import os

# README dosyasını oku
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# requirements.txt dosyasını oku
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="bequickchat",
    version="1.0.0",
    author="Beyza Nur Selvi, Furkan Fidan",
    author_email="",
    description="UDP tabanlı çok kullanıcılı sohbet uygulaması",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bequickchat",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Chat",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "bequickchat-server=src.server:main",
            "bequickchat-client=src.client:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/*.png", "assets/*/*.png"],
    },
    keywords="chat, udp, networking, gui, pyqt5",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/bequickchat/issues",
        "Source": "https://github.com/yourusername/bequickchat",
        "Documentation": "https://github.com/yourusername/bequickchat/blob/main/docs/README.md",
    },
) 