"""Scatter plot interpretation of the profile"""

import click

import perun.utils.cli_helpers as cli_helpers
import perun.utils.bokeh_helpers as bokeh_helpers
import perun.view.scatter.factory as scatter_factory

from perun.utils.helpers import pass_profile

__author__ = 'Jiri Pavela'


def process_title(ctx, _, value):
    """ Creates default title for scatter plot graph, if not provided by the user.

    If the value supplied from CLI is non-None, it is returned as it is. Otherwise, we try to
    create some optimal name for the graph ourselves. We do this according to already processed
    parameters as follows:

      Plot of 'of-key' per 'per-key'

    The title will be further expanded by relevant data to allow for easier identification of the
    result, as the scatter plot might produce more than one graph.

    Arguments:
        ctx(click.Context): called context of the process
        value(object): value that is being processed ad add to parameter

    Returns:
        object: either value (if it is non-None) or default title of the graph
    """
    if not value:
        # Construct default title of the graph
        return "Plot of '{}' per '{}'".format(ctx.params['of_key'], ctx.params['per_key'])
    return value


@click.command()
@click.option('--of', '-o', 'of_key', default='amount', nargs=1,
              show_default=True, type=str,
              is_eager=True, callback=cli_helpers.process_resource_key_param,
              help="Data source for the scatter plot, i.e. what will be displayed on Y axis.")
@click.option('--per', '-p', 'per_key', default='structure-unit-size', nargs=1,
              show_default=True, type=str,
              is_eager=True, callback=cli_helpers.process_resource_key_param,
              help="Keys that will be displayed on X axis of the scatter plot.")
# Not supported in the beta version
# @click.option('--for-uid', '-Fu', 'for_uid', multiple=True, metavar="<for_resource_uid>",
#               help=("Plot only specific resources identified by the uid keys. "
#                     "If not specified, all uid keys will be plotted."))
# @click.option('--except-uid', '-Xu', 'except_uid', multiple=True, metavar="<except_resource_uid>",
#               help=("Plot all resources except those identified by the uid keys. "
#                     "If used together with '--for_uid', then '--for_uid' is applied first in "
#                     "construction of the resulting filter."))
# @click.option('--with-models', '-w', 'with_models', is_flag=True, default=False, is_eager=True,
#               help="Also plot regression models if profile contains them.")
# @click.option('--for-model', '-Fm', 'for_model', multiple=True, type=(str, str, str),
#               help=("Plot only specific models identified by the <method model uid> list. "
#                     "Value '*' serves as a wildcard. "))
# @click.option('--except-model', '-Xm', 'except_model', multiple=True, type=(str, str, str),
#               help=("Plot all models except those specified by the <method model uid> list. "
#                     "Value '*' serves as a wildcard. Similarly to uid filter, the '--for-model' "
#                     "has precedence in filter construction."))
# Bokeh graph specific
@click.option('--filename', '-f', default="scatter", metavar="<html>",
              help="Outputs the graph to the file specified by filename.")
@click.option('--x-axis-label', '-xl', metavar="<text>", default=None,
              callback=cli_helpers.process_bokeh_axis_title,
              help="Label on the X axis of the scatter plot.")
@click.option('--y-axis-label', '-yl', metavar="<text>", default=None,
              callback=cli_helpers.process_bokeh_axis_title,
              help="Label on the Y axis of the scatter plot.")
@click.option('--graph-title', '-gt', metavar="<text>", default=None, callback=process_title,
              help="Title of the scatter plot.")
@click.option('--view-in-browser', '-v', default=False, is_flag=True,
              help="Will show the graph in browser.")
@pass_profile
def scatter(profile, filename, view_in_browser, **kwargs):
    """Interactive visualization of resources and models in scatter plot format.

    Scatter plot shows resources as points according to the given parameters.
    The plot interprets <per> and <of> as x, y coordinates for the points. The
    scatter plot also displays models located in the profile as a curves/lines.

    .. _Bokeh: https://bokeh.pydata.org/en/latest/

    \b
      * **Limitations**: `none`.
      * **Interpretation style**: graphical
      * **Visualization backend**: Bokeh_

    Features in progress:

      * uid filters
      * models filters
      * multiple graphs interpretation

    Graphs are displayed using the Bokeh_ library and can be further customized
    by adding custom labels for axis, custom graph title and different graph
    width.

    The example output of the scatter is as follows::

        \b
                                  <graph_title>
                          `                         o
                          -                        /
                          `                       /o       ```````````````````
                          -                     _/         `  o o = <points> `
                          `                   _- o         `    _             `
            <of>          -               __--o            `  _-  = <models> `
                          `    _______--o- o               `                 `
                          -    o  o  o                     ```````````````````
                          `
                          +````||````||````||````||````

                                      <per>

    Refer to :ref:`views-scatter` for more thorough description and example of
    `scatter` interpretation possibilities. For more thorough explanation of
    regression analysis and models refer to
    :ref:`postprocessors-regression-analysis`.
    """
    # discuss multiple results plotting (i.e. grid of plots? separate files? etc.)
    # Temporary solution for plotting multiple graphs from one command
    graphs = scatter_factory.create_from_params(profile, **kwargs)
    for idx, graph in enumerate(graphs):
        filename_uid = filename + '_result{0}.html'.format(idx)
        bokeh_helpers.save_graphs_in_column([graph], filename_uid, view_in_browser)
