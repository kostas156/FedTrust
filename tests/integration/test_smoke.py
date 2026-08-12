"""Integration smoke tests."""

import fedtrust


def test_package_import() -> None:
    """Package can be imported without errors."""
    assert fedtrust is not None
    assert hasattr(fedtrust, "__version__")
