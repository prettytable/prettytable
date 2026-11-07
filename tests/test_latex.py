from __future__ import annotations

import pytest

from prettytable import HRuleStyle, PrettyTable, VRuleStyle


class TestLatexOutput:
    @pytest.mark.parametrize("formatted", [False, True])
    @pytest.mark.parametrize("header", [False, True])
    @pytest.mark.parametrize("row_count", [0, 1, 2])
    @pytest.mark.parametrize(
        ("fields", "indexes"),
        [
            (None, (0, 1, 2)),
            ([], (0, 1, 2)),
            (["City", "Age", "Name"], (0, 1, 2)),
            (["City", "Name"], (0, 2)),
            (["City", "Name", "City"], (0, 2)),
            (["Age"], (1,)),
            (["City"], (2,)),
        ],
    )
    def test_latex_field_selection(
        self,
        formatted: bool,
        header: bool,
        row_count: int,
        fields: list[str] | None,
        indexes: tuple[int, ...],
    ) -> None:
        names = ["Name", "Age", "City"]
        rows = [["Ada", "35", "London"], ["Linus", "56", "Helsinki"]][:row_count]
        table = PrettyTable(names)
        table.add_rows(rows)

        alignment = "|".join("c" for _ in indexes) if formatted else "c" * len(indexes)
        if formatted:
            alignment = f"|{alignment}|"
        lines = [rf"\begin{{tabular}}{{{alignment}}}"]
        if formatted:
            lines.append(r"\hline")
        if header:
            lines.append(" & ".join(names[i] for i in indexes) + r" \\")
        lines.extend(" & ".join(row[i] for i in indexes) + r" \\" for row in rows)
        if formatted:
            lines.append(r"\hline")
        lines.append(r"\end{tabular}")

        if fields is None:
            output = table.get_latex_string(format=formatted, header=header)
        else:
            output = table.get_latex_string(
                fields=fields, format=formatted, header=header
            )
        assert output == "\r\n".join(lines)

    @pytest.mark.parametrize("formatted", [False, True])
    @pytest.mark.parametrize("column_count", [5, 8, 20])
    @pytest.mark.parametrize("subset", [False, True])
    def test_latex_wide_field_selection(
        self, formatted: bool, column_count: int, subset: bool
    ) -> None:
        names = [f"Field {i}" for i in range(column_count)]
        rows = [list(range(column_count)), list(range(column_count, 2 * column_count))]
        indexes = list(range(0, column_count, 2) if subset else range(column_count))
        table = PrettyTable(names)
        table.add_rows(rows)
        requested = [names[i] for i in indexes][::-1] * 2
        output = table.get_latex_string(fields=requested, format=formatted)
        data_lines = [line for line in output.splitlines() if not line.startswith("\\")]
        assert data_lines == [
            " & ".join(names[i] for i in indexes) + r" \\",
            *(" & ".join(str(row[i]) for i in indexes) + r" \\" for row in rows),
        ]

    @pytest.mark.parametrize("formatted", [False, True])
    def test_latex_selection_after_formatting(self, formatted: bool) -> None:
        names = ["Name", "Age", "City", "Start", "Job", "Salary", "Status"]
        table = PrettyTable(names)
        table.add_rows(
            [
                ["Ada", 35, "London", "2024-04-01", "Analyst", 45000, "Active"],
                ["Linus", 56, "Helsinki", "2020-01-01", "Manager", 80000, "Contract"],
            ]
        )

        def format_status(field: str, value: object) -> str:
            if value == "Contract":
                table.field_names[:] = names[::-1]
            return str(value)

        table.custom_format["Status"] = format_status
        output = table.get_latex_string(fields=names[:-1], format=formatted)
        assert "Name & Age & City & Start & Job & Salary" + r" \\" in output
        assert "35 & London & 2024-04-01 & Analyst & 45000 & Active" + r" \\" in output
        assert (
            "56 & Helsinki & 2020-01-01 & Manager & 80000 & Contract" + r" \\" in output
        )

    @pytest.mark.parametrize("formatted", [False, True])
    def test_latex_custom_field_membership(self, formatted: bool) -> None:
        class Header(str):
            comparisons = 0
            reject_hash = False

            def __eq__(self, other: object) -> bool:
                self.comparisons += 1
                return str.__eq__(self, other)

            def __hash__(self) -> int:
                assert not self.reject_hash
                return str.__hash__(self)

        name = Header("Name")
        names = [name, *(f"Detail {i}" for i in range(9))]
        table = PrettyTable(names)
        table.field_names[0] = name
        table.add_rows([list(range(10)), list(range(10, 20))])

        def format_last(field: str, value: object) -> str:
            name.comparisons = 0
            name.reject_hash = value == 19
            return str(value)

        table.custom_format[names[-1]] = format_last
        output = table.get_latex_string(fields=names[1:], format=formatted)
        assert "1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9" + r" \\" in output
        assert name.comparisons == 18

    def test_latex_output(self, helper_table: PrettyTable) -> None:
        assert helper_table.get_latex_string() == (
            "\\begin{tabular}{cccc}\r\n"
            " & Field 1 & Field 2 & Field 3 \\\\\r\n"
            "1 & value 1 & value2 & value3 \\\\\r\n"
            "4 & value 4 & value5 & value6 \\\\\r\n"
            "7 & value 7 & value8 & value9 \\\\\r\n"
            "\\end{tabular}"
        )
        options = {"fields": ["Field 1", "Field 3"]}
        assert helper_table.get_latex_string(**options) == (
            "\\begin{tabular}{cc}\r\n"
            "Field 1 & Field 3 \\\\\r\n"
            "value 1 & value3 \\\\\r\n"
            "value 4 & value6 \\\\\r\n"
            "value 7 & value9 \\\\\r\n"
            "\\end{tabular}"
        )

    def test_latex_output_formatted(self, helper_table: PrettyTable) -> None:
        assert helper_table.get_latex_string(format=True) == (
            "\\begin{tabular}{|c|c|c|c|}\r\n"
            "\\hline\r\n"
            " & Field 1 & Field 2 & Field 3 \\\\\r\n"
            "1 & value 1 & value2 & value3 \\\\\r\n"
            "4 & value 4 & value5 & value6 \\\\\r\n"
            "7 & value 7 & value8 & value9 \\\\\r\n"
            "\\hline\r\n"
            "\\end{tabular}"
        )

        options = {"fields": ["Field 1", "Field 3"]}
        assert helper_table.get_latex_string(format=True, **options) == (
            "\\begin{tabular}{|c|c|}\r\n"
            "\\hline\r\n"
            "Field 1 & Field 3 \\\\\r\n"
            "value 1 & value3 \\\\\r\n"
            "value 4 & value6 \\\\\r\n"
            "value 7 & value9 \\\\\r\n"
            "\\hline\r\n"
            "\\end{tabular}"
        )

        vrule_options: dict[str, VRuleStyle] = {"vrules": VRuleStyle.FRAME}
        assert helper_table.get_latex_string(format=True, **vrule_options) == (
            "\\begin{tabular}{|cccc|}\r\n"
            "\\hline\r\n"
            " & Field 1 & Field 2 & Field 3 \\\\\r\n"
            "1 & value 1 & value2 & value3 \\\\\r\n"
            "4 & value 4 & value5 & value6 \\\\\r\n"
            "7 & value 7 & value8 & value9 \\\\\r\n"
            "\\hline\r\n"
            "\\end{tabular}"
        )

        hrule_options: dict[str, HRuleStyle] = {"hrules": HRuleStyle.ALL}
        assert helper_table.get_latex_string(format=True, **hrule_options) == (
            "\\begin{tabular}{|c|c|c|c|}\r\n"
            "\\hline\r\n"
            " & Field 1 & Field 2 & Field 3 \\\\\r\n"
            "\\hline\r\n"
            "1 & value 1 & value2 & value3 \\\\\r\n"
            "\\hline\r\n"
            "4 & value 4 & value5 & value6 \\\\\r\n"
            "\\hline\r\n"
            "7 & value 7 & value8 & value9 \\\\\r\n"
            "\\hline\r\n"
            "\\end{tabular}"
        )

    def test_latex_output_header(self, helper_table: PrettyTable) -> None:
        assert helper_table.get_latex_string(format=True, hrules=HRuleStyle.HEADER) == (
            "\\begin{tabular}{|c|c|c|c|}\r\n"
            " & Field 1 & Field 2 & Field 3 \\\\\r\n"
            "\\hline\r\n"
            "1 & value 1 & value2 & value3 \\\\\r\n"
            "4 & value 4 & value5 & value6 \\\\\r\n"
            "7 & value 7 & value8 & value9 \\\\\r\n"
            "\\end{tabular}"
        )

    def test_internal_border_preserved_latex(self, helper_table: PrettyTable) -> None:
        helper_table.border = False
        helper_table.format = True
        helper_table.preserve_internal_border = True

        assert helper_table.get_latex_string().strip() == (
            "\\begin{tabular}{c|c|c|c}\r\n"
            " & Field 1 & Field 2 & Field 3 \\\\\r\n"
            "1 & value 1 & value2 & value3 \\\\\r\n"
            "4 & value 4 & value5 & value6 \\\\\r\n"
            "7 & value 7 & value8 & value9 \\\\\r\n"
            "\\end{tabular}"
        )
