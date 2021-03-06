""" Module for cmake generator and executables build process.

    In order to create final collector executable, some mid-step stages are required. Notably,
    the configuration executable is required, as it provides useful data for creation of time
    efficient collector executable.

    Configuration executable is simply a executable built from the workload source and header files,
    with no additional compiler settings or libraries. It is used for function symbols extraction
    and their filtering in order to create symbols exclude list (see symbols.py).

    Collector executable is the final executable used to collect the profiling data. Additional
    compiler settings are configured, such as -finstrument-functions flag and exclude list.
    The C++ profiling library is dynamically linked to this executable to allow the capture,
    processing and storage of records.

    Thoughts: - not only source files but also libraries - requires also heavy extension of
                profiling library
              - add global error log
              - enable the users to also specify their own compiler flags and settings?
"""

import os
import subprocess

# Cmake constants that may be changed
CMAKE_VERSION = '2.8'
CMAKE_BIN_TARGET = '/bin'
CMAKE_CONFIG_TARGET = 'WorkloadCfg'
CMAKE_COLLECT_TARGET = 'Workload'
CMAKE_PROF_LIB_NAME = 'profile'
CMAKE_PROF_LIB_PATH = '${CMAKE_SOURCE_DIR}'
CMAKE_API_LIB_NAME = 'profapi'
CMAKE_API_LIB_PATH = '${CMAKE_SOURCE_DIR}'


def create_config_cmake(target_path, file_paths):
    """ Creates the cmake file for workload configuration executable

    Arguments:
        target_path(str): cmake target directory path
        file_paths(list): paths to the workload source and header files

    Returns:
        str: absolute path to the created cmake file

    Raises:
        OSError: if the cmake file creation or opening failed
        ValueError: if the cmake file is unexpectedly closed
    """
    # Open the cmake file and get the path
    cmake_path = _cmake_construct_file_path(target_path)
    with open(cmake_path, 'w') as cmake_handle:
        # Write the basic cmake configuration
        _cmake_init(cmake_handle)

        # Write the build configuration
        _cmake_build_data(cmake_handle, CMAKE_CONFIG_TARGET, file_paths)

        # Add the api library
        library_vars = []
        library_vars = _cmake_find_library(cmake_handle, CMAKE_API_LIB_NAME, CMAKE_API_LIB_PATH,
                                           library_vars)

        # Link with the api library
        _cmake_link_libraries(cmake_handle, library_vars, CMAKE_CONFIG_TARGET)

    return cmake_path


def create_collector_cmake(target_path, file_paths, exclude_list):
    """ Creates the cmake file for workload collector executable

    Arguments:
        target_path(str): cmake target directory path
        file_paths(list): paths to the workload source and header files
        exclude_list(list): function names that should be statically excluded

    Returns:
        str: absolute path to the created cmake file

    Raises:
        OSError: if the cmake file creation or opening failed
        ValueError: if the cmake file is unexpectedly closed
    """
    # Open the cmake file and get the path
    cmake_path = _cmake_construct_file_path(target_path)
    with open(cmake_path, 'w') as cmake_handle:
        # Write the basic cmake configuration
        _cmake_init(cmake_handle)
        # Extend the configuration for profiling
        _cmake_add_profile_instructions(cmake_handle, exclude_list)

        # Write the build configuration
        _cmake_build_data(cmake_handle, CMAKE_COLLECT_TARGET, file_paths)

        # Add the profiling and api library
        library_vars = []
        library_vars = _cmake_find_library(cmake_handle, CMAKE_API_LIB_NAME, CMAKE_API_LIB_PATH,
                                           library_vars)
        library_vars = _cmake_find_library(cmake_handle, CMAKE_PROF_LIB_NAME, CMAKE_PROF_LIB_PATH,
                                           library_vars)

        # Link with the profiling and api library
        _cmake_link_libraries(cmake_handle, library_vars, CMAKE_COLLECT_TARGET)

    return cmake_path


def build_executable(cmake_path, target_name):
    """ Invokes call sequence of cmake -> make to build the executable
       Warning - time expensive function due to cmake generator and g++ compilation

    Arguments:
        cmake_path(str): path to the CMakeLists.txt file
        target_name(str): the target executable name (CMAKE_CONFIG_TARGET or CMAKE_COLLECT_TARGET,
                          depending on the generated cmake type)

    Returns:
        str: absolute path to the built executable

    Raises:
        subprocess.CalledProcessError: if the build commands cannot be executed
    """
    # Get the cmake directory
    cmake_dir = str(cmake_path).replace('/CMakeLists.txt', '')

    # Try to execute the build commands
    subprocess.check_call(('cmake', '.'), stdout=subprocess.DEVNULL, cwd=cmake_dir)
    subprocess.check_call('make', stdout=subprocess.DEVNULL, cwd=cmake_dir)

    # Get the executable path
    exec_path = cmake_dir + CMAKE_BIN_TARGET + '/' + target_name
    return os.path.realpath(exec_path)


def _cmake_construct_file_path(target_path):
    """ Constructs the cmake file absolute path

    Arguments:
        target_path(str): cmake target directory path

    Returns:
        str: the constructed cmake file path
    """
    # Extend the path accordingly
    if not target_path.endswith('/'):
        target_path += '/'
    target_path += 'CMakeLists.txt'
    return os.path.realpath(target_path)


def _cmake_init(cmake_file):
    """ Writes init configuration to the cmake file

    Arguments:
        cmake_file(file): file handle to the opened cmake file

    Raises:
        ValueError: if the cmake file is unexpectedly closed
    """
    # Sets the cmake version, paths and compiler config
    cmake_file.write('cmake_minimum_required(VERSION {0})\n\n'
                     '# set the paths\n'
                     'set(CMAKE_BINARY_DIR ${{CMAKE_SOURCE_DIR}}{1})\n'
                     'set(EXECUTABLE_OUTPUT_PATH ${{CMAKE_BINARY_DIR}})\n\n'
                     '# set the compiler\n'
                     'set(CMAKE_CXX_COMPILER "g++")\n'
                     'set(CMAKE_CXX_FLAGS "${{CMAKE_CXX_FLAGS}} -std=c++11 -g")\n\n'
                     .format(CMAKE_VERSION, CMAKE_BIN_TARGET))


def _cmake_add_profile_instructions(cmake_file, exclude_list):
    """ Extends the compiler configuration with instrumentation options

    Arguments:
        cmake_file(file): file handle to the opened cmake file
        exclude_list(list): names of statically excluded functions from profiling

    Raises:
        ValueError: if the cmake file is unexpectedly closed
    """
    # Enable the instrumentation
    cmake_file.write('# extend the compiler flags for profiling\n'
                     'set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -finstrument-functions')
    # Set the excluded functions
    if exclude_list:
        # Create 'sym,sym,sym...' string list from excluded names
        exclude_string = ','.join(exclude_list)
        cmake_file.write(' -finstrument-functions-exclude-function-list={0}")\n\n'
                         .format(exclude_string))
    else:
        cmake_file.write('\n\n')


def _cmake_build_data(cmake_file, target_name, source_files):
    """ Writes build configuration to the cmake file

    Arguments:
        cmake_file(file): file handle to the opened cmake file
        target_name(str): build target name
        source_files(list): paths to the workload source and header files

    Raises:
        ValueError: if the cmake file is unexpectedly closed
    """
    # Set the source variable
    cmake_file.write('# set the sources\n'
                     'set(SOURCE_FILES\n\t')
    # Supply all the workload source files
    sources = '\n\t'.join(str(source) for source in source_files)
    sources += '\n)\n\n'
    cmake_file.write(sources)

    # Specify the executable
    cmake_file.write('# create the executable\n'
                     'add_executable({0} ${{SOURCE_FILES}})\n'
                     .format(target_name))


def _cmake_link_libraries(cmake_file, library_vars, target_name):
    """ Links the profiling library with the collection executable

    Arguments:
        cmake_file(file): file handle to the opened cmake file
        library_vars(list): list of libraries to be linked
        target_name(str): build target to be linked with

    Raises:
        ValueError: if the cmake file is unexpectedly closed
    """
    # Create the string list of all libraries
    libraries = ' '.join('${{{0}}}'.format(lib) for lib in library_vars)
    # Create the target
    cmake_file.write('\n# Link the libraries to the target\n'
                     'target_link_libraries({0} {1})\n'
                     .format(target_name, libraries))


def _cmake_find_library(cmake_file, lib_name, lib_path, library_vars):
    """ Links the profiling library with the collection executable

    Arguments:
        cmake_file(file): file handle to the opened cmake file
        lib_name(str): the name of the library to search for
        lib_path(str): the path to the library to search for
        library_vars(list): list of already found libraries

    Returns:
        list: the updated library vars list

    Raises:
        ValueError: if the cmake file is unexpectedly closed
    """
    # Create the library variable name
    library_var = 'PROFILE_LIB' + str(len(library_vars))
    # Create instruction to find the library
    cmake_file.write('\n# Find the library\n'
                     'find_library({0} {1} PATHS "{2}")\n'
                     .format(library_var, lib_name, lib_path))
    library_vars.append(library_var)
    return library_vars
