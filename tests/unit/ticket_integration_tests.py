import pytest
from src.utils.helpers import map_priority


def test_priority_mapping():
    assert map_priority(1) in ["low", "medium", "high"]
