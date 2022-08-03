# Overview of useful python resources & common commands.

## Resources
- [PEP-8](https://realpython.com/python-pep8/)
- [Writing Structure](https://docs.python-guide.org/writing/structure/)
- [Google's Python Writing Guide](https://google.github.io/styleguide/pyguide.htm)


## Common Commands

To create virtual environment:
>   py -m venv env

To activate virtual environments
>   env\Scripts\activate

To install project
>   py -m pip install .
>   py -m pip install .[dev]

Pre-commit setup after install of project
>   pre-commit install

>   pre-commit autoupdate


## Before commiting:
1. Pre-commit check
>   pre-commit run --all-files

2. Flake8
>   flake8 src --exit-zero --format=html --htmldir reports/flake8 --statistics --tee --output-file reports/flake8/flake8stats.txt

3. Coverage
>   py -m coverage run -m unittest discover -s tests

>   coverage xml -o reports/coverage/coverage.xml

4. For genbadge (must do both those modules (ie flake8/coverage) commands first)
>   genbadge flake8 --output-file ./reports/flake8/badge.svg

>   genbadge coverage --output-file ./reports/coverage/badge.svg  
