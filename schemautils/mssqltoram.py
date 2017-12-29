import pymssql
from additionalfiles.metadata import *


def mssqltoram():
    connect = pymssql.connect(server='localhost', user='user', password='password', database='Northwind')
    cursor = connect.cursor()

    # creating schema
    cursor.execute("use Northwind;")
    cursor.execute("""
                      SELECT
                      TOP(1) TABLE_SCHEMA
                      FROM
                      INFORMATION_SCHEMA.TABLES
                      WHERE TABLE_TYPE = 'BASE TABLE'
                      """)
    row = cursor.fetchone()
    schema = DatabaseSchema()
    schema.name = row[0]
    create_tables(schema, connect)
    return schema


def create_tables(schema, connect):
    cursor = connect.cursor()
    cursor.execute("""
                        SELECT
                            TABLE_NAME
                        FROM
                        INFORMATION_SCHEMA.TABLES
                        WHERE TABLE_TYPE = 'BASE TABLE' AND  not TABLE_NAME = 'sysdiagrams'
                        """)
    row = cursor.fetchone()
    while row is not None:
        table = Table()
        table.name = row[0]
        row = cursor.fetchone()
        schema.tables.append(table)

    cursor.close()

    for table in schema.tables:
        create_fields(connect, table)

    for table in schema.tables:
        create_constraints(connect, schema, table)

    for table in schema.tables:
        create_index(connect, schema, table)


def create_fields(connect, table):
    cursor = connect.cursor()
    cursor.execute("""
                SELECT
                    COLUMN_NAME,
                    DATA_TYPE,
                    CHARACTER_MAXIMUM_LENGTH
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = ?
                """, (table.name,))
    row = cursor.fetchone()
    while row is not None:
        field = Field()
        domain = Domain()
        field.name = row[0]
        domain.char_length = row[2]
        domain.type = row[1]
        field.domain = domain
        table.fields.append(field)
        row = cursor.fetchone()

    cursor.close()


def create_constraints(connect, schema, table):
    cursor = connect.cursor()
    cursor.execute("""
                    SELECT
                        ic.key_ordinal,
                        cl.name
                    FROM sys.key_constraints c
                    join sys.indexes i on c.parent_object_id = i.object_id
                        and c.unique_index_id = i.index_id
                    join sys.index_columns ic on ic.object_id = i.object_id
                        and ic.index_id = i.index_id
                    join sys.columns cl on cl.object_id = i.object_id
                        and ic.column_id = cl.column_id
                    WHERE
                        c.type = 'PK'
                        and 0 = ic.is_included_column
                        and
                        i.object_id = object_id(?)
                    order by ic.key_ordinal
                    """, (table.name,))
    row = cursor.fetchone()
    while row is not None:
        constraint = Constraint()  # PRIMARY
        constraint.item = table.fields[row[1]]
        constraint.item_name = row[1]
        table.constraints.append(constraint)
        row = cursor.fetchone()

    tables_map = {}
    for table in schema.tables:
        tables_map[table.name] = table
    cursor.execute("""
                    SELECT
                        COL_NAME(parent_object_id, parent_column_id) ColumnName,
                        OBJECT_NAME(referenced_object_id) RefTableName,
                        COL_NAME(referenced_object_id, referenced_column_id) RefColumnName

                    FROM
                        sys.foreign_key_columns
                    Where OBJECT_NAME(parent_object_id) = ?;
                    """, (table.name,))
    row = cursor.fetchone()
    while row is not None:
        constraint = Constraint()  # FOREIGN
        constraint.item = table.fields[row[0]]
        constraint.item_name = row[0]
        constraint.reference = tables_map[row[1]]
        constraint.ref_name = row[1]
        if constraint.const_type == 'FOREIGN' and constraint.ref_name == '':
            raise Exception('Нет ссылки для внешнего ключа!')
        if constraint.item_name == '':
            raise Exception('Значения элементов пусты!')

        table.constraints.append(constraint)
        row = cursor.fetchone()


def create_index(connect, schema, table):
    cur = connect.cursor()
    tables_map = {}
    for table in schema.tables:
        tables_map[table.name] = table
    cur.execute("""
                SELECT ind.name IndexName
                FROM sys.indexes ind
                INNER JOIN sys.index_columns ic
                    ON  ind.object_id = ic.object_id and ind.index_id = ic.index_id
                INNER JOIN sys.columns col
                    ON ic.object_id = col.object_id and ic.column_id = col.column_id
                INNER JOIN sys.tables t
                    ON ind.object_id = t.object_id
                WHERE
                    ind.is_primary_key = 0
                    AND ind.is_unique = 0
                    AND ind.is_unique_constraint = 0
                    AND t.is_ms_shipped = 0
                    AND t.name = ?
                """, (table.name,))
    row = cur.fetchone()
    while row is not None:
        index = Index()
        index.field.name = row[0]
        index.field = tables_map[row[0]]
        table.indexes.append(index)
        row = cur.fetchone()
