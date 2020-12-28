
import platform
from pyvboxmanage.utils.exec_command import exec_command
from pyvboxmanage.exceptions.PyVBoxManageException import PyVBoxManageException


def vboxmanage_binary():

    if 'Windows' in platform.system():
        binfile = 'VBoxManage'
    else:
        binfile = 'vboxmanage'

    stdout, stderr, returncode = exec_command(binfile)

    if int(returncode) > 0:
        raise PyVBoxManageException('Unable to locate {} in system PATH'.format(binfile))

    if stderr:
        raise PyVBoxManageException('Unexpected STDERR output from {}'.format(binfile), stderr)

    return binfile
