""" Basic tests for scatter plot visualization """

import os

from click.testing import CliRunner

import perun.cli as cli
import perun.view.scatter.factory as scatter

__author__ = 'Jiri Pavela'


def test_scatter_plot_models(postprocess_profiles):
    """ Test the scatter plot on complexity profiles with models.

    Expecting no errors or exceptions.
    """
    # Filter the postprocess profiles
    tested_profiles = [p for p in list(postprocess_profiles) if 'computation' in p[0]]
    assert len(tested_profiles) == 5

    for profile in tested_profiles:
        # Create graphs from one profile
        graphs = scatter.create_from_params(profile[1], 'amount', 'structure-unit-size',
                                            'structure-unit-size', 'amount [us]',
                                            "Plot of 'amount' per 'structure-unit-size'")
        results = list(graphs)

        # Check if scatter plot generated expected amount of graphs for each profile
        if ('full_computation.perf' in profile[0] or 'initial_guess_computation.perf' in profile[0]
                or 'iterative_computation.perf' in profile[0]):
            assert len(results) == 2
        elif 'bisection_computation.perf' in profile[0]:
            assert len(results) == 4
        elif 'interval_computation.perf' in profile[0]:
            assert len(results) == 6
        else:
            assert False


def test_scatter_plot_no_models(full_profiles):
    """ Test the scatter plot on complexity profiles without models.

    Expecting no errors or exceptions.
    """
    # Filter the full profiles, only the complexity one is needed
    complexity_prof = [p for p in list(full_profiles) if 'prof-2-2017' in p[0]]
    assert len(complexity_prof) == 1
    profile = complexity_prof[0]

    # Create graphs from one profile without models
    graphs = scatter.create_from_params(profile[1], 'amount', 'structure-unit-size',
                                        'structure-unit-size', 'amount [us]',
                                        "Plot of 'amount' per 'structure-unit-size'")
    results = list(graphs)

    # Graphs for two functions should be generated
    assert len(results) == 2


def test_scatter_plot_cli(pcs_full, postprocess_profiles):
    """ Test creating bokeh scatter plot from the cli

    Expecting no errors and created scatter_plot_result0.html, scatter_plot_result1.html files
    """
    # Filter the postprocess profiles, test only on the full computation
    tested_profiles = [p for p in list(postprocess_profiles) if 'full_computation' in p[0]]
    assert len(tested_profiles) == 1
    profile = tested_profiles[0]

    # Run the cli on the given profile
    runner = CliRunner()
    result = runner.invoke(cli.show, [profile[0], 'scatter', '--of=amount',
                                      '--per=structure-unit-size', '--filename=scatter',
                                      '-xl=structure-unit-size', '-yl=amount [us]'])

    assert result.exit_code == 0
    assert 'scatter_result0.html' in os.listdir(os.getcwd())
    assert 'scatter_result1.html' in os.listdir(os.getcwd())


def test_scatter_plot_cli_errors(pcs_full, postprocess_profiles):
    """ Test creating bokeh scatter plot from the cli with invalid inputs

    Expecting to fail all commands and not create any graph files.
    """
    # Filter the postprocess profiles, test only on the full computation
    tested_profiles = [p for p in list(postprocess_profiles) if 'full_computation' in p[0]]
    assert len(tested_profiles) == 1
    profile = tested_profiles[0]

    runner = CliRunner()
    # Try invalid view argument
    result = runner.invoke(cli.show, [profile[0], 'scatterr', '--of=amount',
                                      '--per=structure-unit-size'])
    assert result.exit_code == 2
    assert 'No such command "scatterr"' in result.output

    # Try invalid --of value
    result = runner.invoke(cli.show, [profile[0], 'scatter', '--of=amou',
                                      '--per=structure-unit-size'])
    assert result.exit_code == 2
    assert 'invalid choice: amou' in result.output

    # Try invalid --per value
    result = runner.invoke(cli.show, [profile[0], 'scatter', '--of=amount',
                                      '--per=struct'])
    assert result.exit_code == 2
    assert 'invalid choice: struct' in result.output
