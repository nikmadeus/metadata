import pypyodbc
import psycopg2


def createPostgresqlDDL(schema):
    result = ""
    result += createSchema(schema)

    result += "\n".join(map(createDomain, schema.domains))

    result += "\n".join(map(createTable, schema.tables))

    return result


def createSchema(schema):
    return "CREATE SCHEMA {name}".format(name=schema.name)


def createDomain(domain):
    return """CREATE DOMAIN {domain_name} AS [{type_}]""".format(
        domain_name=domain.name,
        type_=domain.type
    )


def createTable(table):
    fields = ",\n".join(map(createField, table.fields))
    indeces = "\n".join(map(lambda i: createIndex(i, table.name), table.indexes))
    constraints = "\n".join(map(lambda c: createConstraint(c, table.name), table.constraints))
    return """CREATE TABLE {table_name}(\n{fields})\n{indeces}\n{constraints}""".format(
        table_name=table.name,
        fields=fields,
        indeces=indeces,
        constraints=constraints
    )


def createField(field):
    pass
    return "{name} {type_}".format(
        name=field.name,
        type_=field.domain
    )


def createIndex(index, tableName):
    return """CREATE INDEX {name} ON {tableName} ({field})""".format(
        name=index.name,
        tableName=tableName,
        field=index.fields
    )


def createConstraint(constraint, tableName):
    return """ALTER TABLE {tableName} ADD CONSTRAINT {name} {kind} ({items})""".format(
        tableName=tableName,
        name=constraint.name,
        kind=constraint.kind,
        items=constraint.items
    )