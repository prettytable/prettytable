from __future__ import annotations

import os
import random
from typing import Literal

import pytest
from pytest_lazy_fixtures import lf

from prettytable import HRuleStyle, PrettyTable, TableStyle, VRuleStyle
from prettytable.prettytable import _str_block_width

# these tables don't display well outside of raw dump to a terminal, so they are
# moved to external files, where they may be very easy to visually align, by command:
#
#    $  cat tests/data/*.txt
#
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class TestPositionalJunctions:
    """Verify different cases for positional-junction characters"""

    def test_default(self, city_data: PrettyTable) -> None:
        city_data.set_style(TableStyle.DOUBLE_BORDER)

        assert (
            city_data.get_string().strip()
            == """
╔═══════════╦══════╦════════════╦═════════════════╗
║ City name ║ Area ║ Population ║ Annual Rainfall ║
╠═══════════╬══════╬════════════╬═════════════════╣
║  Adelaide ║ 1295 ║  1158259   ║      600.5      ║
║  Brisbane ║ 5905 ║  1857594   ║      1146.4     ║
║   Darwin  ║ 112  ║   120900   ║      1714.7     ║
║   Hobart  ║ 1357 ║   205556   ║      619.5      ║
║   Sydney  ║ 2058 ║  4336374   ║      1214.8     ║
║ Melbourne ║ 1566 ║  3806092   ║      646.9      ║
║   Perth   ║ 5386 ║  1554769   ║      869.4      ║
╚═══════════╩══════╩════════════╩═════════════════╝""".strip()
        )

    def test_no_header(self, city_data: PrettyTable) -> None:
        city_data.set_style(TableStyle.DOUBLE_BORDER)
        city_data.header = False

        assert (
            city_data.get_string().strip()
            == """
╔═══════════╦══════╦═════════╦════════╗
║  Adelaide ║ 1295 ║ 1158259 ║ 600.5  ║
║  Brisbane ║ 5905 ║ 1857594 ║ 1146.4 ║
║   Darwin  ║ 112  ║  120900 ║ 1714.7 ║
║   Hobart  ║ 1357 ║  205556 ║ 619.5  ║
║   Sydney  ║ 2058 ║ 4336374 ║ 1214.8 ║
║ Melbourne ║ 1566 ║ 3806092 ║ 646.9  ║
║   Perth   ║ 5386 ║ 1554769 ║ 869.4  ║
╚═══════════╩══════╩═════════╩════════╝""".strip()
        )

    def test_with_title(self, city_data: PrettyTable) -> None:
        city_data.set_style(TableStyle.DOUBLE_BORDER)
        city_data.title = "Title"

        assert (
            city_data.get_string().strip()
            == """
╔═════════════════════════════════════════════════╗
║                      Title                      ║
╠═══════════╦══════╦════════════╦═════════════════╣
║ City name ║ Area ║ Population ║ Annual Rainfall ║
╠═══════════╬══════╬════════════╬═════════════════╣
║  Adelaide ║ 1295 ║  1158259   ║      600.5      ║
║  Brisbane ║ 5905 ║  1857594   ║      1146.4     ║
║   Darwin  ║ 112  ║   120900   ║      1714.7     ║
║   Hobart  ║ 1357 ║   205556   ║      619.5      ║
║   Sydney  ║ 2058 ║  4336374   ║      1214.8     ║
║ Melbourne ║ 1566 ║  3806092   ║      646.9      ║
║   Perth   ║ 5386 ║  1554769   ║      869.4      ║
╚═══════════╩══════╩════════════╩═════════════════╝""".strip()
        )

    def test_with_title_no_header(self, city_data: PrettyTable) -> None:
        city_data.set_style(TableStyle.DOUBLE_BORDER)
        city_data.title = "Title"
        city_data.header = False
        assert (
            city_data.get_string().strip()
            == """
╔═════════════════════════════════════╗
║                Title                ║
╠═══════════╦══════╦═════════╦════════╣
║  Adelaide ║ 1295 ║ 1158259 ║ 600.5  ║
║  Brisbane ║ 5905 ║ 1857594 ║ 1146.4 ║
║   Darwin  ║ 112  ║  120900 ║ 1714.7 ║
║   Hobart  ║ 1357 ║  205556 ║ 619.5  ║
║   Sydney  ║ 2058 ║ 4336374 ║ 1214.8 ║
║ Melbourne ║ 1566 ║ 3806092 ║ 646.9  ║
║   Perth   ║ 5386 ║ 1554769 ║ 869.4  ║
╚═══════════╩══════╩═════════╩════════╝""".strip()
        )

    def test_hrule_all(self, city_data: PrettyTable) -> None:
        city_data.set_style(TableStyle.DOUBLE_BORDER)
        city_data.title = "Title"
        city_data.hrules = HRuleStyle.ALL
        assert (
            city_data.get_string().strip()
            == """
╔═════════════════════════════════════════════════╗
║                      Title                      ║
╠═══════════╦══════╦════════════╦═════════════════╣
║ City name ║ Area ║ Population ║ Annual Rainfall ║
╠═══════════╬══════╬════════════╬═════════════════╣
║  Adelaide ║ 1295 ║  1158259   ║      600.5      ║
╠═══════════╬══════╬════════════╬═════════════════╣
║  Brisbane ║ 5905 ║  1857594   ║      1146.4     ║
╠═══════════╬══════╬════════════╬═════════════════╣
║   Darwin  ║ 112  ║   120900   ║      1714.7     ║
╠═══════════╬══════╬════════════╬═════════════════╣
║   Hobart  ║ 1357 ║   205556   ║      619.5      ║
╠═══════════╬══════╬════════════╬═════════════════╣
║   Sydney  ║ 2058 ║  4336374   ║      1214.8     ║
╠═══════════╬══════╬════════════╬═════════════════╣
║ Melbourne ║ 1566 ║  3806092   ║      646.9      ║
╠═══════════╬══════╬════════════╬═════════════════╣
║   Perth   ║ 5386 ║  1554769   ║      869.4      ║
╚═══════════╩══════╩════════════╩═════════════════╝""".strip()
        )

    def test_vrules_none(self, city_data: PrettyTable) -> None:
        city_data.set_style(TableStyle.DOUBLE_BORDER)
        city_data.vrules = VRuleStyle.NONE
        assert (
            city_data.get_string().strip()
            == "═══════════════════════════════════════════════════\n"
            "  City name   Area   Population   Annual Rainfall  \n"
            "═══════════════════════════════════════════════════\n"
            "   Adelaide   1295    1158259          600.5       \n"
            "   Brisbane   5905    1857594          1146.4      \n"
            "    Darwin    112      120900          1714.7      \n"
            "    Hobart    1357     205556          619.5       \n"
            "    Sydney    2058    4336374          1214.8      \n"
            "  Melbourne   1566    3806092          646.9       \n"
            "    Perth     5386    1554769          869.4       \n"
            "═══════════════════════════════════════════════════".strip()
        )

    def test_vrules_frame_with_title(self, city_data: PrettyTable) -> None:
        city_data.set_style(TableStyle.DOUBLE_BORDER)
        city_data.vrules = VRuleStyle.FRAME
        city_data.title = "Title"
        assert (
            city_data.get_string().strip()
            == """
╔═════════════════════════════════════════════════╗
║                      Title                      ║
╠═════════════════════════════════════════════════╣
║ City name   Area   Population   Annual Rainfall ║
╠═════════════════════════════════════════════════╣
║  Adelaide   1295    1158259          600.5      ║
║  Brisbane   5905    1857594          1146.4     ║
║   Darwin    112      120900          1714.7     ║
║   Hobart    1357     205556          619.5      ║
║   Sydney    2058    4336374          1214.8     ║
║ Melbourne   1566    3806092          646.9      ║
║   Perth     5386    1554769          869.4      ║
╚═════════════════════════════════════════════════╝""".strip()
        )


class TestStyle:
    @pytest.mark.parametrize(
        "style, expected",
        [
            pytest.param(
                TableStyle.DEFAULT,
                """
+---------------------------------+
|          Table Caption          |
+---+---------+---------+---------+
|   | Field 1 | Field 2 | Field 3 |
+---+---------+---------+---------+
| 1 | value 1 |  value2 |  value3 |
| 4 | value 4 |  value5 |  value6 |
| 7 | value 7 |  value8 |  value9 |
+---+---------+---------+---------+
""",
                id="DEFAULT",
            ),
            pytest.param(
                TableStyle.MARKDOWN,  # TODO fix
                """
**Table Caption**

|     | Field 1 | Field 2 | Field 3 |
| :-: | :-----: | :-----: | :-----: |
|  1  | value 1 |  value2 |  value3 |
|  4  | value 4 |  value5 |  value6 |
|  7  | value 7 |  value8 |  value9 |
""".strip(),
                id="MARKDOWN",
            ),
            pytest.param(
                TableStyle.MSWORD_FRIENDLY,
                """
+---------------------------------+
|          Table Caption          |
|   | Field 1 | Field 2 | Field 3 |
| 1 | value 1 |  value2 |  value3 |
| 4 | value 4 |  value5 |  value6 |
| 7 | value 7 |  value8 |  value9 |
""",
                id="MSWORD_FRIENDLY",
            ),
            pytest.param(
                TableStyle.ORGMODE,
                """
|---------------------------------|
|          Table Caption          |
|---+---------+---------+---------|
|   | Field 1 | Field 2 | Field 3 |
|---+---------+---------+---------|
| 1 | value 1 |  value2 |  value3 |
| 4 | value 4 |  value5 |  value6 |
| 7 | value 7 |  value8 |  value9 |
|---+---------+---------+---------|
""",
                id="ORGMODE",
            ),
            pytest.param(
                TableStyle.PLAIN_COLUMNS,
                """
Table Caption                           
         Field 1        Field 2        Field 3        
1        value 1         value2         value3        
4        value 4         value5         value6        
7        value 7         value8         value9
""",  # noqa: W291
                id="PLAIN_COLUMNS",
            ),
            pytest.param(
                TableStyle.RANDOM,
                """
'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
%               Table Caption           %
'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
%    1     value 1     value2     value3%
%    4     value 4     value5     value6%
%    7     value 7     value8     value9%
'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
""",
                id="RANDOM",
            ),
            pytest.param(
                TableStyle.DOUBLE_BORDER,
                """
╔═════════════════════════════════╗
║          Table Caption          ║
╠═══╦═════════╦═════════╦═════════╣
║   ║ Field 1 ║ Field 2 ║ Field 3 ║
╠═══╬═════════╬═════════╬═════════╣
║ 1 ║ value 1 ║  value2 ║  value3 ║
║ 4 ║ value 4 ║  value5 ║  value6 ║
║ 7 ║ value 7 ║  value8 ║  value9 ║
╚═══╩═════════╩═════════╩═════════╝
""",
            ),
            pytest.param(
                TableStyle.SINGLE_BORDER,
                """
┌─────────────────────────────────┐
│          Table Caption          │
├───┬─────────┬─────────┬─────────┤
│   │ Field 1 │ Field 2 │ Field 3 │
├───┼─────────┼─────────┼─────────┤
│ 1 │ value 1 │  value2 │  value3 │
│ 4 │ value 4 │  value5 │  value6 │
│ 7 │ value 7 │  value8 │  value9 │
└───┴─────────┴─────────┴─────────┘
""",
            ),
        ],
    )
    def test_style(
        self, helper_table: PrettyTable, style: TableStyle, expected: str
    ) -> None:
        random.seed(1234)
        helper_table.title = "Table Caption"
        helper_table.set_style(style)
        assert helper_table.get_string().strip() == expected.strip()

    def test_style_invalid(self, helper_table: PrettyTable) -> None:
        # This is an hrule style, not a table style
        with pytest.raises(ValueError):
            helper_table.set_style(HRuleStyle.ALL)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "original_style,style, expected",
        [
            pytest.param(
                TableStyle.MARKDOWN,
                TableStyle.DEFAULT,
                """
+---+---------+---------+---------+
|   | Field 1 | Field 2 | Field 3 |
+---+---------+---------+---------+
| 1 | value 1 |  value2 |  value3 |
| 4 | value 4 |  value5 |  value6 |
| 7 | value 7 |  value8 |  value9 |
+---+---------+---------+---------+
""",
                id="DEFAULT",
            ),
            pytest.param(
                TableStyle.MSWORD_FRIENDLY,
                TableStyle.MARKDOWN,
                """
|     | Field 1 | Field 2 | Field 3 |
| :-: | :-----: | :-----: | :-----: |
|  1  | value 1 |  value2 |  value3 |
|  4  | value 4 |  value5 |  value6 |
|  7  | value 7 |  value8 |  value9 |
""",
                id="MARKDOWN",
            ),
            pytest.param(
                TableStyle.MARKDOWN,
                TableStyle.MSWORD_FRIENDLY,
                """
|   | Field 1 | Field 2 | Field 3 |
| 1 | value 1 |  value2 |  value3 |
| 4 | value 4 |  value5 |  value6 |
| 7 | value 7 |  value8 |  value9 |
""",
                id="MSWORD_FRIENDLY",
            ),
            pytest.param(
                TableStyle.MARKDOWN,
                TableStyle.ORGMODE,
                """
|---+---------+---------+---------|
|   | Field 1 | Field 2 | Field 3 |
|---+---------+---------+---------|
| 1 | value 1 |  value2 |  value3 |
| 4 | value 4 |  value5 |  value6 |
| 7 | value 7 |  value8 |  value9 |
|---+---------+---------+---------|
""",
                id="ORGMODE",
            ),
            pytest.param(
                TableStyle.MARKDOWN,
                TableStyle.PLAIN_COLUMNS,
                """
         Field 1        Field 2        Field 3        
1        value 1         value2         value3        
4        value 4         value5         value6        
7        value 7         value8         value9
""",  # noqa: W291
                id="PLAIN_COLUMNS",
            ),
            pytest.param(
                TableStyle.MARKDOWN,
                TableStyle.RANDOM,
                """
'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
%    1     value 1     value2     value3%
%    4     value 4     value5     value6%
%    7     value 7     value8     value9%
'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
""",
                id="RANDOM",
            ),
            pytest.param(
                TableStyle.MARKDOWN,
                TableStyle.DOUBLE_BORDER,
                """
╔═══╦═════════╦═════════╦═════════╗
║   ║ Field 1 ║ Field 2 ║ Field 3 ║
╠═══╬═════════╬═════════╬═════════╣
║ 1 ║ value 1 ║  value2 ║  value3 ║
║ 4 ║ value 4 ║  value5 ║  value6 ║
║ 7 ║ value 7 ║  value8 ║  value9 ║
╚═══╩═════════╩═════════╩═════════╝
""",
                id="DOUBLE_BORDER",
            ),
            pytest.param(
                TableStyle.MARKDOWN,
                TableStyle.SINGLE_BORDER,
                """
┌───┬─────────┬─────────┬─────────┐
│   │ Field 1 │ Field 2 │ Field 3 │
├───┼─────────┼─────────┼─────────┤
│ 1 │ value 1 │  value2 │  value3 │
│ 4 │ value 4 │  value5 │  value6 │
│ 7 │ value 7 │  value8 │  value9 │
└───┴─────────┴─────────┴─────────┘
""",
                id="SINGLE_BORDER",
            ),
        ],
    )
    def test_style_reset(
        self,
        helper_table: PrettyTable,
        original_style: TableStyle,
        style: TableStyle,
        expected: str,
    ) -> None:
        """
            Testing to ensure that default styling is reset between changes
            of styles on a PrettyTable

        Args:
            style (str): Style to be used (Default, markdown, etc)
            expected (str): The expected format of style as a string representation
        """
        random.seed(1234)
        helper_table.set_style(original_style)
        helper_table.set_style(style)
        assert helper_table.get_string().strip() == expected.strip()

    @pytest.mark.parametrize(
        "style, expected",
        [
            pytest.param(
                TableStyle.MARKDOWN,
                """
| l |  c  | r | Align left | Align centre | Align right |
| :-| :-: |-: | :----------| :----------: |-----------: |
| 1 |  2  | 3 | value 1    |    value2    |      value3 |
| 4 |  5  | 6 | value 4    |    value5    |      value6 |
| 7 |  8  | 9 | value 7    |    value8    |      value9 |
""",
                id="MARKDOWN",
            ),
        ],
    )
    def test_style_align(self, style: TableStyle, expected: str) -> None:
        table = PrettyTable(
            ["l", "c", "r", "Align left", "Align centre", "Align right"]
        )
        v = 1
        for row in range(3):
            # Some have spaces, some not, to help test padding columns of
            # different widths
            table.add_row(
                [v, v + 1, v + 2, f"value {v}", f"value{v + 1}", f"value{v + 2}"]
            )
            v += 3

        table.set_style(style)
        table.align["l"] = table.align["Align left"] = "l"
        table.align["c"] = table.align["Align centre"] = "c"
        table.align["r"] = table.align["Align right"] = "r"
        assert table.get_string().strip() == expected.strip()


@pytest.fixture
def japanese_pretty_table() -> PrettyTable:
    table = PrettyTable(["Kanji", "Hiragana", "English"])
    table.add_row(["神戸", "こうべ", "Kobe"])
    table.add_row(["京都", "きょうと", "Kyoto"])
    table.add_row(["長崎", "ながさき", "Nagasaki"])
    table.add_row(["名古屋", "なごや", "Nagoya"])
    table.add_row(["大阪", "おおさか", "Osaka"])
    table.add_row(["札幌", "さっぽろ", "Sapporo"])
    table.add_row(["東京", "とうきょう", "Tokyo"])
    table.add_row(["横浜", "よこはま", "Yokohama"])
    return table


@pytest.fixture
def emoji_pretty_table() -> PrettyTable:
    thunder1 = [
        '\033[38;5;226m _`/""\033[38;5;250m.-.    \033[0m',
        "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
        "\033[38;5;228;5m    ⚡\033[38;5;111;25mʻ ʻ\033[38;5;228;5m"
        "⚡\033[38;5;111;25mʻ ʻ \033[0m",
        "\033[38;5;111m    ʻ ʻ ʻ ʻ  \033[0m",
    ]
    thunder2 = [
        "\033[38;5;240;1m     .-.     \033[0m",
        "\033[38;5;240;1m    (   ).   \033[0m",
        "\033[38;5;240;1m   (___(__)  \033[0m",
        "\033[38;5;21;1m  ‚ʻ\033[38;5;228;5m⚡\033[38;5;21;25mʻ‚\033[38;5;228;5m"
        "⚡\033[38;5;21;25m‚ʻ   \033[0m",
        "\033[38;5;21;1m  ‚ʻ‚ʻ\033[38;5;228;5m⚡\033[38;5;21;25mʻ‚ʻ   \033[0m",
    ]
    table = PrettyTable(["Thunderbolt", "Lightning"])
    for i, t1 in enumerate(thunder1):
        table.add_row([t1, thunder2[i]])
    return table


class TestMultiPattern:
    @pytest.mark.parametrize(
        ["pt", "expected_output", "test_type"],
        [
            (
                lf("city_data"),
                """
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
|  Adelaide | 1295 |  1158259   |      600.5      |
|  Brisbane | 5905 |  1857594   |      1146.4     |
|   Darwin  | 112  |   120900   |      1714.7     |
|   Hobart  | 1357 |   205556   |      619.5      |
|   Sydney  | 2058 |  4336374   |      1214.8     |
| Melbourne | 1566 |  3806092   |      646.9      |
|   Perth   | 5386 |  1554769   |      869.4      |
+-----------+------+------------+-----------------+
""",
                "English Table",
            ),
            (
                lf("japanese_pretty_table"),
                """
+--------+------------+----------+
| Kanji  |  Hiragana  | English  |
+--------+------------+----------+
|  神戸  |   こうべ   |   Kobe   |
|  京都  |  きょうと  |  Kyoto   |
|  長崎  |  ながさき  | Nagasaki |
| 名古屋 |   なごや   |  Nagoya  |
|  大阪  |  おおさか  |  Osaka   |
|  札幌  |  さっぽろ  | Sapporo  |
|  東京  | とうきょう |  Tokyo   |
|  横浜  |  よこはま  | Yokohama |
+--------+------------+----------+

""",
                "Japanese table",
            ),
            (
                lf("emoji_pretty_table"),
                """
+-----------------+-----------------+
|   Thunderbolt   |    Lightning    |
+-----------------+-----------------+
|  \x1b[38;5;226m _`/""\x1b[38;5;250m.-.    \x1b[0m  |  \x1b[38;5;240;1m     .-.     \x1b[0m  |
|  \x1b[38;5;226m  ,\\_\x1b[38;5;250m(   ).  \x1b[0m  |  \x1b[38;5;240;1m    (   ).   \x1b[0m  |
|  \x1b[38;5;226m   /\x1b[38;5;250m(___(__) \x1b[0m  |  \x1b[38;5;240;1m   (___(__)  \x1b[0m  |
| \x1b[38;5;228;5m    ⚡\x1b[38;5;111;25mʻ ʻ\x1b[38;5;228;5m⚡\x1b[38;5;111;25mʻ ʻ \x1b[0m | \x1b[38;5;21;1m  ‚ʻ\x1b[38;5;228;5m⚡\x1b[38;5;21;25mʻ‚\x1b[38;5;228;5m⚡\x1b[38;5;21;25m‚ʻ   \x1b[0m |
|  \x1b[38;5;111m    ʻ ʻ ʻ ʻ  \x1b[0m  |  \x1b[38;5;21;1m  ‚ʻ‚ʻ\x1b[38;5;228;5m⚡\x1b[38;5;21;25mʻ‚ʻ   \x1b[0m |
+-----------------+-----------------+
            """,
                "Emoji table",
            ),
        ],
    )
    def test_multi_pattern_outputs(
        self, pt: PrettyTable, expected_output: str, test_type: str
    ) -> None:
        assert (
            pt.get_string().strip() == expected_output.strip()
        ), f"Error output for test output of type {test_type}"


def test_colored_table() -> None:
    table = PrettyTable(field_names=["Namespace", "Count"])
    table.title = "\x1b[34mHere be Table caption\x1b[39m"
    assert (
        table.get_string()
        == """+-----------------------+
| \x1b[34mHere be Table caption\x1b[39m |
+-------------+---------+
|  Namespace  |  Count  |
+-------------+---------+
+-------------+---------+"""
    )


def test_link_and_color() -> None:
    table = PrettyTable(["Link", "Count"])
    # Add link
    text = "Click here"
    table.add_row([f"\033]8;;https://example.com\033\\{text}\033]8;;\033\\", "1"])
    table.add_row(["No link", "2"])
    # Add link with colour
    text = "Click \x1b[34mhere\x1b[39m"
    table.add_row([f"\033]8;;https://example.com\033\\{text}\033]8;;\033\\", "3"])

    assert (
        table.get_string()
        == """\
+------------+-------+
|    Link    | Count |
+------------+-------+
| \033]8;;https://example.com\033\\Click here\033]8;;\033\\ |   1   |
|  No link   |   2   |
| \033]8;;https://example.com\033\\Click \x1b[34mhere\x1b[39m\033]8;;\033\\ |   3   |
+------------+-------+"""
    )


@pytest.mark.parametrize(
    ["test_input", "expected"],
    [
        ("a", 1),
        ("abc", 3),
        ("abc def", 7),
        ("\x1b[34mblue\x1b[39m", 4),
        ("\033]8;;https://example.com\033\\link\033]8;;\033\\", 4),
        # colour inside link
        ("\033]8;;https://example.com\033\\\x1b[34mblue link\x1b[39m\033]8;;\033\\", 9),
        # link inside colour
        ("\x1b[34m\033]8;;https://example.com\033\\blue link\033]8;;\033\\\x1b[39m", 9),
        # 中文 CJK wide characters
        ("\u4e2d\u6587", 4),
        # café (combining acute accent)
        ("cafe\u0301", 4),
        # 👨‍👩‍👧 ZWJ family
        ("\U0001f468\u200d\U0001f469\u200d\U0001f467", 2),
        # ☺️ VS16 emoji
        ("\u263a\ufe0f", 2),
        # 🇺🇸 regional flag
        ("\U0001f1fa\U0001f1f8", 2),
        # control code (bell)
        ("abc\x07def", 6),
    ],
)
def test__str_block_width(test_input: str, expected: int) -> None:
    assert _str_block_width(test_input) == expected


@pytest.mark.parametrize(
    ["fields", "rows", "expected_file"],
    [
        (
            ["Emoji", "Name"],
            [
                ["\U0001f468\u200d\U0001f469\u200d\U0001f467", "Family"],
                ["\U0001f1fa\U0001f1f8", "USA"],
                ["Hi", "Text"],
            ],
            "table_complex_emoji.txt",
        ),
        (
            ["Word", "Lang"],
            [["cafe\u0301", "FR"], ["cafe", "EN"]],
            "table_combining_chars.txt",
        ),
        (
            ["CJK", "Width"],
            [["\u4e2d\u6587", "4"], ["Test", "4"]],
            "table_cjk.txt",
        ),
        (
            ["Status", "Count"],
            [
                ["\x1b[32mOK\x1b[0m", "10"],
                ["\x1b[31mFailed\x1b[0m", "2"],
                ["Normal", "5"],
            ],
            "table_ansi_colors.txt",
        ),
    ],
)
def test_table_unicode_width(
    fields: list[str],
    rows: list[list[str]],
    expected_file: str,
) -> None:
    table = PrettyTable(fields)
    for row in rows:
        table.add_row(row)
    with open(os.path.join(DATA_DIR, expected_file), encoding="utf-8") as fin:
        expected_from_file = fin.read()
    assert table.get_string().rstrip() == expected_from_file.rstrip()


@pytest.mark.parametrize(
    ["align", "expected_file"],
    [
        ("l", "table_align_left.txt"),
        ("r", "table_align_right.txt"),
        ("c", "table_align_center.txt"),
    ],
)
def test_table_alignment_with_emoji(
    align: Literal["l", "c", "r"], expected_file: str
) -> None:
    table = PrettyTable(["Name"])
    table.align["Name"] = align
    table.add_row(["\U0001f468\u200d\U0001f469\u200d\U0001f467"])  # 👨‍👩‍👧
    table.add_row(["Hi"])
    with open(os.path.join(DATA_DIR, expected_file), encoding="utf-8") as fin:
        expected_from_file = fin.read()
    assert table.get_string().rstrip() == expected_from_file.strip()
