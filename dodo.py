"""Makefile like python doit file [#]_ for managing easing Python packaging and
distributing related tasks. Modelled after cookiecutter-pypackage makefile [#]_

References:
    [#]: http://pydoit.org/
    [#]: https://github.com/audreyr/cookiecutter-pypackage/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/Makefile

Attributes:
    PACKAGE: Package name
    GITHUB_REPO: Github repository name
    DOCS_DIR:
    APIDOCSDIR:
"""
import os
import shutil
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


def task_clean_build():
    """Clean build artifacts"""
    return {'basename': 'clean_build',
            'actions': [(remove_files,
                         ['build/', 'dist/', '.eggs/', '*.egg-info', '*.egg'])]}


def task_clean_pyc():
    """Clean python file artifacts"""
    return {'basename': 'clean_pyc',
            'actions': [
                (remove_files, ['*.pyc', '*.pyo', '*~', '__pycache__'])]}


def task_clean_test():
    """Clean test and coverage artifacts"""
    return {'basename': 'clean_test',
            'actions': [(remove_files, ['.tox/', '.coverage', 'htmlcov/'])]}


def task_make_docs():
    """Invoke sphinx-quickstart"""
    return {'basename': 'make_docs',
            'actions': [
                ['sphinx-quickstart', SOURCEDIR, '-p', PACKAGE, '-a', AUTHOR,
                 '-v', '"0.1"', '-l', '"en"', '--makefile', '--batchfile',
                 '--quiet']]}


def task_clean_docs():
    """Clean documentation"""
    return {'basename': 'clean_docs',
            'actions': [(remove_files, [os.path.join(SOURCEDIR, BUILDDIR)])]}


def task_apidocs():
    """Build apidocs"""
    return {'basename': 'apidocs',
            'actions': [
                [SPHINXAPIDOC, PACKAGE, '-o', APIDOCSDIR, '-E', '--no-toc',
                 '--force']
            ]}


def task_docs(builder='html'):
    """Build docs with defined ``builder``"""
    return {'basename': 'docs',
            'actions': [
                [SPHINXBUILD, '-b', builder, SOURCEDIR, BUILDDIR, SPHINXOPTS]
            ]}


# def task_deploydocs():
#     """Clean old docs, build apidocs, compile html and import docs into gh-pages
#     branch"""
#     yield task_clean_docs()
#     yield task_apidocs()
#     yield task_docs('html')
#     html_docs_dir = os.path.join(SOURCEDIR, BUILDDIR, 'html')
#     return {'basename': 'deploydocs',
#             'actions': [['ghp-import', html_docs_dir]]}


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
