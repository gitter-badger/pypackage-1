"""Makefile like task runner for managing easing Python packaging and
distributing related tasks. Modelled after cookiecutter-pypackage makefile [#]_

References:
    [#]: https://github.com/audreyr/cookiecutter-pypackage/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/Makefile
"""
import os
import shutil
from glob import iglob

GITHUB_REPO = ''
PACKAGE_NAME = ''
DOCS_DIR = 'docs'


def remove_files(*pathnames, recursive=False):
    """Remove files and folders using unix style glob syntax

    Args:
        pathnames (str):
        recursive (bool):
    """
    for pathname in pathnames:
        for path in iglob(pathname, recursive=recursive):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)


def task_clean_build():
    """Clean build artifacts"""
    return {
        'actions': [remove_files,
                    ['build/', 'dist/', '.eggs/', '*.egg-info', '*.egg']],
    }


def task_clean_pyc():
    """Clean python file artifacts"""
    return {
        'actions': [remove_files,
                    ['*.pyc', '*.pyo', '*~', '__pycache__']],
    }


def task_clean_test():
    """Clean test and coverage artifacts"""
    return {
        'actions': [remove_files,
                    ['.tox/', '.coverage', 'htmlcov/']],
    }


def task_clean():
    """Clean build, pyc and test artifacts"""
    tasks = (task_clean_pyc, task_clean_test, task_clean_build)
    for task in tasks:
        yield task()


def apidocs():
    """Build apidocs"""
    pass


def docs():
    """Build html docs"""
    pass


def deploydocs():
    """Clean old docs, build apidocs, compile html and and push the docs into
    GitHub pages."""
    pass


def dist():
    """Build Python distribution"""
    return {
        'actions': ['python setup.py sdist bdist_wheel']
    }
