#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Makefile like python doit file [#]_ for managing easing Python packaging and
distributing related tasks. Modelled after cookiecutter-pypackage makefile [#]_

References:
    [#]: http://pydoit.org/
    [#]: https://github.com/audreyr/cookiecutter-pypackage/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/Makefile

Attributes:
    AUTHOR (str): Author's name
    PACKAGE (str): Package name
    GITHUB_REPO (str): Github repository name
"""
import logging
import os
import shutil

try:
    from pathlib import Path
except ImportError():
    # If using python version < 3.4
    from pathlib2 import Path


# -----------------------------------------------------------------------------
# Configurations and metadata
# -----------------------------------------------------------------------------
AUTHOR = ''
PACKAGE = ''
GITHUB_REPO = ''

# Sphinx
SPHINXOPTS = ''
SPHINXBUILD = 'sphinx-build'
SPHINXAPIDOC = 'sphinx-apidoc'
SPHINXQUICKSTART = 'sphinx-quickstart'
SPHINXPROJ = PACKAGE
SOURCEDIR = 'docs'
BUILDDIR = '_build'
APIDOCSDIR = os.path.join(SOURCEDIR, 'apidocs')

# doit configurations
DOIT_CONFIG = {
    # 'default_tasks': [],
    'verbosity': 0,
}

# Logging
logger = logging.getLogger(__name__)


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


def task_clean_build():
    """Clean build artifacts"""
    return {'actions': [(remove_files,
                         ['build/', 'dist/', '.eggs/', '*.egg-info', '*.egg'])]}


def task_clean_pyc():
    """Clean python file artifacts"""
    return {'actions': [
        (remove_files, ['*.pyc', '*.pyo', '*~', '__pycache__'])]}


def task_clean_test():
    """Clean test and coverage artifacts"""
    return {'actions': [(remove_files, ['.tox/', '.coverage', 'htmlcov/'])]}


def task_init_docs():
    """Invoke sphinx-quickstart"""
    return {'actions': [
        ['sphinx-quickstart', SOURCEDIR, '-p', PACKAGE, '-a', AUTHOR,
         '-v', '"0.1"', '-l', '"en"', '--makefile', '--batchfile',
         '--quiet']]}


def task_clean_docs():
    """Clean documentation"""
    return {'actions': [(remove_files, [os.path.join(SOURCEDIR, BUILDDIR)])]}


def task_apidocs():
    """Build apidocs"""
    return {'actions': [
        [SPHINXAPIDOC, PACKAGE, '-o', APIDOCSDIR, '-E', '--no-toc',
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
    return {'actions': [['touch', '.coveragerc']]}


def task_coverage():
    """Run coverage for the project"""
    return {'actions': []}


def task_setup_pytest():
    """Create configuration pytest"""
    return {'actions': [['touch', 'pytest.ini', 'conftest.py']]}


def task_setup_tox():
    """Create tox configuration file"""
    return {'actions': [['touch', 'tox.ini']]}


def task_test():
    """Run tests

    - py.test
    - tox
    - setup.py test
    """
    return {'actions': ['py.test']}


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
    return {'actions': [['touch', '.travis.yml']]}


def task_setup_appreyor():
    return {'actions': [['touch', 'appreyor.yml']]}
