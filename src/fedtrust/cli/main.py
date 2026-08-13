"""FedTrust command-line interface."""

import typer

from fedtrust import __version__

app = typer.Typer(
    name="fedtrust",
    help="Open-Source Evaluation Framework for Trustworthy Federated Learning Systems.",
)


def version_callback(value: bool) -> None:
    """Print the FedTrust version and exit."""
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        help="Show the FedTrust version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """FedTrust command-line interface."""


if __name__ == "__main__":
    app()
