from __future__ import annotations

from typing import ClassVar

import pytest

from prettytable import PrettyTable, RowType, TableStyle


class TestRowEndSection:
    EXPECTED_RESULT = """
┌──────────┬──────────┬──────────┐
│ Field 1  │ Field 2  │ Field 3  │
├──────────┼──────────┼──────────┤
│ value 4  │ value 5  │ value 6  │
│ value 7  │ value 8  │ value 9  │
├──────────┼──────────┼──────────┤
│ value 10 │ value 11 │ value 12 │
└──────────┴──────────┴──────────┘
""".strip()

    TEST_ROWS: ClassVar[list[list[str]]] = [
        ["value 4", "value 5", "value 6"],
        ["value 7", "value 8", "value 9"],
        ["value 10", "value 11", "value 12"],
    ]

    def test_row_end_section_via_argument(self) -> None:
        table = PrettyTable()
        table.set_style(TableStyle.SINGLE_BORDER)
        table.add_row(self.TEST_ROWS[0])
        table.add_row(self.TEST_ROWS[1], divider=True)
        table.add_row(self.TEST_ROWS[2])
        assert table.get_string().strip() == self.EXPECTED_RESULT

    def test_row_end_section_via_method(self) -> None:
        table = PrettyTable()
        table.set_style(TableStyle.SINGLE_BORDER)
        table.add_row(self.TEST_ROWS[0])
        table.add_row(self.TEST_ROWS[1])
        table.add_divider()
        table.add_row(self.TEST_ROWS[2])
        assert table.get_string().strip() == self.EXPECTED_RESULT

    def test_add_rows_divider(self) -> None:
        """A table created with two add_rows calls, one with divider=True has a
        divider"""
        table = PrettyTable()
        table.set_style(TableStyle.SINGLE_BORDER)
        table.add_rows(self.TEST_ROWS[0:2], divider=True)
        table.add_rows(self.TEST_ROWS[2:])
        assert table.get_string().strip() == self.EXPECTED_RESULT

    @pytest.mark.parametrize(
        ("oldsortslice", "sortby", "expected_values"),
        [(False, None, [2, 4, 5]), (True, None, [1, 2, 4, 5]), (False, "n", [2, 4, 5])],
    )
    def test_dividers_follow_selected_rows(
        self, oldsortslice: bool, sortby: str | None, expected_values: list[int]
    ) -> None:
        table = PrettyTable(["n"])
        for n in range(6):
            table.add_row([n], divider=n in (2, 4))

        seen = []

        def keep(row: RowType) -> bool:
            seen.append(row[0])
            return row[0] not in (0, 3)

        expected = PrettyTable(["n"])
        for n in expected_values:
            expected.add_row([n], divider=sortby is None and n in (2, 4))
        assert (
            table.get_string(
                start=1, oldsortslice=oldsortslice, sortby=sortby, row_filter=keep
            )
            == expected.get_string()
        )
        assert seen == list(range(1 if oldsortslice else 0, 6))


class TestClearing:
    def test_clear_rows(self, helper_table: PrettyTable) -> None:
        helper_table.add_row([0, "a", "b", "c"], divider=True)
        helper_table.clear_rows()
        assert helper_table.rows == []
        assert helper_table.dividers == []
        assert helper_table.field_names == ["", "Field 1", "Field 2", "Field 3"]

    def test_clear(self, helper_table: PrettyTable) -> None:
        helper_table.add_row([0, "a", "b", "c"], divider=True)
        helper_table.clear()
        assert helper_table.rows == []
        assert helper_table.dividers == []
        assert helper_table.field_names == []
