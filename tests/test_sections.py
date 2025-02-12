from __future__ import annotations

from prettytable import PrettyTable, TableStyle


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

    def test_row_end_section_via_argument(self) -> None:
        table = PrettyTable()
        table.set_style(TableStyle.SINGLE_BORDER)
        table.add_row(["value 4", "value 5", "value 6"])
        table.add_row(["value 7", "value 8", "value 9"], divider=True)
        table.add_row(["value 10", "value 11", "value 12"])

        assert table.get_string().strip() == self.EXPECTED_RESULT

    def test_row_end_section_via_method(self) -> None:
        table = PrettyTable()
        table.set_style(TableStyle.SINGLE_BORDER)
        table.add_row(["value 4", "value 5", "value 6"])
        table.add_row(["value 7", "value 8", "value 9"])
        table.add_divider()
        table.add_row(["value 10", "value 11", "value 12"])

        assert table.get_string().strip() == self.EXPECTED_RESULT


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
