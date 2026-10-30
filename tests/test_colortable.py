from __future__ import annotations

import re
from typing import Literal

import pytest
from test_prettytable import CITY_DATA, CITY_DATA_HEADER

from prettytable import PrettyTable, TableStyle
from prettytable.colortable import RESET_CODE, ColorTable, Theme, Themes


@pytest.fixture
def row_colortable() -> PrettyTable:
    table = ColorTable()
    table.field_names = CITY_DATA_HEADER
    for row in CITY_DATA:
        table.add_row(row)
    return table


@pytest.fixture
def color_theme() -> Theme:
    return Theme(
        default_color="31",
        vertical_color="32",
        horizontal_color="33",
        junction_color="34",
    )


class TestColorTable:
    def test_themeless(
        self, row_prettytable: PrettyTable, row_colortable: ColorTable
    ) -> None:
        # Not worth the logic customizing the reset code
        # For now we'll just get rid of it
        assert (
            row_colortable.get_string().replace(RESET_CODE, "")
            == row_prettytable.get_string()
        )

    def test_theme_setter(self, color_theme: Theme) -> None:
        table1 = ColorTable(theme=color_theme)

        table2 = ColorTable()
        table2.theme = color_theme

        assert table1.theme == table2.theme

        dict1 = table1.__dict__
        dict2 = table2.__dict__

        # So we don't compare functions
        for func in ("_sort_key", "_row_filter"):
            del dict1[func]
            del dict2[func]

        assert dict1 == dict2


class TestFormatCode:
    def test_basic(self) -> None:
        assert Theme.format_code("31") == "\x1b[31m"

    def test_prefix(self) -> None:
        assert Theme.format_code("\x1b[35m") == "\x1b[35m"

    def test_escapes(self) -> None:
        assert Theme.format_code("\033[41m") == "\x1b[41m"
        assert Theme.format_code("\u001b[41m") == "\x1b[41m"

    def test_empty(self) -> None:
        assert Theme.format_code("") == ""

    def test_stripped(self) -> None:
        assert Theme.format_code("\t\t     \t") == ""

    def test_multiple(self) -> None:
        assert Theme.format_code("30;42") == "\x1b[30;42m"
        assert Theme.format_code("\x1b[30;42m") == "\x1b[30;42m"


class TestColorTableRendering:
    """Tests for the rendering of the color table

    Methods
    -------
    test_color_table_rendering
        Tests the color table rendering using the default alignment (`'c'`)
    """

    @pytest.mark.parametrize(
        ["with_title", "with_header"],
        [
            (False, True),  # the default
            (True, True),  # titled
            (True, False),  # titled, no header
        ],
    )
    def test_color_table_rendering(self, with_title: bool, with_header: bool) -> None:
        """Tests the color table rendering using the default alignment (`'c'`)"""
        chars = {
            "+": "\x1b[36m+\x1b[0m\x1b[96m",
            "-": "\x1b[34m-\x1b[0m\x1b[96m",
            "|": "\x1b[34m|\x1b[0m\x1b[96m",
            " ": " ",
        }

        plus = chars.get("+")
        minus = chars.get("-")
        pipe = chars.get("|")
        space = chars.get(" ")
        assert isinstance(plus, str)
        assert isinstance(minus, str)
        assert isinstance(pipe, str)
        assert isinstance(space, str)

        # +-----------------------+
        # |        Efforts        |
        # +---+---+---+---+---+---+
        # | A | B | C | D | E | f |
        # +---+---+---+---+---+---+
        # | 1 | 2 | 3 | 4 | 5 | 6 |
        # +---+---+---+---+---+---+

        header = (
            plus + minus * 23 + plus,
            pipe + space * 8 + "Efforts" + space * 8 + pipe,
            (plus + minus * 3) * 6 + plus,
        )

        body = (
            "".join(pipe + space + char + space for char in "ABCDEF") + pipe,
            (plus + minus * 3) * 6 + plus,
            "".join(pipe + space + char + space for char in "123456") + pipe,
            (plus + minus * 3) * 6 + plus,
        )

        if with_title:
            header_str = str("\n".join(header))
        else:
            header_str = str(header[2])
        if with_header:
            body_str = str("\n".join(body))
        else:
            body_str = str("\n".join(body[2:]))

        table = ColorTable(
            ("A", "B", "C", "D", "E", "F"),
            theme=Themes.OCEAN,
        )

        if with_title:
            table.title = "Efforts"
        table.header = with_header
        table.add_row([1, 2, 3, 4, 5, 6])

        expected = f"{header_str}\n{body_str}\x1b[0m"
        result = str(table)

        assert expected == result

    def test_all_themes(self) -> None:
        """Tests rendering with all available themes"""
        table = ColorTable(
            ("A", "B", "C", "D", "E", "F"),
        )
        table.title = "Theme Test"
        table.add_row([1, 2, 3, 4, 5, 6])

        for theme in vars(Themes).values():
            if isinstance(theme, Theme):
                table.theme = theme
                result = str(table)
                assert result  # Simple check to ensure rendering doesn't fail

    @pytest.mark.parametrize(
        "style", [TableStyle.DOUBLE_BORDER, TableStyle.SINGLE_BORDER]
    )
    @pytest.mark.parametrize("theme_first", [True, False])
    @pytest.mark.parametrize("with_title", [True, False])
    def test_border_style_and_theme_order(
        self, style: TableStyle, theme_first: bool, with_title: bool
    ) -> None:
        plain = PrettyTable(["name", "count"])
        plain.add_row(["alpha", 7])
        plain.set_style(style)
        table = ColorTable(["name", "count"])
        table.add_row(["alpha", 7])
        if theme_first:
            table.theme = Themes.OCEAN
            table.set_style(style)
        else:
            table.set_style(style)
            table.theme = Themes.OCEAN
        if with_title:
            plain.title = table.title = "Colors and borders"

        result = table.get_string()
        assert re.sub(r"\x1b\[[0-9;]*m", "", result) == plain.get_string()
        assert Themes.OCEAN.vertical_color in result
        assert Themes.OCEAN.junction_color in result
        assert table.top_left_junction_char.startswith(Themes.OCEAN.junction_color)

    @pytest.mark.parametrize(
        "style", [style for style in TableStyle if style != TableStyle.RANDOM]
    )
    @pytest.mark.parametrize("with_header", [True, False])
    @pytest.mark.parametrize("with_title", [True, False])
    def test_theme_updates_preserve_preset_style(
        self, style: TableStyle, with_header: bool, with_title: bool
    ) -> None:
        plain = PrettyTable(["name", "count"])
        table = ColorTable(["name", "count"])
        for item in (plain, table):
            item.add_row(["alpha", 7])
            item.set_style(style)
            item.padding_width = 3
            item.left_padding_width = 3
            item.right_padding_width = 3
            item.header = with_header
            if with_title:
                item.title = "Colors and borders"

        table.theme = Themes.OCEAN
        table.theme = Themes.HIGH_CONTRAST
        rendered = table.get_string()
        table.update_theme()
        table.update_theme()

        assert table.get_string() == rendered
        assert re.sub(r"\x1b\[[0-9;]*m", "", rendered) == plain.get_string()
        assert table.padding_width == table.left_padding_width == 3
        assert table.right_padding_width == 3
        assert table.header is with_header

    def test_switch_border_styles(self) -> None:
        table = ColorTable(["name", "count"], theme=Themes.OCEAN)
        table.add_row(["alpha", 7])
        plain = PrettyTable(["name", "count"])
        plain.add_row(["alpha", 7])
        for style in (
            TableStyle.DOUBLE_BORDER,
            TableStyle.SINGLE_BORDER,
            TableStyle.DEFAULT,
        ):
            table.set_style(style)
            plain.set_style(style)
            result = table.get_string()
            assert re.sub(r"\x1b\[[0-9;]*m", "", result) == plain.get_string()
            assert Themes.OCEAN.vertical_color in result

    def test_custom_theme_characters_without_preset(self) -> None:
        theme = Theme(vertical_char="!", horizontal_char="=", junction_char="*")
        table = ColorTable(["a"], theme=theme)
        table.add_row([1])
        assert table.get_string().replace(RESET_CODE, "") == (
            "*===*\n! a !\n*===*\n! 1 !\n*===*"
        )

    @pytest.mark.parametrize("theme_first", [True, False])
    def test_preset_characters_override_custom_theme_characters(
        self, theme_first: bool
    ) -> None:
        theme = Theme(
            vertical_char="!",
            horizontal_char="=",
            junction_char="*",
            vertical_color="31",
            horizontal_color="32",
            junction_color="33",
        )
        table = ColorTable(["a"])
        table.add_row([1])
        if theme_first:
            table.theme = theme
            table.set_style(TableStyle.DOUBLE_BORDER)
        else:
            table.set_style(TableStyle.DOUBLE_BORDER)
            table.theme = theme
        plain = PrettyTable(["a"])
        plain.add_row([1])
        plain.set_style(TableStyle.DOUBLE_BORDER)

        result = table.get_string()
        assert re.sub(r"\x1b\[[0-9;]*m", "", result) == plain.get_string()
        assert theme.vertical_color in result

    @pytest.mark.parametrize("theme", [Themes.DEFAULT, Themes.OCEAN])
    @pytest.mark.parametrize("theme_first", [True, False])
    @pytest.mark.parametrize("align", ["l", "c", "r"])
    @pytest.mark.parametrize("width", range(4))
    def test_markdown_header_with_narrow_columns(
        self,
        theme: Theme,
        theme_first: bool,
        align: Literal["l", "c", "r"],
        width: int,
    ) -> None:
        field = "x" * width
        plain = PrettyTable([field])
        table = ColorTable([field])
        for item in (plain, table):
            item.add_row(["y" * width])
        if theme_first:
            table.theme = theme
            table.set_style(TableStyle.MARKDOWN)
        else:
            table.set_style(TableStyle.MARKDOWN)
            table.theme = theme
        plain.set_style(TableStyle.MARKDOWN)
        for item in (plain, table):
            item.align = align
            item.padding_width = 0
            item.left_padding_width = 0
            item.right_padding_width = 0

        result = re.sub(r"\x1b\[[0-9;]*m", "", table.get_string())
        assert table.header is True
        assert result == plain.get_string()
        assert "\x1b" not in result
        separators = {
            "l": " :-" if width == 3 else " :",
            "c": " : ",
            "r": "-: " if width == 3 else ": ",
        }
        assert result.splitlines()[1] == f"|{separators[align]}|"

    @pytest.mark.parametrize("theme", [Themes.DEFAULT, Themes.OCEAN])
    @pytest.mark.parametrize("align", ["l", "c", "r"])
    @pytest.mark.parametrize("width", range(4))
    def test_markdown_rule_preserves_narrow_glyph_slices(
        self, theme: Theme, align: Literal["l", "c", "r"], width: int
    ) -> None:
        table = ColorTable(["x"], theme=theme)
        table.set_style(TableStyle.MARKDOWN)
        table.align = align
        table.left_padding_width = table.right_padding_width = 0
        # Cover the rule builder's boundary widths before Markdown's renderer
        # applies its minimum centered-column width.
        table._widths = [width]

        result = table._stringify_hrule(table._get_options({}))
        expected = {
            "l": " :-" if width == 3 else " :",
            "c": " : " if width == 3 else ": ",
            "r": "-: " if width == 3 else ": ",
        }
        assert re.sub(r"\x1b\[[0-9;]*m", "", result) == f"|{expected[align]}|"
