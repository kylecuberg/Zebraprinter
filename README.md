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
  - [Installation](#installation)
  - [Use](#use)
  - [ToDo](#todo)

## Requirements

Python 3.10 is the currently supported version.
If you wish to change this, you may use any version >3.7, but if you plan to edit, the version of python must be updated in the pyproject.toml in the "target_version" under tool.black

## Installation

1. Make sure computer has Python installed & you know the location of the python executable file.
2. Download & extract files from Github
3. Move whole folder to desired location
4. Must run this line from command line for new users:
   py -m pip install {file_location where zip was extracted to}
5. In the excel file, right click the button.
6. Click "assign macro", then "edit"
7. In the macro, set the PythonExe variable to your computers file location of python.exe (found in step 1)
   - For easiest scenario, python will be installed for all users.
8. In the macro, set the PythonScriptExe to the location of the "{}\src\cell.py" file (beginning part should match the file location)
9. For manual, follow 8 but set the PythonScriptExe to the location of the "{}\src\manual.py" file (beginning part should match the file location)
10. You will need to get the private.py file from @kylecuberg to get the connection info!

## Use

Most scripts within this project will take an input, query against SPARC for the rest of the appropriate information (as well as verify the information provided was contained within SPARC), and send a string of characters to the appropriate printer for the label type/size associated.

For most items, there will be an associated .bat file. This is a command line prompt that runs the python script for you.

For the remaining items, there is an excel file. Enter the serials in the first column, and hit the macro button to print those serials.
THe "manual" macro in the excel file is the only script that does not reference SPARC. Instead, it simply takes the given serials and barcodes & outputs the labels.

NOTE: Each time the excel macro gets run, the file will autosave before the script executes.

## ToDo

- [] Add "manual" macro to xlsb
- [] Dynamic referencing in xlsb macro to prevent needing to edit macro for each new user?
- [] Update qrtext.sn to be mirror processboxlabel generalization
- [X] Update qrtext.boxlabel to be mirror processboxlabel generalization
- [] Update wo.py to use qrtext class
- [] Add pouch to qrtext class
- [] Update pouch.py to use qrtext class
- [X] V1/V2 cells stored differently, need alt query
