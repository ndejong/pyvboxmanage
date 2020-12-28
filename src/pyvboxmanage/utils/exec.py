
import subprocess
from pyvboxmanage.exceptions.PyVBoxManageException import PyVBoxManageException


def exec_command(command_line, timeout=10):
    try:
        sp = subprocess.run(command_line, shell=True, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        raise PyVBoxManageException(e)

    return sp.stdout, sp.stderr, sp.returncode
