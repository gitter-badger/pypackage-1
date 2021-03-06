#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Makefile like python doit file [#]_ for managing easing Python packaging and
distributing related tasks. Modelled after cookiecutter-pypackage makefile [#]_

References:
    [#]: http://pydoit.org/
    [#]: https://github.com/audreyr/cookiecutter-pypackage/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/Makefile

Attributes:
    AUTHOR (str): Author's name
    PROJECT (str): Project/Package name
    GITHUB_REPO (str): Github repository name
"""
import logging
import os
import shutil

import functools

try:
    from pathlib import Path
except ImportError():
    # If using python version < 3.4
    from pathlib2 import Path


# -----------------------------------------------------------------------------
# Configurations and metadata
# -----------------------------------------------------------------------------
AUTHOR = ''
PROJECT = ''
GITHUB_REPO = ''

# Supported python versions and runtimes.
PYTHON_SUPPORT = {
    'py26': False,
    'py27': False,
    'py33': False,
    'py34': True,
    'py35': True,
    'py36': True,
    'pypy': False,
    'pypy3': False,
}

# Sphinx
SPHINXOPTS = ''
SPHINXBUILD = 'sphinx-build'
SPHINXAPIDOC = 'sphinx-apidoc'
SPHINXQUICKSTART = 'sphinx-quickstart'
SPHINXPROJ = PROJECT
SOURCEDIR = 'docs'
BUILDDIR = '_build'
APIDOCSDIR = os.path.join(SOURCEDIR, 'apidocs')


# Logging
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# doit configurations
# -----------------------------------------------------------------------------
DOIT_CONFIG = {
    'default_tasks': [],
    'verbosity': 0,
}


def set_default_task(task):
    """Decorator for setting task into default tasks

    >>> @set_default_task
    >>> def task_do_something():
    >>>     ...

    would do same as

    >>> DOIT_CONFIG['default_tasks'].append('do_something')
    """

    @functools.wraps(task)
    def wrapper(*args, **kwargs):
        name = task.__name__.strip('task_')
        globals().setdefault('DOIT_CONFIG', dict())
        DOIT_CONFIG.setdefault('default_tasks', list())
        DOIT_CONFIG['default_tasks'].append(name)
        result = task(*args, **kwargs)
        return result
    return wrapper


# -----------------------------------------------------------------------------
# Utils
# -----------------------------------------------------------------------------


def create_files(*paths):
    """Create files and folders.

    Examples:
        >>> create_files('file.txt', 'file2.txt')

    Args:
        *paths (str|Path):

    Todo:
        - write content
    """
    for filepath in map(Path, paths):
        dirname, _ = os.path.split(str(filepath))
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        filepath.touch(exist_ok=True)


def remove_files(*paths):
    """Remove files and folders. Supports unix style glob syntax.

    Examples:
        >>> remove_files('file.txt', '**/file.txt', 'file.*')

    Args:
        *paths (str|Path):
    """
    p = Path('.')
    for path in paths:
        for pathname in p.glob(str(path)):
            try:
                if pathname.is_dir():
                    shutil.rmtree(str(pathname))
                else:
                    os.remove(str(pathname))
            except FileNotFoundError:
                pass


def combine(*tasks):
    """Combine actions of different tasks

    Examples:
        >>> combine({'actions': ['action1']}, {'actions': ['action2']})
        {'actions': ['action1', 'action2']}

    Args:
        *tasks (dict): Tasks that containing actions to be combined
    """
    return {'actions': sum((task.get('actions', []) for task in tasks), [])}


# -----------------------------------------------------------------------------
# doit tasks
# -----------------------------------------------------------------------------


def task_setup_project():
    """Create basic project file structure"""
    files = ['README.rst', 'LICENSE.txt', 'requirements.txt',
             'requirements-dev.txt']
    return {'actions': [(create_files, files)]}


def task_setup_git():
    return {'actions': ['git init',
                        (create_files, ['.gitignore'])]}


def task_clean_build():
    """Clean build artifacts"""
    files = ['build/', 'dist/', '.eggs/', '*.egg-info', '*.egg']
    return {'actions': [(remove_files, files)]}


def task_clean_pyc():
    """Clean python file artifacts"""
    files = ['*.pyc', '*.pyo', '*~', '__pycache__']
    return {'actions': [(remove_files, files)]}


def task_clean_test():
    """Clean test and coverage artifacts"""
    files = ['.tox/', '.coverage', 'htmlcov/']
    return {'actions': [(remove_files, files)]}


def task_setup_docs():
    """Invoke sphinx-quickstart"""
    return {'actions': [
        ['sphinx-quickstart', SOURCEDIR, '-p', PROJECT, '-a', AUTHOR,
         '-v', '"0.1"', '-l', '"en"', '--makefile', '--batchfile',
         '--quiet']]}


def task_clean_docs():
    """Clean documentation"""
    files = [os.path.join(SOURCEDIR, BUILDDIR)]
    return {'actions': [(remove_files, files)]}


def task_apidocs():
    """Build apidocs"""
    return {'actions': [
        [SPHINXAPIDOC, PROJECT, '-o', APIDOCSDIR, '-E', '--no-toc',
         '--force']
    ]}


def task_docs(builder='html'):
    """Build docs with defined ``builder``"""
    return {'actions': [
        [SPHINXBUILD, '-b', builder, SOURCEDIR, BUILDDIR, SPHINXOPTS]
    ]}


def task_release_docs():
    """Release the full compiled documentation

    1. Clean old docs
    2. build apidocs
    3. Compile html
    4. Release the docs
        a) github pages using ghp-import
        b) readthedocs.org
    """
    html_docs_dir = os.path.join(SOURCEDIR, BUILDDIR, 'html')
    return combine(task_clean_docs(),
                   task_apidocs(),
                   task_docs('html'),
                   {'actions': [['ghp-import', html_docs_dir]]})


def task_setup_coverage():
    """Create coverage files"""
    files = ['.coveragerc']
    return {'actions': [(create_files, files)]}


def task_coverage():
    """Run coverage for the project"""
    return {'actions': []}


def task_setup_pytest():
    """Create configuration pytest"""
    files = ['pytest.ini', 'conftest.py']
    return {'actions': [(create_files, files)]}


def task_setup_tox():
    """Create tox configuration file"""
    files = ['tox.ini']
    return {'actions': [(create_files, files)]}


def task_test():
    """Run tests

    - py.test
    - tox
    - setup.py test
    """
    return {'actions': ['py.test']}


def task_setup_versioneer():
    """Setup versioneer"""
    return {'actions': ['versioneer', 'install']}


def task_setuptools():
    """Initialise setup.py and setup.cfg

    Todo:
         - setup.py from template
    """
    files = ['setup.py', 'setup.cfg']
    return {'actions': [(create_files, files)]}


def task_dist():
    """Build Python distribution"""
    return {'actions': ['python setup.py sdist bdist_wheel']}


def task_release_pypi():
    """Upload a release of the package into PyPI"""
    return {'actions': []}


def task_release_conda():
    """Upload a release of the package into conda-forge"""
    return {'actions': []}


def task_setup_travis():
    files = ['.travis.yml']
    return {'actions': [(create_files, files)]}


def task_setup_appreyor():
    files = ['appreyor.yml']
    return {'actions': [(create_files, files)]}


def task_setup_cli():
    """Setup commandline client for the project

    Todo:
        - load from template
        - Options
            - argparse
            - click
            - docopt
            - ...
    """
    return {'actions': []}


def task_add_cli_entry_points():
    """Add commandline interface entry points to setup.py"""
    return {'actions': []}
