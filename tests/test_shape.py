from __future__ import annotations

import pytest

from prettytable import PrettyTable


def test_shape_tracks_mutations():
    table = PrettyTable()
    assert table.shape == (0, 0)
    table.field_names = ["a", "b"]
    assert table.shape == (0, 2)
    table.add_rows([[1, 2], [3, 4]])
    assert table.shape == (2, 2)
    table.add_column("c", [5, 6])
    assert table.shape == (2, 3)
    table.del_row(0)
    assert table.shape == (1, 3)
    table.del_column("a")
    assert table.shape == (1, 2)
    table.clear_rows()
    assert table.shape == (0, 2)
    table.clear()
    assert table.shape == (0, 0)


def test_shape_describes_stored_data():
    table = PrettyTable(["a", "b"])
    table.add_rows([[1, 2], [3, 4], [5, 6]])
    table.start = 1
    table.end = 2
    table.fields = ["a"]
    table.header = False
    assert table.shape == (3, 2)
    assert table[1:].shape == (2, 2)
    assert table.shape == (table.rowcount, table.colcount)


def test_shape_is_read_only():
    with pytest.raises(AttributeError):
        PrettyTable().shape = (1, 1)
