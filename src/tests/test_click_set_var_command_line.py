
import os
import pytest
from click.testing import CliRunner
from pyvboxmanage.cli import click


# NB: these tests work in isolation, however when they are run together with other runner.invoke() that use `args`
#     then the result.stdout returns empty - it is not obvious how to resolve this even using a manual `del` on
#     variable names in other tests does not resolve.


# def test_pyvboxmanage_dryrun_test01_set_var_cli():
#     runner = CliRunner()
#     config01_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test01config.yml')
#
#     result = runner.invoke(click.pyvboxmanage, args='--dry-run --setting source_vmname=FOOBAR "{}"'.
#                            format(config01_filename) )
#     assert result.exit_code == 0
#     assert 'Successfully executed command line "vboxmanage clonevm FOOBAR --basefolder' in result.stdout


# def test_pyvboxmanage_dryrun_test02_set_var_cli():
#     runner = CliRunner()
#     config01_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test01config.yml')
#
#     result = runner.invoke(click.pyvboxmanage, args='--dry-run --setting source_vmname=FOOBAR "{}"'.
#                            format(config01_filename) )
#     assert result.exit_code == 0
#     assert 'Successfully executed command line "vboxmanage clonevm FOOBAR --basefolder' in result.stdout


# def test_pyvboxmanage_dryrun_test03_set_var_cli():
#
#     runner = CliRunner()
#     config_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test03config.yml')
#
#     result = runner.invoke(click.pyvboxmanage, args='--dry-run --setting unset_variable01=replacement_sourcevm01 "{}"'.
#                            format(config_filename) )
#     assert result.exit_code == 0
#     assert 'Successfully executed command line "vboxmanage showvminfo replacement_sourcevm01"' in result.stdout
