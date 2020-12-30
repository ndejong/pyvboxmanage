
import sys
import logging
from pyvboxmanage import __exec_timeout_default__ as EXEC_TIMEOUT_DEFAULT
from pyvboxmanage.exceptions.PyVBoxManageException import PyVBoxManageException
from pyvboxmanage.utils.config import load_configuration_files
from pyvboxmanage.utils.bin_file import vboxmanage_binary
from pyvboxmanage.utils.exec_command import exec_command


logger = logging.getLogger(__name__)


class PyVBoxManage:

    config = None
    dry_run = None
    bin_file = None

    def __init__(self, configuration_files, dry_run=False):
        self.dry_run = dry_run
        self.config = load_configuration_files(configuration_files)
        self.bin_file = vboxmanage_binary(dry_run=dry_run)

    def main(self):
        for item in self.config:
            stdout, stderr, returncode = self.config_item_runner(item)
            self.config_item_outputs(stdout, item['outputs'])
            if self.config_item_triggers(stdout, stderr, returncode, item['triggers']) is False:
                logger.info('Stopping "{}" because trigger condition does not match'.format(item['command']))
                return

    def config_item_triggers(self, stdout, stderr, returncode, setup):
        if setup is None:
            setup = []
        elif type(setup) is not list:
            raise PyVBoxManageException('Unexpected triggers config', setup)

        for trigger_setup in setup:
            if trigger_setup['source'] == 'stdout':
                content = stdout
            elif trigger_setup['source'] == 'stderr':
                content = stderr
            elif trigger_setup['source'] == 'returncode':
                content = returncode
            else:
                raise PyVBoxManageException('Unexpected trigger source condition')

            if trigger_setup['string'] in content.decode('utf8'):
                logger.debug('Trigger string "{}" is present'.format(trigger_setup['string']))
                if trigger_setup['condition'] != 'present':
                    logger.debug('Trigger string does not match expected "present" condition state')
                    return False
            else:
                logger.debug('Trigger string "{}" is not present'.format(trigger_setup['string']))
                if trigger_setup['condition'] != 'not_present':
                    logger.debug('Trigger string does not match expected "not_present" condition state')
                    return False
        return True

    def config_item_outputs(self, stdout, setup):
        if setup is None:
            setup = []
        elif type(setup) is not list:
            raise PyVBoxManageException('Unexpected outputs config', setup)

        for output_target in setup:
            if output_target.lower() in ['/dev/null', 'devnull', 'null']:
                continue
            elif output_target.lower() in ['stdout']:
                print(stdout.decode('utf8'), file=sys.stdout)
            elif output_target.lower() in ['stderr']:
                print(stdout.decode('utf8'), file=sys.stderr)
            else:
                try:
                    with open(output_target, mode='wb') as f:
                        f.write(stdout)
                except Exception as e:
                    raise PyVBoxManageException('Unable to write to {}'.format(output_target), e)
                logger.debug('Output written to {}'.format(output_target))

    def config_item_runner(self, item):
        command_line = self.render_command(item)
        logger.debug('Rendered command line: {}'.format(command_line))
        if item['timeout']:
            exec_timeout = item['timeout']
        else:
            exec_timeout = EXEC_TIMEOUT_DEFAULT
        logger.debug('Command line exec timeout {}'.format(exec_timeout))

        if self.dry_run is True:
            stdout, stderr, returncode = b'', b'', 0
        else:
            stdout, stderr, returncode = exec_command(command_line, timeout=exec_timeout)

        if item['returncodes']:
            if returncode in item['returncodes']:
                if returncode > 0:
                    logger.warning('Command line "{}" returncode "{}" configured as okay'.format(command_line, returncode))
                else:
                    logger.info('Successfully executed command line "{}"'.format(command_line))
                return stdout, stderr, returncode
            else:
                raise PyVBoxManageException('Unexpected "{}" returncode from command execution'.format(returncode), command_line)

        if returncode > 0:
            raise PyVBoxManageException('Unexpected response from {}'.format(command_line), stderr)

        logger.info('Successfully executed command line "{}"'.format(command_line))
        return stdout, stderr, returncode

    def render_command(self, command):
        command_line = '{} {}'.format(self.bin_file, command['command'])

        if type(command['arguments']) is list:
            for item_argument in command['arguments']:
                if ' ' in item_argument:
                    command_line += ' "{}"'.format(item_argument)
                else:
                    command_line += ' {}'.format(item_argument)

        if type(command['options']) is dict:
            for option_key, option_value in command['options'].items():
                if type(option_value) is bool and option_value is True:
                    command_line += ' --{}'.format(option_key)
                else:
                    command_line += ' --{} "{}"'.format(option_key, option_value)

        return command_line
