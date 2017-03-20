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
import os
import shutil
from functools import reduce
from glob import iglob

# Package metadata
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
DOIT_CONFIG = {}


def remove_files(*pathnames, recursive=False):
    """Remove files and folders using unix style glob syntax.

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


def combine(*tasks):
    """Combine actions of different tasks"""
    return {'actions': sum((task['actions'] for task in tasks), [])}


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


def task_make_docs():
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


def task_deploydocs():
    """Clean old docs, build apidocs, compile html and import docs into gh-pages
    branch"""
    html_docs_dir = os.path.join(SOURCEDIR, BUILDDIR, 'html')
    return combine(task_clean_docs(),
                   task_apidocs(),
                   task_docs('html'),
                   {'actions': [['ghp-import', html_docs_dir]]})


def task_coverage():
    """Run coverage for the project"""
    pass


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


def release():
    """Upload a release of the package."""
    pass
