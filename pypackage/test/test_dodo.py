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
        yield Path(directory)


@pytest.fixture(scope='module')
def files():
    return tuple(map(Path, ('file.txt', 'file2.txt')))


def test_create_files(tmpdir, files):
    with tmpdir:
        create_files(*files)
        for file in files:
            assert file.exists()


def test_remove_files(tmpdir, files):
    with tmpdir:
        remove_files(*files)
        for file in files:
            assert not file.exists()


def test_combine():
    assert True
