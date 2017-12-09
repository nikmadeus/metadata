from additionalfiles import custom_minidom as md
from codecs import open


def ramtoxml(schema):

    if schema is None:
        raise Exception('Schema is not defined!')

    xml = md.Document()

    dbd_schema = xml.createElement('dbd_schema')

    if schema.fulltext_engine is not None:
        dbd_schema.setAttribute("fulltext_engine", schema.fulltext_engine)
    if schema.version is not None:
        dbd_schema.setAttribute("version", schema.version)
    if schema.name is not None:
        dbd_schema.setAttribute("name", schema.name)
    if schema.description is not None:
        dbd_schema.setAttribute("description", schema.description)

    dbd_schema.appendChild(xml.createElement("custom"))

    domains = xml.createElement("domains")
    for domain in addDomains(xml, schema.domains):
        domains.appendChild(domain)
    dbd_schema.appendChild(domains)

    tables = xml.createElement("tables")
    for table in addTables(xml, schema.tables):
        tables.appendChild(table)
    dbd_schema.appendChild(tables)

    xml.appendChild(dbd_schema)

    # xml.writexml(open("test.xml", 'w', 'utf-8'), '', '  ', '\n', 'utf-8')
    # запись в файл
    xml_str = xml.toprettyxml(indent="  ")
    with open("test.xml", "w", 'utf-8') as f:
        f.write(xml_str)

    return xml


def addDomains(xml, domains):

    for domain in domains:
        node = xml.createElement("domain")
        if domain.name is not None:
            node.setAttribute("name", domain.name)
        if domain.type is not None:
            node.setAttribute("type", domain.type)
        if domain.description is not None:
            node.setAttribute("description", domain.description)
        if domain.data_type_id is not None:
            node.setAttribute("data_type_id", domain.data_type_id)
        if domain.length is not None:
            node.setAttribute("length", domain.length)
        if domain.char_length is not None:
            node.setAttribute("char_length", domain.char_length)
        if domain.precision is not None:
            node.setAttribute("precision", domain.precision)
        if domain.scale is not None:
            node.setAttribute("scale", domain.scale)
        if domain.width is not None:
            node.setAttribute("width", domain.width)
        if domain.align is not None:
            node.setAttribute("align", domain.align)

        props = []
        if domain.show_null:
            props.append("show_null")
        if domain.show_lead_nulls:
            props.append("show_lead_nulls")
        if domain.thousands_separator:
            props.append("thousands_separator")
        if domain.summable:
            props.append("summable")
        if domain.case_sensitive:
            props.append("case_sensitive")

        if props:
            node.setAttribute("props", ", ".join(props))

        yield node


def addTables(xml, tables):

    for table in tables:
        node = xml.createElement("table")
        if table.name is not None:
            node.setAttribute("name", table.name)
        if table.description is not None:
            node.setAttribute("description", table.description)
        if table.temporal_mode is not None:
            node.setAttribute("temporal_mode", table.temporal_mode)
        if table.means is not None:
            node.setAttribute("means", table.means)

        props = []
        if table.can_add:
            props.append("add")
        if table.can_edit:
            props.append("edit")
        if table.can_delete:
            props.append("delete")
        if props:
            node.setAttribute("props", ", ".join(props))

        if table.constraints:
            for field in addFields(xml, table.fields):
                node.appendChild(field)

        if table.constraints:
            for constraint in addConstraints(xml, table.constraints):
                node.appendChild(constraint)

        if table.constraints:
            for index in addIndexes(xml, table.indexes):
                node.appendChild(index)

        yield node


def addFields(xml, fields):

    for field in fields:
        node = xml.createElement("field")
        if field.position is not None:
            node.setAttribute("position", field.position)
        if field.name is not None:
            node.setAttribute("name", field.name)
        if field.rname is not None:
            node.setAttribute("rname", field.rname)
        if field.description is not None:
            node.setAttribute("description", field.description)
        if field.domain is not None:
            node.setAttribute("domain", field.domain)

        props = []
        if field.can_input:
            props.append("input")
        if field.can_edit:
            props.append("edit")
        if field.show_in_grid:
            props.append("show_in_grid")
        if field.show_in_details:
            props.append("show_in_details")
        if field.is_mean:
            props.append("is_mean")
        if field.autocalculated:
            props.append("autocalculated")
        if field.required:
            props.append("required")
        if props:
            node.setAttribute("props", ", ".join(props))

        yield node


def addConstraints(xml, constraints):

    for constraint in constraints:
        node = xml.createElement("constraint")

        if constraint.name is not None:
            node.setAttribute("name", constraint.name)
        if constraint.constraint_type is not None:
            node.setAttribute("constraint_type", constraint.constraint_type)
        if constraint.reference is not None:
            node.setAttribute("reference", constraint.reference)
        if constraint.expression is not None:
            node.setAttribute("expression", constraint.expression)
        if constraint.kind is not None:
            node.setAttribute("kind", constraint.kind)
        if constraint.items is not None:
            node.setAttribute("items", constraint.items)

        props = []
        if constraint.has_value_edit:
            props.append("has_value_edit")
        if constraint.cascading_delete:
            props.append("cascading_delete")
        if constraint.cascading_delete:
            props.append("full_cascading_delete")
        if props:
            node.setAttribute("props", ", ".join(props))

        yield node


def addIndexes(xml, indexes):

    for index in indexes:
        if not index.fields == []:
            node = xml.createElement("index")

            if index.name is not None:
                node.setAttribute("name", index.name)
            if index.kind is not None:
                node.setAttribute("kind", index.kind)

            props = []
            if index.fulltext:
                props.append("fulltext")
            if index.uniqueness:
                props.append("uniqueness")
            if props:
                node.setAttribute("props", ", ".join(props))

            yield node
