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
  - [Installation](#installation)

## Installation

1. Download & extract from Github
2. In core.py  set the cell_list value to the file location of the xlsb file (where this setup is installed)
   1. "C:\Users\KylePatterson\Documents\CubergGithub\zebraPrinter\input\Print_File.xlsb" is current, only the "{}\input\Print_file.xlsb" will be the same for yours
3. In the excel file, right click the button.
4. Click "assign macro", then "edit"
5. in the macro, set the PythonExe to your computers file location of python.exe
   - For easiest scenario, install python for all users, and find that location
6. In the macro, set the PythonScriptExe to the location of the "{}\src\core.py" file (beginning part should match the {}from like 2.1 above)

Each time the excel macro gets run, the file will need to be saved before the script executes.

For workorders, use the input bat file. It will prompt for work order & run.

Must run this line from command line for new users:
   py -m pip install C:\Users\KylePatterson\Documents\CubergGithub\zebraPrinter
