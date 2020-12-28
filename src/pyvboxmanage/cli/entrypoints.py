
from pyvboxmanage import __title__ as NAME
from pyvboxmanage import __version__ as VERSION
from pyvboxmanage.cli import click
from pyvboxmanage.exceptions.PyVBoxManageException import PyVBoxManageException


def pyvboxmanage():

    try:
        click.pyvboxmanage()
    except PyVBoxManageException as e:
        print('')
        print('{} v{}'.format(NAME, VERSION))
        print('ERROR: ', end='')
        for err in iter(e.args):
            print(err)
        print('')
        exit(1)

