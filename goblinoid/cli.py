#!/usr/bin/env python3
"""Goblinoid CLI."""

import logging
import sys

import click
import daiquiri

from goblinoid import create_indexes
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
@click.option('-v', '--verbose', is_flag=True,
              help="Be verbose about what's going on.")
@click.option('--version', is_flag=True, is_eager=True, callback=_print_version, expose_value=False,
              help="Print Goblinoid version and exit.")
@click.option('--module-import', '-m', type=str, required=True,
              help="Python's import specification to a package/module from where models iterable should be imported.")
@click.option('--models-iterable', '-i', type=str, required=False,
              help="A name of iterable that holds all models defined.")
@click.option('--indexes-iterable', '-I', type=str, required=False,
              help="A name of iterable that holds all indexes defined.")
@click.option('--schema-file', type=click.File(mode='w'), required=False,
              default='./schema.groovy', show_default=True,
              help="Define a name and path of the resulting schema.")
@click.option('--indexes-file', type=click.File(mode='w'), required=False,
              default='./indexes.groovy', show_default=True,
              help="Define a name and path of the resulting index definitions.")
@click.option('--keep-schema-maker', is_flag=True,
              help="Keep default schema maker for undefined vertex/edge types (*NOT* recommended).")
@click.option('--schema-vertex-identifier', type=str, default=None,
              help="Create a special vertex in the graph database holding schema version "
                   "and creation time (recommended to provide).")
def cli(ctx=None, verbose=0, module_import=None, models_iterable=None, indexes_iterable=None,
        keep_schema_maker=False, schema_vertex_identifier=None,
        schema_file=None, indexes_file=None):
    """Create graph database schema and indexes automatically from source code."""
    if ctx:
        ctx.auto_envvar_prefix = 'GOBLINOID'

    if verbose:
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("Debug mode turned on")
        _LOGGER.debug(f"Passed options: {locals()}")

    if models_iterable:
        _LOGGER.info(f"Creating schema, writing result into {schema_file.name}")
        create_schema(module_import, models_iterable, schema_file.name,
                      remove_schema_maker=not keep_schema_maker, schema_vertex_identifier=schema_vertex_identifier)

    if indexes_iterable:
        _LOGGER.info(f"Creating indexes, writing result into {indexes_file.name}")
        create_indexes(module_import, indexes_iterable, indexes_file.name)

    if not models_iterable and not indexes_iterable:
        _LOGGER.error("Please specify indexes and/or modules iterable to generate indexes/schema from.")
        sys.exit(1)


if __name__ == '__main__':
    cli()
