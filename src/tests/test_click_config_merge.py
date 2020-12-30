
import os
import pytest
from click.testing import CliRunner
from pyvboxmanage.cli import click


def test_pyvboxmanage_dryrun_test01_merge_test02():
    runner = CliRunner()
    config01_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test01config.yml')
    config02_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test02config.yml')

    result = runner.invoke(click.pyvboxmanage, ['--dry-run', config01_filename, config02_filename])
    assert result.exit_code == 0
    assert 'Successfully executed command line "vboxmanage showvminfo test02targetvname"' in result.output
    assert 'Successfully executed command line "vboxmanage unregistervm test02targetvname --delete"' in result.output
    assert 'Successfully executed command line "vboxmanage clonevm test02sourcevname --basefolder "/test02targetbasefolder" --groups "/test02targetgroups" --mode "machine" --name "test02targetvname" --register"' in result.output
    assert 'Successfully executed command line "vboxmanage modifyvm test02targetvname --bridgeadapter1 "test02targetbridgeadapter" --bridgeadapter2 "test02targetbridgeadapter" --bridgeadapter3 "test02targetbridgeadapter" --bridgeadapter4 "test02targetbridgeadapter" --cableconnected1 "on" --cableconnected2 "on" --cableconnected3 "on" --cableconnected4 "on" --macaddress1 "08002722E901" --macaddress2 "08002722E902" --macaddress3 "08002722E903" --macaddress4 "08002722E904" --nic1 "bridged" --nic2 "bridged" --nic3 "bridged" --nic4 "bridged" --nictype1 "82543GC" --nictype2 "82543GC" --nictype3 "82543GC" --nictype4 "82543GC""' in result.output
