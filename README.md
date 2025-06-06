# PrettyTable

[![PyPI version](https://img.shields.io/pypi/v/prettytable.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/prettytable/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/prettytable.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/prettytable/)
[![PyPI downloads](https://img.shields.io/pypi/dm/prettytable.svg)](https://pypistats.org/packages/prettytable)
[![GitHub Actions status](https://github.com/prettytable/prettytable/workflows/Test/badge.svg)](https://github.com/prettytable/prettytable/actions)
[![Codecov](https://codecov.io/gh/prettytable/prettytable/branch/main/graph/badge.svg)](https://codecov.io/gh/prettytable/prettytable)
[![Licence](https://img.shields.io/github/license/prettytable/prettytable.svg)](LICENSE)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)
[![Tidelift](https://tidelift.com/badges/package/pypi/prettytable)](https://tidelift.com/subscription/pkg/pypi-prettytable?utm_source=pypi-prettytable&utm_medium=badge)

PrettyTable lets you print tables in an attractive ASCII form:

```
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
| Adelaide  | 1295 |  1158259   |      600.5      |
| Brisbane  | 5905 |  1857594   |      1146.4     |
| Darwin    | 112  |   120900   |      1714.7     |
| Hobart    | 1357 |   205556   |      619.5      |
| Melbourne | 1566 |  3806092   |      646.9      |
| Perth     | 5386 |  1554769   |      869.4      |
| Sydney    | 2058 |  4336374   |      1214.8     |
+-----------+------+------------+-----------------+
```

## Installation

Install via pip:

    python -m pip install -U prettytable

Install latest development version:

    python -m pip install -U git+https://github.com/prettytable/prettytable

Or from `requirements.txt`:

    -e git://github.com/prettytable/prettytable.git#egg=prettytable

## Demo

To see demo output, run:

```bash
python3 -m prettytable
```

## Tutorial on how to use the PrettyTable API

### Getting your data into (and out of) the table

Let's suppose you have a shiny new PrettyTable:

```python
from prettytable import PrettyTable
table = PrettyTable()
```

and you want to put some data into it. You have a few options.

#### Row by row

You can add data one row at a time. To do this you can set the field names first using
the `field_names` attribute, and then add the rows one at a time using the `add_row`
method:

```python
table.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
table.add_row(["Adelaide", 1295, 1158259, 600.5])
table.add_row(["Brisbane", 5905, 1857594, 1146.4])
table.add_row(["Darwin", 112, 120900, 1714.7])
table.add_row(["Hobart", 1357, 205556, 619.5])
table.add_row(["Sydney", 2058, 4336374, 1214.8])
table.add_row(["Melbourne", 1566, 3806092, 646.9])
table.add_row(["Perth", 5386, 1554769, 869.4])
```

#### All rows at once

When you have a list of rows, you can add them in one go with `add_rows`:

```python
table.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
table.add_rows(
    [
        ["Adelaide", 1295, 1158259, 600.5],
        ["Brisbane", 5905, 1857594, 1146.4],
        ["Darwin", 112, 120900, 1714.7],
        ["Hobart", 1357, 205556, 619.5],
        ["Sydney", 2058, 4336374, 1214.8],
        ["Melbourne", 1566, 3806092, 646.9],
        ["Perth", 5386, 1554769, 869.4],
    ]
)
```

#### Column by column

You can add data one column at a time as well. To do this you use the `add_column`
method, which takes two arguments - a string which is the name for the field the column
you are adding corresponds to, and a list or tuple which contains the column data:

```python
table.add_column("City name",
["Adelaide","Brisbane","Darwin","Hobart","Sydney","Melbourne","Perth"])
table.add_column("Area", [1295, 5905, 112, 1357, 2058, 1566, 5386])
table.add_column("Population", [1158259, 1857594, 120900, 205556, 4336374, 3806092,
1554769])
table.add_column("Annual Rainfall",[600.5, 1146.4, 1714.7, 619.5, 1214.8, 646.9,
869.4])
```

#### Mixing and matching

If you really want to, you can even mix and match `add_row` and `add_column` and build
some of your table in one way and some of it in the other. Tables built this way are
kind of confusing for other people to read, though, so don't do this unless you have a
good reason.

#### Importing data from a CSV file

If you have your table data in a comma-separated values file (.csv), you can read this
data into a PrettyTable like this:

```python
from prettytable import from_csv
with open("myfile.csv") as fp:
    mytable = from_csv(fp)
```

#### Importing data from a database cursor

If you have your table data in a database which you can access using a library which
confirms to the Python DB-API (e.g. an SQLite database accessible using the `sqlite`
module), then you can build a PrettyTable using a cursor object, like this:

```python
import sqlite3
from prettytable import from_db_cursor

connection = sqlite3.connect("mydb.db")
cursor = connection.cursor()
cursor.execute("SELECT field1, field2, field3 FROM my_table")
mytable = from_db_cursor(cursor)
```

#### Getting data out

There are three ways to get data out of a PrettyTable, in increasing order of
completeness:

- The `del_row` method takes an integer index of a single row to delete.
- The `del_column` method takes a field name of a single column to delete.
- The `clear_rows` method takes no arguments and deletes all the rows in the table - but
  keeps the field names as they were so you that you can repopulate it with the same
  kind of data.
- The `clear` method takes no arguments and deletes all rows and all field names. It's
  not quite the same as creating a fresh table instance, though - style related
  settings, discussed later, are maintained.

### Displaying your table in ASCII form

PrettyTable's main goal is to let you print tables in an attractive ASCII form, like
this:

```
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
| Adelaide  | 1295 |  1158259   |      600.5      |
| Brisbane  | 5905 |  1857594   |      1146.4     |
| Darwin    | 112  |   120900   |      1714.7     |
| Hobart    | 1357 |   205556   |      619.5      |
| Melbourne | 1566 |  3806092   |      646.9      |
| Perth     | 5386 |  1554769   |      869.4      |
| Sydney    | 2058 |  4336374   |      1214.8     |
+-----------+------+------------+-----------------+
```

You can print tables like this to `stdout` or get string representations of them.

#### Printing

To print a table in ASCII form, you can just do this:

```python
print(table)
```

The old `table.printt()` method from versions 0.5 and earlier has been removed.

To pass options changing the look of the table, use the `get_string()` method documented
below:

```python
print(table.get_string())
```

#### Stringing

If you don't want to actually print your table in ASCII form but just get a string
containing what _would_ be printed if you use `print(table)`, you can use the
`get_string` method:

```python
mystring = table.get_string()
```

This string is guaranteed to look exactly the same as what would be printed by doing
`print(table)`. You can now do all the usual things you can do with a string, like write
your table to a file or insert it into a GUI.

The table can be displayed in several different formats using `get_formatted_string` by
changing the `out_format=<text|html|json|csv|latex|mediawiki>`. This function passes
through arguments to the functions that render the table, so additional arguments can be
given. This provides a way to let a user choose the output formatting.

```python
def my_cli_function(table_format: str = 'text'):
  ...
  print(table.get_formatted_string(table_format))
```

#### Controlling which data gets displayed

If you like, you can restrict the output of `print(table)` or `table.get_string` to only
the fields or rows you like.

The `fields` argument to these methods takes a list of field names to be printed:

```python
print(table.get_string(fields=["City name", "Population"]))
```

gives:

```
+-----------+------------+
| City name | Population |
+-----------+------------+
| Adelaide  |  1158259   |
| Brisbane  |  1857594   |
| Darwin    |   120900   |
| Hobart    |   205556   |
| Melbourne |  3806092   |
| Perth     |  1554769   |
| Sydney    |  4336374   |
+-----------+------------+
```

The `start` and `end` arguments take the index of the first and last row to print
respectively. Note that the indexing works like Python list slicing - to print the 2nd,
3rd and 4th rows of the table, set `start` to 1 (the first row is row 0, so the second
is row 1) and set `end` to 4 (the index of the 4th row, plus 1):

```python
print(table.get_string(start=1, end=4))
```

prints:

```
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
| Brisbane  | 5905 |    1857594 | 1146.4          |
| Darwin    | 112  |     120900 | 1714.7          |
| Hobart    | 1357 |     205556 | 619.5           |
+-----------+------+------------+-----------------+
```

#### Filtering your table

You can make sure that your tables are filtered by giving `get_string` a `row_filter`
keyword argument, which must be a function with one argument `row` returning a Boolean
value. The `row` is the list of fields in a row.

For example, to print the example table we built earlier of Australian capital city
data, so that cities with a population of at least 1,000,000, we can do this:

```python
def filter_function(row: list[str]) -> bool:
    return row[2] > 999999

print(table.get_string(row_filter=filter_function))
```

to get:

```
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
|  Adelaide | 1295 |  1158259   |      600.5      |
|  Brisbane | 5905 |  1857594   |      1146.4     |
|   Sydney  | 2058 |  4336374   |      1214.8     |
| Melbourne | 1566 |  3806092   |      646.9      |
|   Perth   | 5386 |  1554769   |      869.4      |
+-----------+------+------------+-----------------+
```

#### Changing the alignment of columns

By default, all columns in a table are centre aligned.

##### All columns at once

You can change the alignment of all the columns in a table at once by assigning a one
character string to the `align` attribute. The allowed strings are `"l"`, `"r"` and
`"c"` for left, right and centre alignment, respectively:

```python
table.align = "r"
print(table)
```

gives:

```
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
|  Adelaide | 1295 |    1158259 |           600.5 |
|  Brisbane | 5905 |    1857594 |          1146.4 |
|    Darwin |  112 |     120900 |          1714.7 |
|    Hobart | 1357 |     205556 |           619.5 |
| Melbourne | 1566 |    3806092 |           646.9 |
|     Perth | 5386 |    1554769 |           869.4 |
|    Sydney | 2058 |    4336374 |          1214.8 |
+-----------+------+------------+-----------------+
```

##### One column at a time

You can also change the alignment of individual columns based on the corresponding field
name by treating the `align` attribute as if it were a dictionary.

```python
table.align["City name"] = "l"
table.align["Area"] = "c"
table.align["Population"] = "r"
table.align["Annual Rainfall"] = "c"
print(table)
```

gives:

```
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
| Adelaide  | 1295 |    1158259 |      600.5      |
| Brisbane  | 5905 |    1857594 |      1146.4     |
| Darwin    | 112  |     120900 |      1714.7     |
| Hobart    | 1357 |     205556 |      619.5      |
| Melbourne | 1566 |    3806092 |      646.9      |
| Perth     | 5386 |    1554769 |      869.4      |
| Sydney    | 2058 |    4336374 |      1214.8     |
+-----------+------+------------+-----------------+
```

##### Sorting your table by a field

You can make sure that your ASCII tables are produced with the data sorted by one
particular field by giving `get_string` a `sortby` keyword argument, which must be a
string containing the name of one field.

For example, to print the example table we built earlier of Australian capital city
data, so that the most populated city comes last, we can do this:

```python
print(table.get_string(sortby="Population"))
```

to get:

```
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
| Darwin    | 112  |   120900   |      1714.7     |
| Hobart    | 1357 |   205556   |      619.5      |
| Adelaide  | 1295 |  1158259   |      600.5      |
| Perth     | 5386 |  1554769   |      869.4      |
| Brisbane  | 5905 |  1857594   |      1146.4     |
| Melbourne | 1566 |  3806092   |      646.9      |
| Sydney    | 2058 |  4336374   |      1214.8     |
+-----------+------+------------+-----------------+
```

If we want the most populated city to come _first_, we can also give a
`reversesort=True` argument.

If you _always_ want your tables to be sorted in a certain way, you can make the setting
long-term like this:

```python
table.sortby = "Population"
print(table)
print(table)
print(table)
```

All three tables printed by this code will be sorted by population (you could do
`table.reversesort = True` as well, if you wanted). The behaviour will persist until you
turn it off:

```python
table.sortby = None
```

If you want to specify a custom sorting function, you can use the `sort_key` keyword
argument as Pythons `sorted()` `key` parameter. The value of the `sort_key` parameter
should be a function (or other callable) that takes a single argument and returns a key
to use for sorting purposes.

If your table has n columns, each list will have n+1 elements. Each list corresponds to
one row of the table. The first element will be whatever data is in the relevant row, in
the column specified by the `sort_by` argument. The remaining n elements are the data in
each of the table's columns, in order, including a repeated instance of the data in the
`sort_by` column.

#### Adding sections to a table

You can divide your table into different sections using the `add_divider` method or
`divider` argument to `add_row()` or even to `add_rows()`. This will add a dividing line
into the table under the row who has this field set. So we can set up a table like this:

```python
table = PrettyTable()
table.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
table.add_row(["Adelaide", 1295, 1158259, 600.5])
table.add_divider()
table.add_row(["Brisbane", 5905, 1857594, 1146.4], divider=True)
table.add_rows(
    [["Darwin", 112, 120900, 1714.7],
     ["Hobart", 1357, 205556, 619.5]],
    divider=True
)
table.add_row(["Melbourne", 1566, 3806092, 646.9])
table.add_row(["Perth", 5386, 1554769, 869.4])
table.add_row(["Sydney", 2058, 4336374, 1214.8])
```

to get a table like this:

```
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
|  Adelaide | 1295 |  1158259   |      600.5      |
+-----------+------+------------+-----------------+
|  Brisbane | 5905 |  1857594   |      1146.4     |
+-----------+------+------------+-----------------+
|   Darwin  | 112  |   120900   |      1714.7     |
|   Hobart  | 1357 |   205556   |      619.5      |
+-----------+------+------------+-----------------+
| Melbourne | 1566 |  3806092   |      646.9      |
|   Perth   | 5386 |  1554769   |      869.4      |
|   Sydney  | 2058 |  4336374   |      1214.8     |
+-----------+------+------------+-----------------+
```

Any added dividers will be removed if a table is sorted.

### Changing the appearance of your table - the easy way

By default, PrettyTable produces ASCII tables that look like the ones used in SQL
database shells. But it can print them in a variety of other formats as well. If the
format you want to use is common, PrettyTable makes this easy for you to do using the
`set_style` method. If you want to produce an uncommon table, you'll have to do things
slightly harder (see later).

#### Setting a table style

You can set the style for your table using the `set_style` method before any calls to
`print` or `get_string`. Here's how to print a table in Markdown format:

```python
from prettytable import TableStyle

table.set_style(TableStyle.MARKDOWN)
print(table)
```

In addition to `MARKDOWN` you can use these in-built styles:

- `DEFAULT` - The default look, used to undo any style changes you may have made
- `PLAIN_COLUMNS` - A borderless style that works well with command line programs for
  columnar data
- `MSWORD_FRIENDLY` - A format which works nicely with Microsoft Word's "Convert to
  table" feature
- `ORGMODE` - A table style that fits [Org mode](https://orgmode.org/) syntax
- `SINGLE_BORDER` and `DOUBLE_BORDER` - Styles that use continuous single/double border
  lines with Box drawing characters for a fancier display on terminal

Other styles are likely to appear in future releases.

### Changing the appearance of your table - the hard way

If you want to display your table in a style other than one of the in-built styles
listed above, you'll have to set things up the hard way.

Don't worry, it's not really that hard!

#### Style options

PrettyTable has a number of style options which control various aspects of how tables
are displayed. You have the freedom to set each of these options individually to
whatever you prefer. The `set_style` method just does this automatically for you.

The options are:

| Option                       | Details                                                                                                                                                                                          |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `border`                     | A Boolean option (must be `True` or `False`). Controls whether a border is drawn inside and around the table.                                                                                    |
| `preserve_internal_border`   | A Boolean option (must be `True` or `False`). Controls whether borders are still drawn within the table even when `border=False`.                                                                |
| `header`                     | A Boolean option (must be `True` or `False`). Controls whether the first row of the table is a header showing the names of all the fields.                                                       |
| `hrules`                     | Controls printing of horizontal rules after rows. Allowed values: `FRAME`, `HEADER`, `ALL`, `NONE`.                                                                                              |
| `HEADER`, `ALL`, `NONE`      | These are variables defined inside the `prettytable` module so make sure you import them or use `prettytable.FRAME` etc.                                                                         |
| `vrules`                     | Controls printing of vertical rules between columns. Allowed values: `FRAME`, `ALL`, `NONE`.                                                                                                     |
| `int_format`                 | A string which controls the way integer data is printed. This works like: `print("%<int_format>d" % data)`.                                                                                      |
| `float_format`               | A string which controls the way floating point data is printed. This works like: `print("%<float_format>f" % data)`.                                                                             |
| `custom_format`              | A dictionary of field and callable. This allows you to set any format you want `pf.custom_format["my_col_int"] = lambda f, v: f"{v:,}"`. The type of the callable is `Callable[[str, Any], str]` |
| `padding_width`              | Number of spaces on either side of column data (only used if left and right paddings are `None`).                                                                                                |
| `left_padding_width`         | Number of spaces on left-hand side of column data.                                                                                                                                               |
| `right_padding_width`        | Number of spaces on right-hand side of column data.                                                                                                                                              |
| `vertical_char`              | Single character string used to draw vertical lines. Default: `\|`.                                                                                                                              |
| `horizontal_char`            | Single character string used to draw horizontal lines. Default: `-`.                                                                                                                             |
| `_horizontal_align_char`     | Single character string used to indicate column alignment in horizontal lines. Default: `:` for Markdown, otherwise `None`.                                                                      |
| `junction_char`              | Single character string used to draw line junctions. Default: `+`.                                                                                                                               |
| `top_junction_char`          | Single character string used to draw top line junctions. Default: `junction_char`.                                                                                                               |
| `bottom_junction_char`       | single character string used to draw bottom line junctions. Default: `junction_char`.                                                                                                            |
| `right_junction_char`        | Single character string used to draw right line junctions. Default: `junction_char`.                                                                                                             |
| `left_junction_char`         | Single character string used to draw left line junctions. Default: `junction_char`.                                                                                                              |
| `top_right_junction_char`    | Single character string used to draw top-right line junctions. Default: `junction_char`.                                                                                                         |
| `top_left_junction_char`     | Single character string used to draw top-left line junctions. Default: `junction_char`.                                                                                                          |
| `bottom_right_junction_char` | Single character string used to draw bottom-right line junctions. Default: `junction_char`.                                                                                                      |
| `bottom_left_junction_char`  | Single character string used to draw bottom-left line junctions. Default: `junction_char`.                                                                                                       |
| `min_table_width`            | Number of characters used for the minimum total table width.                                                                                                                                     |
| `max_table_width`            | Number of characters used for the maximum total table width.                                                                                                                                     |
| `max_width`                  | Number of characters used for maximum width of a column.                                                                                                                                         |
| `min_width`                  | Number of characters used for minimum width of a column.                                                                                                                                         |
| `use_header_width`           | A Boolean option (must be `True` or `False`). Controls whether the width of the header is used for computing column width. Default: `True`.                                                      |
| `break_on_hyphens`           | Whether long lines are wrapped on hyphens. Default: `True`.                                                                                                                                      |

You can set the style options to your own settings in two ways:

#### Setting style options for the long term

If you want to print your table with a different style several times, you can set your
option for the long term just by changing the appropriate attributes. If you never want
your tables to have borders you can do this:

```python
table.border = False
print(table)
print(table)
print(table)
```

Neither of the 3 tables printed by this will have borders, even if you do things like
add extra rows in between them. The lack of borders will last until you do:

```python
table.border = True
```

to turn them on again. This sort of long-term setting is exactly how `set_style` works.
`set_style` just sets a bunch of attributes to pre-set values for you.

Note that if you know what style options you want at the moment you are creating your
table, you can specify them using keyword arguments to the constructor. For example, the
following two code blocks are equivalent:

```python
table = PrettyTable()
table.border = False
table.header = False
table.padding_width = 5

table = PrettyTable(border=False, header=False, padding_width=5)
```

#### Changing style options just once

If you don't want to make long-term style changes by changing an attribute like in the
previous section, you can make changes that last for just one `get_string` by giving
those methods keyword arguments. To print two "normal" tables with one borderless table
between them, you could do this:

```python
print(table)
print(table.get_string(border=False))
print(table)
```

### Changing the appearance of your table - with _colors_!

PrettyTable has the functionality of printing your table with ANSI color codes. This
includes support for most Windows versions through
[Colorama](https://pypi.org/project/colorama/). To get started, import the `ColorTable`
class instead of `PrettyTable`.

```diff
-from prettytable import PrettyTable
+from prettytable.colortable import ColorTable
```

The `ColorTable` class can be used the same as `PrettyTable`, but it adds an extra
property. You can now specify a custom _theme_ that will format your table with colors.

```python
from prettytable.colortable import ColorTable, Themes

table = ColorTable(theme=Themes.OCEAN)

print(table)
```

#### Creating a custom theme

The `Theme` class allows you to customize both the characters and colors used in your
table.

| Argument                                                   | Description                                               |
| ---------------------------------------------------------- | --------------------------------------------------------- |
| `default_color`                                            | The color to use as default                               |
| `vertical_char`, `horizontal_char`, and `junction_char`    | The characters used for creating the outline of the table |
| `vertical_color`, `horizontal_color`, and `junction_color` | The colors used to style each character.                  |

> **Note:** Colors are formatted with the `Theme.format_code(s: str)` function. It
> accepts a string. If the string starts with an escape code (like `\x1b`) then it will
> return the given string. If the string is just whitespace, it will return `""`. If the
> string is a number (like `"34"`), it will automatically format it into an escape code.
> I recommend you look into the source code for more information.

### Displaying your table in JSON

PrettyTable will also print your tables in JSON, as a list of fields and an array of
rows. Just like in ASCII form, you can actually get a string representation - just use
`get_json_string()`.

### Displaying your table in MediaWiki markup

PrettyTable can also print your tables in MediaWiki table markup, making it easy to
format tables for wikis. Similar to the ASCII format, you can get a string
representation using `get_mediawiki_string()`.

### Displaying your table in HTML form

PrettyTable will also print your tables in HTML form, as `<table>`s. Just like in ASCII
form, you can actually get a string representation - just use `get_html_string()`. HTML
printing supports the `fields`, `start`, `end`, `sortby` and `reversesort` arguments in
exactly the same way as ASCII printing.

#### Styling HTML tables

By default, PrettyTable outputs HTML for "vanilla" tables. The HTML code is quite
simple. It looks like this:

```html
<table>
  <thead>
    <tr>
      <th>City name</th>
      <th>Area</th>
      <th>Population</th>
      <th>Annual Rainfall</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Adelaide</td>
      <td>1295</td>
      <td>1158259</td>
      <td>600.5</td>
    </tr>
    <tr>
      <td>Brisbane</td>
      <td>5905</td>
      <td>1857594</td>
      <td>1146.4</td>
      ...
    </tr>
  </tbody>
</table>
```

If you like, you can ask PrettyTable to do its best to mimic the style options that your
table has set using inline CSS. This is done by giving a `format=True` keyword argument
to `get_html_string` method. Note that if you _always_ want to print formatted HTML you
can do:

```python
table.format = True
```

and the setting will persist until you turn it off.

Just like with ASCII tables, if you want to change the table's style for just one
`get_html_string` you can pass those methods' keyword arguments - exactly like `print`
and `get_string`.

#### Setting HTML attributes

You can provide a dictionary of HTML attribute name/value pairs to the `get_html_string`
method using the `attributes` keyword argument. This lets you specify common HTML
attributes like `id` and `class` that can be used for linking to your tables or
customising their appearance using CSS. For example:

```python
print(table.get_html_string(attributes={"id":"my_table", "class":"red_table"}))
```

will print:

```html
<table id="my_table" class="red_table">
  <thead>
    <tr>
      <th>City name</th>
      <th>Area</th>
      <th>Population</th>
      <th>Annual Rainfall</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      ... ... ...
    </tr>
  </tbody>
</table>
```

#### Setting HTML escaping

By default, PrettyTable will escape the data contained in the header and data fields
when sending output to HTML. This can be disabled by setting the `escape_header` and
`escape_data` to false. For example:

```python
print(table.get_html_string(escape_header=False, escape_data=False))
```

### Miscellaneous things

#### Copying a table

You can call the `copy` method on a PrettyTable object without arguments to return an
identical independent copy of the table.

If you want a copy of a PrettyTable object with just a subset of the rows, you can use
list slicing notation:

```python
new_table = old_table[0:5]
```

## Contributing

After editing files, use the [Black](https://github.com/psf/black) linter to auto-format
changed lines.

```sh
python -m pip install black
black prettytable*.py
```
