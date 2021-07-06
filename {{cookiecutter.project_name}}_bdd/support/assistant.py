from ast import literal_eval


def convert_string_to_object(value):
    """Cast a string to an object."""
    try:
        return literal_eval(value)
    except ValueError:
        return value


def parse_behave_table(context_table):
    """Cast behave's table to a dict."""
    return next(
        dict(zip(context_table.headings, row)) for row in context_table.rows
    )


def cast_table_to_dict(context_table):
    """Converts behave's table to dict with types"""
    dict_with_strings = parse_behave_table(context_table)
    return {
        key: convert_string_to_object(value)
        for key, value in dict_with_strings.items()
    }


def cast_table_with_one_column_to_list(context_table):
    """Converts behave's one-column-table to list"""
    assert len(context_table.headings), "Table with more than one column"
    return [row[context_table.headings[0]] for row in context_table]
