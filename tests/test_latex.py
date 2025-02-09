from __future__ import annotations

from test_prettytable import helper_table

from prettytable import HRuleStyle, VRuleStyle


class TestLatexOutput:
    def test_latex_output(self) -> None:
        t = helper_table()
        assert t.get_latex_string() == (
            "\\begin{tabular}{cccc}\r\n"
            " & Field 1 & Field 2 & Field 3 \\\\\r\n"
            "1 & value 1 & value2 & value3 \\\\\r\n"
            "4 & value 4 & value5 & value6 \\\\\r\n"
            "7 & value 7 & value8 & value9 \\\\\r\n"
            "\\end{tabular}"
        )
        options = {"fields": ["Field 1", "Field 3"]}
        assert t.get_latex_string(**options) == (
            "\\begin{tabular}{cc}\r\n"
            "Field 1 & Field 3 \\\\\r\n"
            "value 1 & value3 \\\\\r\n"
            "value 4 & value6 \\\\\r\n"
            "value 7 & value9 \\\\\r\n"
            "\\end{tabular}"
        )

    def test_latex_output_formatted(self) -> None:
        t = helper_table()
        assert t.get_latex_string(format=True) == (
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
        assert t.get_latex_string(format=True, **options) == (
            "\\begin{tabular}{|c|c|}\r\n"
            "\\hline\r\n"
            "Field 1 & Field 3 \\\\\r\n"
            "value 1 & value3 \\\\\r\n"
            "value 4 & value6 \\\\\r\n"
            "value 7 & value9 \\\\\r\n"
            "\\hline\r\n"
            "\\end{tabular}"
        )

        options = {"vrules": VRuleStyle.FRAME}
        assert t.get_latex_string(format=True, **options) == (
            "\\begin{tabular}{|cccc|}\r\n"
            "\\hline\r\n"
            " & Field 1 & Field 2 & Field 3 \\\\\r\n"
            "1 & value 1 & value2 & value3 \\\\\r\n"
            "4 & value 4 & value5 & value6 \\\\\r\n"
            "7 & value 7 & value8 & value9 \\\\\r\n"
            "\\hline\r\n"
            "\\end{tabular}"
        )

        options = {"hrules": HRuleStyle.ALL}
        assert t.get_latex_string(format=True, **options) == (
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

    def test_latex_output_header(self) -> None:
        t = helper_table()
        assert t.get_latex_string(format=True, hrules=HRuleStyle.HEADER) == (
            "\\begin{tabular}{|c|c|c|c|}\r\n"
            " & Field 1 & Field 2 & Field 3 \\\\\r\n"
            "\\hline\r\n"
            "1 & value 1 & value2 & value3 \\\\\r\n"
            "4 & value 4 & value5 & value6 \\\\\r\n"
            "7 & value 7 & value8 & value9 \\\\\r\n"
            "\\end{tabular}"
        )

    def test_internal_border_preserved_latex(self) -> None:
        pt = helper_table()
        pt.border = False
        pt.format = True
        pt.preserve_internal_border = True

        assert pt.get_latex_string().strip() == (
            "\\begin{tabular}{c|c|c|c}\r\n"
            " & Field 1 & Field 2 & Field 3 \\\\\r\n"
            "1 & value 1 & value2 & value3 \\\\\r\n"
            "4 & value 4 & value5 & value6 \\\\\r\n"
            "7 & value 7 & value8 & value9 \\\\\r\n"
            "\\end{tabular}"
        )
