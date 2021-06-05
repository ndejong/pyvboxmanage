
import os
import re
import yaml
import logging
from pyvboxmanage.utils.merge import merge
from pyvboxmanage.exceptions.PyVBoxManageException import PyVBoxManageException

from pyvboxmanage import __config_import_recursion_limit__
from pyvboxmanage import __variable_tag_open__
from pyvboxmanage import __variable_tag_close__


logger = logging.getLogger(__name__)


def load_configuration_files(configuration_files, variable_overrides=None):

    config = {}
    for configuration_file in configuration_files:
        config = merge(config, load_configuration_file(configuration_file))

    config = replace_config_vars(config, variable_overrides)
    return normalize_config(config)


def load_configuration_file(configuration_file, __level=0):

    if not os.path.exists(configuration_file):
        raise PyVBoxManageException('Configuration file not found', configuration_file)

    if __level >= __config_import_recursion_limit__:
        raise PyVBoxManageException('Configuration recursion limit reached, likely circular import references', __level)

    with open(configuration_file) as f:
        content = f.read()

    config = parse_yaml_content(content)
    logger.debug('Loaded configuration file {}'.format(configuration_file))

    if 'imports' in config.keys() and type(config['imports']) is list:
        for configuration_import_file in config['imports']:
            if not os.path.exists(configuration_import_file):
                configuration_import_file = os.path.join(os.path.dirname(configuration_file), configuration_import_file)
            config = merge(config, load_configuration_file(configuration_import_file, __level+1))

    return config


def replace_config_vars(config, variable_overrides=None):

    if variable_overrides is None:
        variable_overrides = {}

    content = yaml.dump(config)

    if 'vars' in config.keys():
        if type(config['vars']) is not dict:
            raise PyVBoxManageException('Unexpected "vars" configuration', config['vars'])
        variables = merge(config['vars'], variable_overrides)
    else:
        variables = variable_overrides

    for key, value in variables.items():
        expression = "{}\s*{}\s*{}".\
            format(re.escape(__variable_tag_open__), re.escape(key), re.escape(__variable_tag_close__))
        content = re.sub(expression, str(value), content)

    expression = "{}.+{}".format(re.escape(__variable_tag_open__), re.escape(__variable_tag_close__))
    matches = re.findall(expression, content, re.MULTILINE)
    if matches:
        for m in matches:
            logger.warning('Suspected unset variable: {}'.format(m))

    return parse_yaml_content(content)


def parse_yaml_content(content):
    try:
        config = yaml.safe_load(content)
    except yaml.parser.ParserError as e:
        raise PyVBoxManageException('Configuration file format error', e)

    if type(config) is not dict:
        raise PyVBoxManageException('Unexpected configuration file format')

    return config


def normalize_config(config):

    if 'pyvboxmanage' not in config.keys():
        raise PyVBoxManageException('Unexpected configuration file format, missing "pyvboxmanage" root')

    if type(config['pyvboxmanage']) is not list:
        raise PyVBoxManageException('Unexpected configuration file format, "pyvboxmanage" content is not a list')

    items = []

    for item in config['pyvboxmanage']:
        if type(item) is not dict:
            raise PyVBoxManageException('Unexpected configuration file format, item is not a dict', item)

        command = options = arguments = outputs = triggers = returncodes = timeout = None

        for key, value in item.items():

            # arguments
            if key.lower() in ['arg', 'argument', 'args', 'arguments']:
                arguments = __normalize_arguments(key, value)

            # options
            elif key.lower() in ['opts', 'options']:
                options = __normalize_options(key, value)

            # outputs
            elif key.lower() in ['out', 'output', 'outputs']:
                outputs = __normalize_outputs(key, value)

            # returncodes
            elif key.lower() in ['returncode', 'return_code', 'returncodes', 'return_codes']:
                returncodes = __normalize_returncodes(key, value)

            # triggers
            elif key.lower() in ['trigger', 'triggers']:
                triggers = __normalize_triggers(key, value)

            # timeout
            elif key.lower() in ['timeout']:
                timeout = __normalize_timeout(key, value)

            # command
            else:
                if command is not None:
                    raise PyVBoxManageException('Unexpected configuration attribute "{}" in "{}"'.format(key, command))
                command = key

        items.append({
            'command': command,
            'options': options,
            'arguments': arguments,
            'outputs': outputs,
            'triggers': triggers,
            'returncodes': returncodes,
            'timeout': timeout
        })

    return items


def __normalize_arguments(key, value):
    if type(value) is str:
        return [value]
    return value


def __normalize_options(key, value):
    if type(value) is not dict:
        raise PyVBoxManageException('Unexpected options configuration {}'.format(key), value)
    return value


def __normalize_outputs(key, value):
    if type(value) is str:
        return [value]
    return value


def __normalize_returncodes(key, value):
    if type(value) in [str, int]:
        returncodes = [value]
    elif type(value) is list:
        returncodes = value
    else:
        raise PyVBoxManageException('Unexpected returncodes type', value)

    for returncode_index, returncode in enumerate(returncodes):
        if type(returncode) is str:
            try:
                returncodes[returncode_index] = int(returncode)
            except ValueError as e:
                raise PyVBoxManageException(e, value)
        elif type(returncode) is not int:
            raise PyVBoxManageException('Unexpected returncodes value type', value)

    return returncodes


def __normalize_triggers(key, value):
    if type(value) is dict:
        triggers = [value]
    elif type(value) is list:
        triggers = value
    else:
        raise PyVBoxManageException('Unexpected triggers configuration {}'.format(key), value)

    for trigger_index, trigger in enumerate(triggers):
        # source
        if 'source' not in trigger.keys():
            triggers[trigger_index]['source'] = 'stdout'
        if trigger['source'].lower() not in ['stdout', 'stderr', 'returncode']:
            raise PyVBoxManageException('Unexpected trigger source supplied', trigger)
        triggers[trigger_index]['source'] = triggers[trigger_index]['source'].lower()

        # string
        if 'string' not in trigger.keys():
            raise PyVBoxManageException('Required "string" trigger setting missing', trigger)

        # condition
        if 'condition' not in trigger.keys():
            triggers[trigger_index]['condition'] = 'present'
        elif trigger['condition'].lower() in ['present']:
            triggers[trigger_index]['condition'] = 'present'
        elif trigger['condition'].lower() in ['not present', 'not_present', 'notpresent', '!present', '! present']:
            triggers[trigger_index]['condition'] = 'not_present'
        else:
            raise PyVBoxManageException('Unexpected trigger condition supplied', trigger)

    return triggers


def __normalize_timeout(key, value):
    if type(value) is str:
        try:
            timeout = int(value)
        except ValueError as e:
            raise PyVBoxManageException(e, value)
    elif type(value) is int:
        timeout = value
    else:
        raise PyVBoxManageException('Unexpected triggers configuration {}'.format(key), value)

    return timeout
