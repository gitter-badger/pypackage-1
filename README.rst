Tools for Creating and Managing Python Packages
-----------------------------------------------
Directory structure

::

    .
    ├── docs/                   # Sphinx documentation
    |   ├── index.rst
    |   ├── makefile            # Unix style makefile for sphinx
    |   ├── make.dot            # Windows style makefile for sphinx
    |   ├── conf.py             # Sphinx configuration file
    |   └── ...
    ├── package/
    |   ├── module/             # Module inside the package
    |   |   ├── tests/          # Pytest directory. Each module contains its own tests
    |   |   └── ...
    |   ├── __init__.py
    |   ├── _version.py         # Versioneer file. Created by versioneer.
    |   ├── logging.{yml,json,py}   # Logging configuration file. Can be yaml, json or python file.
    |   ├── exceptions.py       # Project exceptions
    |   ├── cli.py              # Commandline interface
    |   └── ...
    ├── .git/                   # Git repository
    ├── .gitignore              # Git ignore file
    ├── LICENSE                 # License
    ├── README                  # Readme
    ├── setup.cfg               # Setup configurations
    ├── setup.py                # Main setup file
    ├── MANIFEST                # Manages which files are included in the distribution
    ├── requirements.txt        # Libraries that are required to install this package
    ├── requirements-dev.txt    # Libraries that are required for developing this package
    ├── pytest.ini              # Pytest configuration file
    ├── tox.ini                 # Tox configuration file.
    ├── conftest.py             # More pytest configurations
    ├── .coveragerc             # Coverage configurations
    ├── .travis.yml             # Travis configurations
    ├── apprevor.yml            # Apprevor configurations
    ├── dodo.py                 # Task automation file for python doit
    └── ...
