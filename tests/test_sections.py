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


class TestSectionSelection:
    @pytest.mark.parametrize(
        "flags,rejected,start,oldsortslice,expected",
        [
            (
                [False, True, False, False],
                "A",
                0,
                False,
                [("B", True), ("C", False), ("D", False)],
            ),
            (
                [True, False, False, False],
                "A",
                0,
                False,
                [("B", False), ("C", False), ("D", False)],
            ),
            (
                [False, True, False, False],
                "",
                1,
                False,
                [("B", True), ("C", False), ("D", False)],
            ),
            ([False, True, False, False], "B", 1, True, [("C", False), ("D", False)]),
        ],
        ids=["filter-unflagged", "filter-flagged", "slice", "legacy-filter"],
    )
    def test_dividers_follow_selected_rows(
        self,
        flags: list[bool],
        rejected: str,
        start: int,
        oldsortslice: bool,
        expected: list[tuple[str, bool]],
    ) -> None:
        table = PrettyTable(["value"])
        for value, divider in zip("ABCD", flags):
            table.add_row([value], divider=divider)
        control = PrettyTable(["value"])
        for value, divider in expected:
            control.add_row([value], divider=divider)

        assert (
            table.get_string(
                row_filter=lambda row: row[0] != rejected,
                start=start,
                oldsortslice=oldsortslice,
            )
            == control.get_string()
        )
        assert table.rows == [[value] for value in "ABCD"]
        assert table.dividers == flags

    @pytest.mark.parametrize("oldsortslice", [False, True])
    def test_filter_runs_once_in_slice_order(self, oldsortslice: bool) -> None:
        table = PrettyTable(["value"])
        for value in "ABCD":
            table.add_row([value], divider=value == "B")
        visited: list[str] = []

        def row_filter(row: RowType) -> bool:
            visited.append(row[0])
            return row[0] != "A"

        control = PrettyTable(["value"])
        for value in "BC" if oldsortslice else "CD":
            control.add_row([value], divider=value == "B")
        assert (
            table.get_string(
                row_filter=row_filter, start=1, end=3, oldsortslice=oldsortslice
            )
            == control.get_string()
        )
        assert visited == list("BC" if oldsortslice else "ABCD")

    @pytest.mark.parametrize("reverse,expected", [(False, "BDCA"), (True, "ACBD")])
    def test_sort_clears_dividers_and_preserves_callbacks(
        self, reverse: bool, expected: str
    ) -> None:
        rows = [[3, "A"], [1, "B"], [2, "C"], [1, "D"]]
        table = PrettyTable(["key", "value"])
        for row in rows:
            table.add_row(row, divider=True)
        visited: list[str] = []
        sort_inputs: list[RowType] = []

        def row_filter(row: RowType) -> bool:
            visited.append(row[1])
            return True

        def sort_key(row: RowType) -> int:
            assert visited == list("ABCD")
            sort_inputs.append(row[:])
            return row[0]

        control = PrettyTable(["key", "value"])
        for value in expected:
            control.add_row(next(row for row in rows if row[1] == value))
        assert (
            table.get_string(
                sortby="key",
                reversesort=reverse,
                sort_key=sort_key,
                row_filter=row_filter,
            )
            == control.get_string()
        )
        assert sort_inputs == [[row[0], *row] for row in rows]
        assert table.rows == rows
        assert table.dividers == [True, True, True, True]

    def test_duplicate_rows_keep_distinct_dividers(self) -> None:
        table = PrettyTable(["value"])
        table.add_row(["A"])
        table.add_row(["B"], divider=True)
        table.add_row(["B"])
        table.add_row(["C"])
        control = PrettyTable(["value"])
        control.add_row(["B"], divider=True)
        control.add_row(["B"])
        control.add_row(["C"])
        assert (
            table.get_string(row_filter=lambda row: row[0] != "A")
            == control.get_string()
        )

    @pytest.mark.parametrize(
        "oldsortslice,sortby,expected",
        [
            (False, None, [False, True, False, False]),
            (True, None, [True, False]),
            (False, "value", [False, False, False, False]),
            (True, "value", [False, False]),
        ],
    )
    def test_legacy_divider_getter_does_not_call_selection_callbacks(
        self, oldsortslice: bool, sortby: str | None, expected: list[bool]
    ) -> None:
        table = PrettyTable(["value"])
        for value in "ABCD":
            table.add_row([value], divider=value == "B")

        def unexpected_callback(row: RowType) -> bool:
            msg = "Divider lookup must not invoke selection callbacks"
            raise AssertionError(msg)

        options = table._get_options(
            {
                "start": 1,
                "end": 3,
                "oldsortslice": oldsortslice,
                "sortby": sortby,
                "row_filter": unexpected_callback,
                "sort_key": unexpected_callback,
            }
        )
        assert table._get_dividers(options) == expected

    def test_legacy_divider_getter_retains_default_list(self) -> None:
        table = PrettyTable(["value"])
        table.add_row(["A"], divider=True)
        assert table._get_dividers(table._get_options({})) is table._dividers

    def test_legacy_filter_sort_slice_order(self) -> None:
        rows = [[9, "A"], [3, "B"], [1, "C"], [2, "D"], [0, "E"]]
        table = PrettyTable(["key", "value"])
        for row in rows:
            table.add_row(row, divider=True)
        visited: list[str] = []
        sort_inputs: list[RowType] = []

        def row_filter(row: RowType) -> bool:
            visited.append(row[1])
            return row[1] != "C"

        def sort_key(row: RowType) -> int:
            assert visited == list("BCD")
            sort_inputs.append(row[:])
            return row[0]

        control = PrettyTable(["key", "value"])
        control.add_rows([rows[3], rows[1]])
        assert (
            table.get_string(
                oldsortslice=True,
                start=1,
                end=4,
                row_filter=row_filter,
                sortby="key",
                sort_key=sort_key,
            )
            == control.get_string()
        )
        assert visited == list("BCD")
        assert sort_inputs == [[3, 3, "B"], [2, 2, "D"]]
        assert table.rows == rows
        assert table.dividers == [True] * len(rows)

    def test_filtered_empty_table(self) -> None:
        table = PrettyTable(["value"])
        table.add_row(["A"], divider=True)
        assert (
            table.get_string(row_filter=lambda row: False)
            == PrettyTable(["value"]).get_string()
        )

    def test_paginated_dividers(self) -> None:
        table = PrettyTable(["value"])
        for value in "ABCD":
            table.add_row([value], divider=value == "C")
        first = PrettyTable(["value"])
        first.add_rows([["A"], ["B"]])
        second = PrettyTable(["value"])
        second.add_row(["C"], divider=True)
        second.add_row(["D"])
        assert (
            table.paginate(page_length=2)
            == first.get_string() + "\f" + second.get_string()
        )


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
