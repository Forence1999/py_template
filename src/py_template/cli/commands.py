"""Command-line interface for py_template."""

import click

from py_template.__version__ import __version__


@click.group()
@click.version_option(version=__version__, prog_name="py_template")
def main():
    """py_template - A minimal Python project template."""


@main.command()
def info():
    """Display template information."""
    click.echo(f"py_template v{__version__}")
    click.echo("A minimal Python project template")
    click.echo("\nUse this template to start your own Python project.")


@main.command()
@click.option("--name", default="World", help="Name to greet")
def hello(name):
    """Say hello (example command)."""
    click.echo(f"Hello, {name}!")
    click.echo("\nThis is an example command.")
    click.echo("You can replace this with your own commands.")


if __name__ == "__main__":
    main()
