"""Tests for the FedTrust command-line interface."""

from typer.testing import CliRunner

from fedtrust.cli.main import app

runner = CliRunner()


def test_help() -> None:
    """CLI displays help information."""
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "FedTrust" in result.stdout
    assert "Open-Source Evaluation Framework" in result.stdout


def test_version() -> None:
    """CLI displays the package version."""
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "0.1.0"
