
import os
import pytest
from click.testing import CliRunner
from pyvboxmanage.cli import click
from pyvboxmanage import __version__


def test_pyvboxmanage_version():
    runner = CliRunner()
    result = runner.invoke(click.pyvboxmanage, '--version')
    assert __version__ in result.output
    assert result.exit_code == 0


def test_pyvboxmanage_help():
    runner = CliRunner()
    result = runner.invoke(click.pyvboxmanage, '--help')
    assert 'Usage:' in result.output
    assert 'Options:' in result.output
    assert result.exit_code == 0


def test_pyvboxmanage_dryrun():
    runner = CliRunner()
    config_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdryrun_configuration.yml')

    if not os.path.isfile(config_filename):
        raise Exception('Expected configuration file missing', config_filename)

    result = runner.invoke(click.pyvboxmanage, ['--dry-run', config_filename])
    assert 'Successfully executed command line "vboxmanage showvminfo Ubuntu-20.04-pipeline"' in result.output
    assert 'Successfully executed command line "vboxmanage clonevm Ubuntu-20.04-master' in result.output
    assert 'Successfully executed command line "vboxmanage modifyvm Ubuntu-20.04-pipeline --nic1' in result.output
    assert 'Successfully executed command line "vboxmanage startvm Ubuntu-20.04-pipeline --type' in result.output
    assert result.exit_code == 0
