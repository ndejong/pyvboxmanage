
import logging
import platform
from pyvboxmanage.utils.exec_command import exec_command
from pyvboxmanage.exceptions.PyVBoxManageException import PyVBoxManageException


logger = logging.getLogger(__name__)


def vboxmanage_binary(dry_run=False):

    if 'Windows' in platform.system():
        bin_file = 'VBoxManage'
    else:
        bin_file = 'vboxmanage'

    if dry_run:
        logger.debug('Dry mode VBoxManage binary set to {}'.format(bin_file))
        return bin_file

    stdout, stderr, returncode = exec_command(bin_file)

    if int(returncode) > 0:
        raise PyVBoxManageException('Unable to locate {} in system PATH'.format(bin_file))

    if stderr:
        raise PyVBoxManageException('Unexpected STDERR output from {}'.format(bin_file), stderr)

    logger.debug('VBoxManage binary available as {}'.format(bin_file))
    return bin_file
