#!/usr/bin/env python3
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
    "--schema-file",
    type=click.File(mode="w"),
    required=False,
    default="./schema.groovy",
    show_default=True,
    help="Define a name and path of the resulting schema.",
)
def cli(
    ctx=None,
    verbose=0,
    module_import=None,
    models_iterable=None,
    keep_schema_maker=False,
    schema_vertex_identifier=None,
    schema_file=None,
):
    """Create graph database schema automatically from source code."""
    if ctx:
        ctx.auto_envvar_prefix = "GOBLINOID"

    if verbose:
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("Debug mode turned on")
        _LOGGER.debug(f"Passed options: {locals()}")

    _LOGGER.info(f"Creating schema, writing result into {schema_file.name}")
    create_schema(
        module_import,
        models_iterable,
        schema_file.name,
    )


if __name__ == "__main__":
    cli()
