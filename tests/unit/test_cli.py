"""Test CLI commands."""

from click.testing import CliRunner

from py_template.cli.commands import main


def test_info_command():
    """Test info command."""
    runner = CliRunner()
    result = runner.invoke(main, ["info"])
    assert result.exit_code == 0
    assert "py_template" in result.output
    assert "0.1.0" in result.output


def test_hello_command():
    """Test hello command."""
    runner = CliRunner()
    result = runner.invoke(main, ["hello"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_hello_command_with_name():
    """Test hello command with custom name."""
    runner = CliRunner()
    result = runner.invoke(main, ["hello", "--name", "Python"])
    assert result.exit_code == 0
    assert "Hello, Python!" in result.output
