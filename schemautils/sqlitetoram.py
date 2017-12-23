from metadata import DatabaseSchema, Domain, Table, Field, Constraint, Index
import sqlite3


def sqlitetoram(sqlitefile):
    # Установка соединения с SQLite базой
    connect = sqlite3.connect(sqlitefile)
    cursor = connect.cursor()
    print("sqlite version: ", sqlite3.version)
    print("Database ", sqlitefile, " opened succesfully!")

    # Schema
    schema_query = cursor.execute("""select dbd$schemas.id, dbd$schemas.name from dbd$schemas""").fetchone()

    schema = DatabaseSchema()
    if schema_query[0] is not None:
        schema.id = schema_query[0]
    if schema_query[1] is not None:
        schema.name = schema_query[1]

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
                                     dbd$domains.case_sensitive,
                                     dbd$domains.uuid
                                   from dbd$domains
                                     inner join dbd$data_types on dbd$domains.data_type_id = dbd$data_types.id
                                   order by dbd$domains.id
                                   """).fetchall()
    for domain_row in domains_query:

        domain = Domain()

        if domain_row[0] is not None:
            domain.id = domain_row[0]
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

        if domain_row[10] == 1:
            props.append("show_null")
        if domain_row[11] == 1:
            props.append("show_lead_nulls")
        if domain_row[12] == 1:
            props.append("thousands_separator")
        if domain_row[13] == 1:
            props.append("summable")
        if domain_row[14] == 1:
            props.append("case_sensitive")
        domain.props = ", ".join(props)

        if domain_row[15] is not None:
            domain.uuid = domain_row[15]

        if domain_row[1] is not None:
            schema.domains.append(domain)

    # Tables
    tables_query = cursor.execute("""
                                  select
                                    dbd$tables.id,
                                    dbd$schemas.name,
                                    dbd$tables.name,
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

        if table_row[5] == 1:
            props.append("add")
        if table_row[6] == 1:
            props.append("edit")
        if table_row[7] == 1:
            props.append("delete")
        table.props = ", ".join(props)

        if table_row[8] is not None:
            table.temporal_mode = table_row[8]

        if table_row[2] is not None:
            schema.tables.append(table)

    # Fields
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
                                    dbd$fields.required,
                                    dbd$fields.uuid
                                  from dbd$fields
                                  order by dbd$fields.table_id, dbd$fields.position
                                  """).fetchall()
    for field_row in fields_query:

        field = Field()

        field.name = field_row[3]
        field.rname = field_row[4]
        field.description = field_row[5]
        field.domain = field_row[6]

        props = []

        if field_row[7] == 1:
            props.append("input")
        if field_row[8] == 1:
            props.append("edit")
        if field_row[9] == 1:
            props.append("show_in_grid")
        if field_row[10] == 1:
            props.append("show_in_details")
        if field_row[11] == 1:
            props.append("is_mean")
        if field_row[12] == 1:
            props.append("autocalculated")
        if field_row[13] == 1:
            props.append("required")
        field.props = ", ".join(props)

        field.uuid = field_row[14]

    # Constraints
    constraints_query = cursor.execute("""
                                      select
                                        constraints_t.id "constraint_id",
                                        constraints_t.name,
                                        constraints_t.constraint_type "constraint_type",
                                        dbd$constraint_details.position "position",
                                        dbd$tables.id "table_id",
                                        dbd$fields.id "field_id",
                                        dbd$fields.name "field_name",
                                        const_ref.table_id "ref_table_id",
                                        constraints_t.has_value_edit,
                                        constraints_t.cascading_delete,
                                        constraints_t.expression
                                      from
                                        dbd$constraints constraints_t
                                        left join dbd$constraint_details
                                          on dbd$constraint_details.constraint_id = constraints_t.id
                                        inner join dbd$tables
                                          on constraints_t.table_id = dbd$tables.id
                                        left join dbd$fields
                                          on dbd$constraint_details.field_id=dbd$fields.id
                                        left join dbd$constraints const_ref
                                          on constraints_t.unique_key_id = const_ref.id
                                      order by
                                        table_id, position
                                      """).fetchall()
    for constraint_row in constraints_query:

        constraint = Constraint()

        constraint.name = constraint_row[2]
        constraint.constraint_type = constraint_row[3]
        constraint.reference = constraint_row[4]
        constraint.unique_key_id = constraint_row[5]

        props = []

        if constraint_row[6] == 1:
            props.append("has_value_edit")
        if constraint_row[7] == 1:
            props.append("cascading_delete")
        if props:
            constraint.props = ", ".join(props)

        constraint.expression = constraint_row[8]
        constraint.uuid = constraint_row[9]

    # Indexes
    index_query = cursor.execute("""
                                   select
                                     dbd$indices.id,
                                     dbd$indices.name,
                                     dbd$indices.table_id,
                                     dbd$index_details.position,
                                     dbd$index_details.field_id,
                                     dbd$fields.name,
                                     dbd$indices.kind,
                                     dbd$indices.local,
                                     dbd$index_details.descend,
                                     dbd$index_details.expression
                                   from
                                     dbd$indices
                                     inner join dbd$index_details
                                       on dbd$index_details.index_id = dbd$indices.id
                                     inner join dbd$tables
                                       on dbd$indices.table_id = dbd$tables.id
                                     left join dbd$fields
                                       on dbd$index_details.field_id = dbd$fields.id
                                   order by
                                     dbd$tables.name, dbd$index_details.position
                                   """).fetchall()
    for index_row in index_query:
        index = Index()
        props = []
        index.name = index_row[2]
        index.local = index_row[3]
        index.kind = index_row[4]
        index.field = index_row[4]
        index.uuid = index_row[5]
        if props:
            index.props = ", ".join(props)

    return schema
