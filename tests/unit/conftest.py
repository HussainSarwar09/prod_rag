import pytest


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    unit_marker = pytest.mark.unit
    for item in items:
        item.add_marker(unit_marker)
