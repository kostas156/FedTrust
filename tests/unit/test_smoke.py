"""Smoke tests for basic package functionality."""

import fedtrust


def test_version() -> None:
    """Package has a version string."""
    assert fedtrust.__version__ == "0.1.0"


def test_author() -> None:
    """Package has an author string."""
    assert isinstance(fedtrust.__author__, str)