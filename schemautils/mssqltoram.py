from metadata import DatabaseSchema, Domain, Table, Field, Constraint, ConstraintDetail, Index, IndexDetail
import pymssql


def mssqltoram(schema, mssqlfile):

    connect = pymssql.connect(server='localhost', user='user', password='password', database='Northwind')
    cursor = connect.cursor()

    # creating schema
    cursor.execute("use Northwind;")
    row = cursor.execute("""
                          SELECT
                          TOP(1) TABLE_SCHEMA
                          FROM
                          INFORMATION_SCHEMA.TABLES
                          WHERE TABLE_TYPE = 'BASE TABLE'
                          """).fetchone()
    schema = DatabaseSchema()
    schema.name = row[0]

    # creating tables
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
            table.append_field(field)
            row = cursor.fetchone()

        tables_map = {}
        for table in schema.tables:
            tables_map[table.name] = table
        cursor.execute("""
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
        row = cursor.fetchone()
        while row is not None:
            index = Index()
            index.field_name = row[0]
            index.field = tables_map[row[0]]
            table.append_index(index)
            row = cursor.fetchone()
