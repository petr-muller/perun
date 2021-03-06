""" Module for internal collector configuration file generator.

    The complexity collector library needs some specific configuration settings in order to work
    properly and efficiently. The library uses the circ.conf file to pass the configuration data
    at collector's runtime. The file format is specified in the circ.rst documentation

    This module handles all the necessary operations to create correct circ.conf file.

"""


import os
import json
import perun.collect.complexity.symbols as symbols

# Default internal parameters
DEFAULT_DATA_FILENAME = 'trace.log'
DEFAULT_STORAGE_SIZE = 20000
DEFAULT_DIRECT_OUTPUT = False


def create_runtime_config(executable_path, runtime_filter, include_list, configuration):
    """ Creates the config.conf configuration

    Arguments:
        executable_path(str): path to the executable which will use the configuration
        runtime_filter(list): function mangled names, which should be filtered at runtime
        include_list(list): list of function symbols(rule_key tuple) to be profiled
        configuration(dict): dictionary with configuration data

    Raises:
        OSError: if the config file creation or opening failed
        ValueError: if the config file is unexpectedly closed
    """
    # Open the file
    config_path = _config_construct_file_path(executable_path)
    with open(config_path, 'w') as config_handle:
        # Write the configuration settings
        _config_write_config(config_handle, executable_path, runtime_filter, include_list,
                             configuration)


def _config_construct_file_path(executable_path):
    """ Constructs the file path for the config.conf file

    Arguments:
        executable_path(str): path to the executable which will use the configuration

    Returns:
        str: the configuration file constructed path
    """
    # Extract the executable directory for config target
    path = os.path.realpath(executable_path)
    pos = path.rfind('/')
    return path[:pos + 1] + 'circ.conf'


def _config_symbols_to_addresses(executable_path, runtime_filter, sample_map):
    """ Translates the identifiers in filter and sample configuration to their
        symbol table addresses

    Arguments:
        executable_path(str): path to the executable which will use the configuration
        runtime_filter(list): function mangled names, which should be filtered at runtime
        sample_map(dict): dict of sample configuration as 'mangled name: sample ratio'

    Returns:
        tuple: list of function addresses to be filtered at runtime
               dict of function addresses and sampling values
    """
    # Get the symbol:address
    symbol_map = symbols.extract_symbol_map(executable_path)
    # Translate the filter identifiers
    final_filter = []
    for func in runtime_filter:
        if func in symbol_map.keys():
            final_filter.append(int(symbol_map[func], 16))
    # Translate the sample identifiers
    final_sample = dict()
    for item in sample_map:
        if item in symbol_map:
            final_sample[int(symbol_map[item], 16)] = sample_map[item]
    return final_filter, final_sample


def _config_write_config(config_handle, executable_path, runtime_filter, include_list,
                         job_settings):
    """ Writes the configuration stored in the config dictionary into the file

    Arguments:
        config_handle(file): file handle to the opened config file
        executable_path(str): path to the executable which will use the configuration
        runtime_filter(list): addresses of functions to filter at runtime
        include_list(list): list of function symbols(rule_key tuple) to be profiled
        job_settings(dict): dictionary with collect job configuration data

    Raises:
        ValueError: if the config file is unexpectedly closed
        TypeError: if the json serializing fails
    """
    sample_map = dict()
    # Create the translation table for identifiers
    if 'sampling' in job_settings:
        sample_map = _config_create_sample(include_list, job_settings['sampling'])
    filter_list, sample_dict = _config_symbols_to_addresses(executable_path, runtime_filter,
                                                            sample_map)

    # Create the internal configuration
    internal_conf = {
        'internal_data_filename': job_settings.get('internal_data_filename', DEFAULT_DATA_FILENAME),
        'internal_storage_size': job_settings.get('internal_storage_size', DEFAULT_STORAGE_SIZE),
        'internal_direct_output': job_settings.get('internal_direct_output', DEFAULT_DIRECT_OUTPUT),
    }
    # Append the runtime filter configuration
    if filter_list:
        internal_conf['runtime_filter'] = filter_list
    # Append the sampling configuration
    if sample_dict:
        internal_conf['sampling'] = []
        for sample_rule in sample_dict:
            internal_conf['sampling'].append(
                {'func': sample_rule, 'sample': sample_dict[sample_rule]})

    # Serializes the configuration dictionary to the proper circ format
    config_handle.write('CIRC = {0}'.format(json.dumps(internal_conf, sort_keys=True, indent=2)))


def _config_create_sample(include_list, sample_list):
    """ Creates the sample map as 'sample func mangled name: sample ratio' from the
        include list and sample list

    Arguments:
        include_list(list): list of rule_keys tuples
        sample_list(list): list of sampling rules (dictionaries)

    Returns:
        dict: the created sample map
    """
    sample_map = dict()
    # Try to pair the sample configuration and include list to create sample map
    # 'mangled name: sample value'
    for sample in sample_list:
        # Unify the sampling function name to match the names in include list
        sample_name = symbols.unify_sample_func(sample['func'])
        for include_func in include_list:
            if include_func.rule == sample_name:
                # Sampling name and include list name match
                sample_map[include_func.mangled_name] = sample['sample']
                break
    return sample_map
