
import pytest
from pyvboxmanage import __author__
from pyvboxmanage import __version__
from pyvboxmanage import __title__


def test_author_exist():
    assert __author__ is not None


def test_version_exist():
    assert __version__ is not None


def test_title_exist():
    assert __title__ is not None
