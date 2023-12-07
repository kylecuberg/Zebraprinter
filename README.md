# Zebra Printing

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Flake8 Status](./reports/flake8/badge.svg)](./reports/flake8/index.html)
[![Coverage Status](./reports/coverage/badge.svg)](./reports/coverage/badge.svg)
[![pre-commit enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
<!-- [![Status](https://img.shields.io/badge/status-active-success.svg)]() -->
[![GitHub Issues](https://img.shields.io/github/issues/kylecuberg/zebraPrinter.svg)](https://github.com/kylecuberg/zebraPrinter/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylecuberg/zebraPrinter.svg)](https://github.com/kylecuberg/zebraPrinter/pulls)
[![Python](https://img.shields.io/pypi/pyversions/cookiecutter-hypermodern-python-instance)](https://www.python.org/downloads/release/python-3100/)

## About

This project is intended to meet the requirements of PEP-518 and PEP-621, removing the setup.py file and having only minor use of setup.cfg (intended at this time only for flake8 support)

## Contents

- [Zebra Printing](#zebra-printing)
  - [About](#about)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Installation - Windows](#installation---windows)
  - [Installation - Mac](#installation---mac)
  - [Use](#use)
  - [ToDo](#todo)

## Requirements

Python 3.10+ is the currently supported version.
If you wish to change this, you may use any version >3.7, but if you plan to edit, the version of python must be updated in the pyproject.toml in the "target_version" under tool.black

## Installation - Windows

Project has been updated to utilize an executable gui.
Installation is the download of the executable.

## Installation - Mac

Executable does not work for mac, and there is no support for Mac yet planned.

## Use

Download the .exe file and run
Executable is under dist/all_label_gui.exe

![image](docs/Program Images/Main Screen.png)

## ToDo

- [x] V1/V2 cells stored differently, need alt query
- [x] Add EL label printing
- [x] Simpler installation guide? Add python installation descriptions & figure out how to do it not using VSCode
- [x] Separate dryroom & cage printing
- [ ] Clearer labels for functions
- [ ] Simplify the way to get the item check (SQL query)?
- [x] Removed large file check, allow application to be easily downloaded
