import psycopg2

database_name = "Northwind"
psql_user = "postgres",
psql_password = 'root'

try:
    cursor = psycopg2.connect("dbname='postgres' user='{0}' password='{1}'".format(psql_user, psql_password)).cursor()
    cursor.execute('SELECT version()')
    print(cursor.fetchone())

    cursor.execute("DROP DATABASE IF EXISTS '{0}'".format(database_name))
    cursor.execute("Create DATABASE IF NOT EXISTS '{0}'".format(database_name))

except psycopg2.Error as err:
    print("Connection error: {}".format(err))


@staticmethod
def get_param(count):
    ret = "%s," * count
    return ret[:-1]


def transfer_table(table):
    # table_name = table.name
    # fields = [field.name for field in table.fields]
    # param = get_param(len(fields))
    # fields = ", ".join(fields)
    pass

# Generation DDL instructions
def genPSDDL(schema):

    # for table in schema.tables:
    #     transfer_table(table.name)

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
