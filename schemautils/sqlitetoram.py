from metadata import DatabaseSchema, Domain, Table, Field, Constraint, ConstraintDetail, Index, IndexDetail
import sqlite3


def sqlitetoram(sqlitefile):

    # Set connection with SQLite database
    connect = sqlite3.connect(sqlitefile)
    cursor = connect.cursor()
    print(sqlite3.version)
    print("Database opened succesfully!")

    # Schema
    schema_query = cursor.execute("""select name from dbd$schemas""")

    schema = DatabaseSchema()
    # schema.name = schema_query[1]

    # Domains
    domains_query = cursor.execute("""
                                     select
                                     dbd$domains.id,
                                     dbd$domains.name,
                                     dbd$domains.description,
                                     dbd$data_types.type_id,
                                     dbd$domains.length,
                                     dbd$domains.char_length,
                                     dbd$domains.precision,
                                     dbd$domains.scale,
                                     dbd$domains.width,
                                     dbd$domains.align,
                                     dbd$domains.show_null,
                                     dbd$domains.show_lead_nulls,
                                     dbd$domains.thousands_separator,
                                     dbd$domains.summable,
                                     dbd$domains.case_sensitive "case_sensitive",
                                     dbd$domains.uuid
                                   from dbd$domains
                                     inner join dbd$data_types on dbd$domains.data_type_id = dbd$data_types.id
                                   order by dbd$domains.id
                                   """).fetchall()
    for domain_row in domains_query:

        domain = Domain()

        if domain_row[1] is not None:
            domain.name = domain_row[1]
        if domain_row[2] is not None:
            domain.description = domain_row[2]
        if domain_row[3] is not None:
            domain.type = domain_row[3]
        if domain_row[4] is not None:
            domain.length = int(domain_row[4])
        if domain_row[5] is not None:
            domain.char_length = int(domain_row[5])
        if domain_row[6] is not None:
            domain.precision = int(domain_row[6])
        if domain_row[7] is not None:
            domain.scale = int(domain_row[7])
        if domain_row[8] is not None:
            domain.width = int(domain_row[8])
        if domain_row[9] is not None:
            domain.align = domain_row[9]

        props = []

        if (domain_row[10] is not None) and (domain_row[10] == 1):
            props.append("show_null")
        if (domain_row[11] is not None) and (domain_row[11] == 1):
            props.append("show_lead_nulls")
        if (domain_row[12] is not None) and (domain_row[12] == 1):
            props.append("thousands_separator")
        if (domain_row[13] is not None) and (domain_row[13] == 1):
            props.append("summable")
        if (domain_row[14] is not None) and (domain_row[14] == 1):
            props.append("case_sensitive")
        domain.props = ", ".join(props)

        if domain_row[15] is not None:
            domain.uuid = domain_row[15]

        if domain_row[1] is not None:
            schema.domains.append(domain)

    tables_query = cursor.execute("""
                                  select
                                    dbd$tables.id,
                                    dbd$schemas.name "schema_name",
                                    dbd$tables.name "table_name",
                                    dbd$tables.description,
                                    dbd$tables.means,
                                    dbd$tables.can_add,
                                    dbd$tables.can_edit,
                                    dbd$tables.can_delete,
                                    dbd$tables.temporal_mode
                                  from dbd$tables
                                    inner join dbd$schemas on dbd$tables.schema_id = dbd$schemas.id
                                  order by dbd$tables.id
                                  """).fetchall()

    for table_row in tables_query:

        table = Table()

        table.name = table_row[2]
        table.description = table_row[3]
        table.means = table_row[4]

        props = []

        if (table_row[5] is not None) and (table_row[5] == 1):
            props.append("add")
        if (table_row[6] is not None) and (table_row[6] == 1):
            props.append("edit")
        if (table_row[7] is not None) and (table_row[7] == 1):
            props.append("delete")
        table.props = ", ".join(props)

        if table_row[8] is not None:
            table.temporal_mode = table_row[8]

        if table_row[2] is not None:
            schema.tables.append(table)

    fields_query = cursor.execute("""
                                                      select
                                                        dbd$fields.id,
                                                        dbd$fields.table_id,
                                                        dbd$fields.position,
                                                        dbd$fields.name,
                                                        dbd$fields.russian_short_name,
                                                        dbd$fields.description,
                                                        dbd$fields.domain_id,
                                                        dbd$fields.can_input,
                                                        dbd$fields.can_edit,
                                                        dbd$fields.show_in_grid,
                                                        dbd$fields.show_in_details,
                                                        dbd$fields.is_mean,
                                                        dbd$fields.autocalculated,
                                                        dbd$fields.required
                                                      from dbd$fields
                                                      order by dbd$fields.table_id, dbd$fields.position
                                                      """).fetchall()
    for field_row in fields_query:

        field = Field()

        field.name = field_row[3]
        field.rname = field_row[4]
        field.description = field_row[5]

        props = []

        if (field_row[7] is not None) and (field_row[7] == 1):
            props.append("input")
        if (field_row[8] is not None) and (field_row[8] == 1):
            props.append("edit")
        if (field_row[9] is not None) and (field_row[9] == 1):
            props.append("show_in_grid")
        if (field_row[10] is not None) and (field_row[10] == 1):
            props.append("show_in_details")
        if (field_row[11] is not None) and (field_row[11] == 1):
            props.append("is_mean")
        if (field_row[12] is not None) and (field_row[12] == 1):
            props.append("autocalculated")
        if (field_row[13] is not None) and (field_row[13] == 1):
            props.append("required")
        field.props = ", ".join(props)

        field.uuid = field_row[14]

    return schema
