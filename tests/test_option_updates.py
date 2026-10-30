from __future__ import annotations

import pytest

from prettytable import PrettyTable


@pytest.mark.parametrize("as_pairs", [False, True])
def test_custom_format_update_overrides_float_format(as_pairs: bool) -> None:
    table = PrettyTable(["value"])
    table.add_row([1.25])
    table.float_format = ".1"
    formats = {"value": lambda field, value: f"custom {value}"}

    table.custom_format.update(formats.items() if as_pairs else formats)

    assert "value" not in table.float_format
    assert "custom 1.25" in table.get_string()


def test_alignment_update_validates_values() -> None:
    table = PrettyTable(["value"])

    with pytest.raises(ValueError, match="Alignment"):
        table.align.update({"value": "invalid"})  # type: ignore[dict-item]

    assert table.align["value"] == "c"


@pytest.mark.parametrize("field", ["value", "self"])
def test_alignment_update_accepts_keywords(field: str) -> None:
    table = PrettyTable([field])
    if field == "self":
        table.align.update(self="l")
    else:
        table.align.update(value="l")
    assert table.align[field] == "l"
