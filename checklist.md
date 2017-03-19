Python Packaging Checklist
--------------------------
Directory structure

```
.
├── docs/                   # Sphinx documentation
|   ├── index.rst
|   ├── makefile
|   ├── make.dot
|   └── ...
├── package/
|   ├── module/             # Module inside the package
|   |   ├── tests/          # Pytest directory. Each module contains its own tests
|   |   └── ...
|   ├── __init__.py
|   ├── _version.py         # Versioneer file. Created by versioneer.
|   ├── logging.py |        # Logging configuration file
        logging.yaml
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
├── pytest.ini |            # Pytest configuration file
    tox.ini                 # Tox configuration file. Can contain pytest configurations
├── conftest.py             # More pytest configurations
├── .coveragerc             # Coverage configurations
├── .travis.yml             # Travis configurations 
├── apprevor.yml            # Apprevor configurations
└── ...
```

Python version support

- [ ] py26
- [ ] py27
- [ ] py33
- [ ] py34
- [ ] py35
- [ ] py36
- [ ] pypy
- [ ] pypy3


Common files and modules

- [ ] License
    - [ ] https://choosealicense.com/
    - [ ] https://github.com/licenses/license-templates
- [ ] Readme
- [ ] Version Control
    - [ ] git repository
    - [ ] gitignore file
- [ ] Setuptools
    - [ ] setup.py
    - [ ] MANIFEST
- [ ] requirements.txt
- [ ] requirements-dev.txt
- [ ] Tests
    - [ ] pytest
    - [ ] tox
    - [ ] Coverage
        - [ ] pytest-cov
        - [ ] .coveragerc 
- [ ] Documentation
    - [ ] Sphinx
- [ ] Versioning
    - [ ] Versioneer

Common but optional files and modules

- [ ] `__init__.py`
- [ ] Logging
- [ ] Exceptions
- [ ] Command line client & entry points

 Services
 
- [ ] Remote Repository
    - [ ] GitHub
    - [ ] BitBucket
    - [ ] GitLab
- [ ] Continuous Integration
    - [ ] travis
    - [ ] appveyor
    - [ ] circle-ci
- [ ] Dependency Management
    - [ ] Pyup
- [ ] Distributing
    - [ ] PyPI
    - [ ] Conda
        - [ ] environment.yml
- [ ] Communication / Chat
    - [ ] Gitter
- [ ] Coverage
    - [ ] coveralls.io

Task Automation

- [ ] Makefile
- [ ] dodo.py
