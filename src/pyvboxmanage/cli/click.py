
import click

from pyvboxmanage import __title__ as NAME
from pyvboxmanage import __version__ as VERSION
from pyvboxmanage.utils import logger
from pyvboxmanage.PyVBoxManage import PyVBoxManage


@click.command(no_args_is_help=True)
@click.argument('configuration_file', required=True)
@click.option('-v', '--verbose', is_flag=True, help='Verbose logging messages (debug level).')
@click.option('-q', '--quiet', is_flag=True, help='Quiet mode, with priority over --verbose')
@click.option('-d', '--dry-run', is_flag=True, help='Dry run mode, output the commands that would execute only.')
@click.version_option(VERSION)
def pyvboxmanage(configuration_file, verbose, quiet, dry_run):
    """
    PyVBoxManage is a wrapper tool around VBoxManage that facilitates the orchestration of VBoxManage commands from a
    simple YAML configuration file that matches the input opts/args for VBoxManage.  This makes it possible to
    implement common sequences of VBoxManage commands such as spinning up a new dev/test instance with different
    hardware just by using a single command line with a configuration file.

    Variables, output redirection, exit-triggers and returncode-exceptions are available to make flexible setups.

    Documentation available https://pyvboxmanage.readthedocs.io
    """

    ctx = click.get_current_context()
    ctx.ensure_object(dict)

    if quiet:
        logger.init(name=NAME, level='critical')
    elif verbose:
        logger.init(name=NAME, level='debug')
    else:
        logger.init(name=NAME, level='info')

    logger.debug('{} v{}'.format(NAME, VERSION))

    PyVBoxManage(configuration_file=configuration_file, dry_run=dry_run).main()
