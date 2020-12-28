
import pytest
from click.testing import CliRunner
from pyvboxmanage.cli import click
from pyvboxmanage import __version__


def test_dmm_version():
    runner = CliRunner()
    result = runner.invoke(click.pyvboxmanage, '--version')
    assert __version__ in result.output
    assert result.exit_code == 0


def test_dmm_help():
    runner = CliRunner()
    result = runner.invoke(click.pyvboxmanage, '--help')
    assert 'Usage:' in result.output
    assert 'Options:' in result.output
    assert result.exit_code == 0

