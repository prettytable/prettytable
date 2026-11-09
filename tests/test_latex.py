from __future__ import annotations

from prettytable import HRuleStyle, PrettyTable, VRuleStyle


class TestLatexOutput:
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

    def test_latex_escapes_special_characters(self) -> None:
        """LaTeX specials in headers and cells must be escaped (issue #542)."""
        table = PrettyTable()
        table.field_names = ["Na_me", "A&B"]
        table.add_row(["100%", "5$"])
        table.add_row(["a#b", "x{y}"])

        assert table.get_latex_string() == (
            "\\begin{tabular}{cc}\r\n"
            "Na\\_me & A\\&B \\\\\r\n"
            "100\\% & 5\\$ \\\\\r\n"
            "a\\#b & x\\{y\\} \\\\\r\n"
            "\\end{tabular}"
        )

    def test_latex_formatted_escapes_special_characters(self) -> None:
        """The formatted LaTeX path escapes specials too (issue #542)."""
        table = PrettyTable()
        table.field_names = ["col_1"]
        table.add_row(["50%"])

        assert table.get_latex_string(format=True) == (
            "\\begin{tabular}{|c|}\r\n"
            "\\hline\r\n"
            "col\\_1 \\\\\r\n"
            "50\\% \\\\\r\n"
            "\\hline\r\n"
            "\\end{tabular}"
        )

    def test_latex_escapes_backslash_tilde_caret(self) -> None:
        """Backslash must not double-escape characters added by the escaping."""
        table = PrettyTable()
        table.field_names = ["a~b"]
        table.add_row(["x\\y"])

        assert table.get_latex_string() == (
            "\\begin{tabular}{c}\r\n"
            "a\\textasciitilde{}b \\\\\r\n"
            "x\\textbackslash{}y \\\\\r\n"
            "\\end{tabular}"
        )
