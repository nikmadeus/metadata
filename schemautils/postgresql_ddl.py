import psycopg2

psql_user = "admin",
psql_password = 'password'

try:
    cursor = psycopg2.connect("dbname='postgres' user='{0}' password='{1}'".format(psql_user, psql_password)).cursor()
except psycopg2.Error as err:
    print("Connection error: {}".format(err))


# Generation DDL instructions
def genPSDDL(schema):

    result = "CREATE SCHEMA {name}".format(name=schema.name)
    result += "\n".join(map(genDomain, schema.domains))
    result += "\n".join(map(genTable, schema.tables))

    return result


def genDomain(domain):

    return """CREATE DOMAIN {domain_name} AS [{type}]""".format(
        domain_name=domain.name,
        type=domain.type
    )


def genTable(table):

    fields = "\n".join(map(genField, table.fields))
    indeces = "\n".join(map(lambda i: genIndex(i, table.name), table.indexes))
    constraints = "\n".join(map(lambda c: genConstraint(c, table.name), table.constraints))

    return """CREATE TABLE {table_name}(\n{fields})\n{indeces}\n{constraints}""".format(
        table_name=table.name,
        fields=fields,
        indeces=indeces,
        constraints=constraints
    )


def genField(field):

    return "{name} {type}".format(
        name=field.name,
        type=field.domain
    )


def genConstraint(constraint, tableName):

    return """ALTER TABLE {tableName} ADD CONSTRAINT {name} {kind} ({items})""".format(
        tableName=tableName,
        name=constraint.name,
        kind=constraint.kind,
        items=constraint.items
    )


def genIndex(index, tableName):

    return """CREATE INDEX {name} ON {tableName} ({field})""".format(
        name=index.name,
        tableName=tableName,
        field=index.fields
    )