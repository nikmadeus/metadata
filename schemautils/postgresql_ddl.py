# Generation DDL instructions
def genPSDDL(ddl_path, schema):

    result = "CREATE SCHEMA {0}".format(schema.name)
    result += "\n".join(map(genDomain, schema.domains))
    result += "\n".join(map(genTable, schema.tables))

    if ddl_path:
        with open(ddl_path, 'w', encoding='utf-8') as file:
            file.write(result)
    return result

    return result


def genDomain(domain):

    return """CREATE DOMAIN {0} AS [{1}]""".format(
        domain.name,
        domain.type
    )


def genTable(table):

    fields = "\n".join(map(genField, table.fields))
    indeces = "\n".join(map(lambda i: genIndex(i, table.name), table.indexes))
    forconstraints = map(lambda c: genForConstraint(table.name, c),
                      filter(lambda c: c.kind == "FOREIGN", table.constraints))
    checkconstraints = map(lambda c: genCheckConstraint(table.name, c),
                         filter(lambda c: c.kind == "CHECK", table.constraints))

    return """CREATE TABLE {0}(\n{1})\n{2}\n{3}\n{4}""".format(
        table.name,
        fields,
        indeces,
        forconstraints,
        checkconstraints
    )


def genField(field):

    return "{0} {1}".format(
        field.name,
        field.domain
    )


def genForConstraint(constraint, tableName):

    return """ALTER TABLE {0} ADD FOREIGN KEY ({1}) REFERENCES {2} {3};\n""".format(
        tableName,
        constraint.name,
        constraint.reference,
        constraint.items
    )


def genCheckConstraint(constraint, tableName):

    return "ALTER TABLE {0} ADD CHECK {1} {2};\n".format(
        tableName,
        constraint.expression,
        constraint.items
    )


def genIndex(index, tableName):

    return """CREATE {0} {1} ON {2} ({3})""".format(
        "UNIQUE" if index.uniqueness else "",
        "INDEX" + index.name if index.name is not None else "INDEX",
        tableName,
        index.fields[0]
    )
