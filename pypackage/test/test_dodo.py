import contextlib
import os
from tempfile import TemporaryDirectory
import pytest

from pypackage.dodo import create_files, remove_files

try:
    from pathlib import Path
except ImportError:
    # If using python version < 3.4
    from pathlib2 import Path


@pytest.fixture(scope='module')
def tmpdir():
    """Temporary directory"""
    with TemporaryDirectory() as directory:
        @contextlib.contextmanager
        def remember_cwd():
            curdir = os.getcwd()
            try:
                os.chdir(directory)
                yield
            finally:
                os.chdir(curdir)
        yield remember_cwd


@pytest.fixture(scope='module')
def files():
    return 'file.txt', 'file2.txt'


def test_create_files(tmpdir, files):
    with tmpdir():
        create_files(*files)
        for file in files:
            assert Path(file).exists()


def test_remove_files(tmpdir, files):
    with tmpdir():
        remove_files(*files)
        for file in files:
            assert not Path(file).exists()


def test_combine():
    assert True
