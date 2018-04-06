#!/usr/bin/env python3
"""Goblinoid CLI."""

import logging

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
@click.option('-v', '--verbose', is_flag=True, envvar='THOTH_SOLVER_DEBUG',
              help="Be verbose about what's going on.")
@click.option('--version', is_flag=True, is_eager=True, callback=_print_version, expose_value=False,
              help="Print Goblinoid version and exit.")
@click.option('--module-import', '-m', type=str, required=True,
              help="TODO")
@click.option('--models-iterable', '-i', type=str, required=True,
              help="TODO")
@click.option('--schema-file', type=click.File(mode='w'), required=False,
              default='./schema.groovy', show_default=True,
              help="TODO")
@click.option('--indexes-file', type=click.File(mode='w'), required=False,
              default='./indexes.groovy', show_default=True,
              help="TODO")
def cli(ctx=None, verbose=0, module_import=None, models_iterable=None, schema_file=None, indexes_file=None):
    """Thoth solver command line interface."""
    if ctx:
        ctx.auto_envvar_prefix = 'GOBLINOID'

    if verbose:
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("Debug mode turned on")
        _LOGGER.debug(f"Passed options: {locals()}")

    _LOGGER.info(f"Creating schema, writing result into {schema_file.name}")
    create_schema(module_import, models_iterable, schema_file.name)
    _LOGGER.info(f"Creating indexes, writing result into {indexes_file.name}")
    create_indexes(module_import, models_iterable, indexes_file.name)


if __name__ == '__main__':
    cli()
