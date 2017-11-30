"""Basic tests for utility package and sanity checks"""

import pkgutil

import perun.utils as utils
import perun.vcs as vcs
import perun.collect as collect
import perun.postprocess as postprocess
import perun.logic.config as config
import perun.logic.commands as commands
import perun.view as view

__author__ = 'Tomas Fiedor'


def assert_all_registered_modules(package_name, package, must_have_function_names):
    """Asserts that for given package all of its modules are properly registered in Perun

    Moreover checks that all of the must have functions are implemented as well.

    Arguments:
        package_name(str): name of the package we are checking all the modules
        package(module): checked package
        must_have_function_names(list): list of functions that the module from package has to have
          registered
    """
    registered_modules = utils.get_supported_module_names(package_name)
    for (_, module_name, _) in pkgutil.iter_modules(package.__path__, package.__name__ + '.'):
        module = utils.get_module(module_name)
        for must_have_function_name in must_have_function_names:
            assert hasattr(module, must_have_function_name) and "Missing {} in module {}".format(
                must_have_function_name, module_name
            )

        # Each module has to be registered in get_supported_module_names
        unit_name = module_name.split('.')[-1]
        assert unit_name in registered_modules and "{} was not registered properly".format(
            module_name
        )


def assert_all_registered_cli_units(package_name, package, must_have_function_names):
    """Asserts that for given package all of its modules are properly registered in Perun

    Moreover checks that it has the CLI interface function in order to be called through click,
    and that certain functions are implemented as well (namely collect/postprocess) in order
    to automate the process of profile generation and postprocessing.

    Arguments:
        package_name(str): name of the package we are checking all the modules
        package(module): checked package (one of collect, postprocess, view)
        must_have_function_names(list): list of functions that the module from package has to have
          registered
    """
    registered_modules = utils.get_supported_module_names(package_name)
    for (_, module_name, _) in pkgutil.iter_modules(package.__path__, package.__name__ + '.'):
        # Each module has to have run.py module
        module = utils.get_module(module_name)
        assert hasattr(module, 'run') and "Missing module run.py in the '{}' module".format(
            package_name
        )
        run_module = utils.get_module(".".join([module_name, "run"]))
        for must_have_function_name in must_have_function_names:
            assert not must_have_function_name or hasattr(run_module, must_have_function_name) and \
                "run.py is missing '{}' function".format(must_have_function_name)

        # Each module has to have CLI interface function of the same name
        unit_name = module_name.split('.')[-1]
        assert hasattr(run_module, unit_name) and "{} is missing CLI function point".format(
            unit_name
        )

        # Each module has to be registered in get_supported_module_names
        assert unit_name in registered_modules and "{} was not registered properly".format(
            module_name
        )


def test_get_supported_modules():
    """Test whether all currently compatible modules are registered in the function

    This serves and sanity check for new modules that could be added in future. Namely it checks
    all of the collectors, postprocessors and view that they can be used from the CLI and also
    tests that VCS modules can be used as a backend for perun.

    Expecting no errors and every supported module registered in the function
    """
    # Check that all of the internal modules (vcs) are properly registered and has interface for
    # concrete functions.
    assert_all_registered_modules('vcs', vcs, [
        '_init', '_get_minor_head', '_walk_minor_versions', '_walk_major_versions',
        '_get_minor_version_info', '_get_head_major_version', '_check_minor_version_validity',
        '_massage_parameter'
    ])

    # Check that all of the CLI units (collectors, postprocessors and visualizations) are properly
    # registered.
    assert_all_registered_cli_units('collect', collect, ['collect'])
    assert_all_registered_cli_units('postprocess', postprocess, ['postprocess'])
    assert_all_registered_cli_units('view', view, [])


def test_paging_and_config(monkeypatch, capsys):
    """Helper function for testing various configs of paging through turn_off_paging_wrt_config"""
    cfg = config.Config('shared', '', {'general': {'paging': 'always'}})
    monkeypatch.setattr("perun.logic.config.shared", lambda: cfg)
    assert commands.turn_off_paging_wrt_config('status')
    assert commands.turn_off_paging_wrt_config('log')

    cfg = config.Config('shared', '', {'general': {'paging': 'only-log'}})
    monkeypatch.setattr("perun.logic.config.shared", lambda: cfg)
    assert not commands.turn_off_paging_wrt_config('status')
    assert commands.turn_off_paging_wrt_config('log')

    cfg = config.Config('shared', '', {'general': {'paging': 'only-status'}})
    monkeypatch.setattr("perun.logic.config.shared", lambda: cfg)
    assert commands.turn_off_paging_wrt_config('status')
    assert not commands.turn_off_paging_wrt_config('log')

    cfg = config.Config('shared', '', {'general': {'paging': 'never'}})
    monkeypatch.setattr("perun.logic.config.shared", lambda: cfg)
    assert not commands.turn_off_paging_wrt_config('status')
    assert not commands.turn_off_paging_wrt_config('log')

    cfg = config.Config('shared', '', {})
    monkeypatch.setattr("perun.logic.config.shared", lambda: cfg)
    assert commands.turn_off_paging_wrt_config('status')
    assert commands.turn_off_paging_wrt_config('log')
    out, _ = capsys.readouterr()
    assert 'warn' in out and 'missing ``general.paging``' in out
