#!/usr/bin/env python3
# goblinoid
# Copyright(C) 2018-2019 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Goblinoid CLI."""

import logging

import click
import daiquiri

from goblinoid import create_schema
from goblinoid import __version__ as goblinoid_version

daiquiri.setup(level=logging.INFO)

_LOGGER = logging.getLogger(__name__)


def _print_version(ctx, _, value):
    """Print Goblinoid version and exit."""
    if not value or ctx.resilient_parsing:
        return
    click.echo(goblinoid_version)
    ctx.exit()


@click.command()
@click.pass_context
@click.option("-v", "--verbose", is_flag=True, help="Be verbose about what's going on.")
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    callback=_print_version,
    expose_value=False,
    help="Print Goblinoid version and exit.",
)
@click.option(
    "--module-import",
    "-m",
    type=str,
    required=True,
    help="Python's import specification to a package/module from where models iterable should be imported.",
)
@click.option(
    "--models-iterable",
    "-i",
    type=str,
    required=True,
    help="A name of iterable that holds all models defined.",
)
@click.option(
    "--output-file",
    "-o",
    type=click.File(mode="w"),
    required=False,
    default="./init.groovy",
    show_default=True,
    help="Define a name and path of the resulting file.",
)
@click.option(
    "--index-file",
    type=click.File(mode="r"),
    required=False,
    default=None,
    help="A path to index file to be used to append indexes the resulting file.",
)
def cli(
    ctx=None,
    verbose=0,
    module_import=None,
    models_iterable=None,
    keep_schema_maker=False,
    schema_vertex_identifier=None,
    output_file=None,
    index_file=None,
):
    """Create graph database schema automatically from source code."""
    if ctx:
        ctx.auto_envvar_prefix = "GOBLINOID"

    if verbose:
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("Debug mode turned on")
        _LOGGER.debug(f"Passed options: {locals()}")

    _LOGGER.info(f"Creating schema, writing result into {output_file.name}")
    create_schema(
        module_import,
        models_iterable,
        output_file.name,
        index_file.name if index_file else None,
    )


if __name__ == "__main__":
    cli()
