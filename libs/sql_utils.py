from itertools import chain

import sqlalchemy as sa


def json_object(table: sa.Table | sa.sql.Alias):
    columns = {sa.text(f'\'{column.name}\''): column for column in table.c}
    return sa.func.json_build_object(*chain(*columns.items()))


def json_object_or_none(table: sa.Table | sa.sql.Alias):
    return sa.case(
        (
            table.c.id.isnot(None),
            json_object(table),
        ),
        else_=None,
    )
