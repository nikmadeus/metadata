from custom_minidom import *


def assembly_attributes(db_elem, dom_elem):  # сборка аттрибутов
    props_included = False
    for attr in db_elem.attributes:
        value = db_elem.attributes[attr]
        if value is True and not props_included:
            dom_elem.setAttribute('props', str(assembly_props(db_elem)))
            props_included = True
        elif value is not None and value is not False and value is not True:
            dom_elem.setAttribute(attr, str(value))


def assembly_props(db_elem):
    props = [str(attr) for attr in db_elem.attributes if db_elem.get(attr) is True]
    return ', '.join(props)


def writexmlfile(schema, output):
    doc = Document()
    # Заполнение схемы
    dbd_schema = doc.createElement('dbd_schema')
    assembly_attributes(schema, dbd_schema)

    domains_output = doc.createElement('domains')
    for domain in schema.domains.values():
        domain_output = doc.createElement("domain")
        assembly_attributes(domain, domain_output)
        domains_output.appendChild(domain_output)
    dbd_schema.appendChild(domains_output)

    tables_output = doc.createElement('tables')
    for table in schema.tables.values():
        table_output = doc.createElement("table")
        assembly_attributes(table, table_output)
        for field in table.fields.values():
            # Заполняется структура поля
            field_output = doc.createElement('field')
            assembly_attributes(field, field_output)
            table_output.appendChild(field_output)

        for constraint in table.constraints:
            constraint_output = doc.createElement('constraint')
            assembly_attributes(constraint, constraint_output)

        for index in table.indexes:
            index_output = doc.createElement('index')
            assembly_attributes(index, index_output)
            table_output.appendChild(index_output)
        tables_output.appendChild(table_output)
    dbd_schema.appendChild(tables_output)
    doc.appendChild(dbd_schema)

    # Выгрузка созданной dom-схемы в файл
    doc.writexml(open(output, 'w', encoding='utf-8'))
