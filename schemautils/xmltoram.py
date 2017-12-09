from metadata import DatabaseSchema, Domain, Table, Field, Constraint, ConstraintDetail, Index, IndexDetail


def xmltoram(xml):

    schema = DatabaseSchema()

    SchemaElement = xml.getElementsByTagName("dbd_schema")
    for schema in SchemaElement:
        schema.fulltext_engine = schema.getAttribute('fulltext_engine')
        schema.version = schema.getAttribute('version')
        schema.name = schema.getAttribute('name')
        schema.description = schema.getAttribute('description')

    schema.domains = createObjDomains(xml)
    schema.tables = createObjTables(xml)

    return schema


def createObjDomains(xml):

    domains = []

    DomainElement = xml.getElementsByTagName("domain")
    for domain in DomainElement:
        vardomain = Domain()
        for attr in domain.attributes.keys():
            if attr == "name":
                vardomain.name = domain.getAttribute('name')
            if attr == "type":
                vardomain.type = domain.getAttribute('type')
            if attr == "description":
                vardomain.description = domain.getAttribute('description')
            if attr == "data_type_id":
                vardomain.data_type_id = domain.getAttribute('data_type_id')
            if attr == "length":
                vardomain.length = domain.getAttribute('length')
            if attr == "char_length":
                vardomain.char_length = domain.getAttribute('char_length')
            if attr == "precision":
                vardomain.precision = domain.getAttribute('precision')
            if attr == "scale":
                vardomain.scale = domain.getAttribute('scale')
            if attr == "width":
                vardomain.width = domain.getAttribute('width')
            if attr == "align":
                vardomain.align = domain.getAttribute('align')
            if attr == "props":
                for prop in domain.getAttribute('props').split(", "):
                    if prop == "show_null":
                        vardomain.show_null = True
                    elif prop == "show_lead_nulls":
                        vardomain.show_lead_nulls = True
                    elif prop == "thousands_separator":
                        vardomain.thousands_separator = True
                    elif prop == "summable":
                        vardomain.summable = True
                    elif prop == "case_sensitive":
                        vardomain.case_sensitive = True

        # vardomain.validating()
        domains.append(vardomain)

    return domains


def createObjTables(xml):

    tables = []

    TableElement = xml.getElementsByTagName("table")
    for table in TableElement:
        vartable = Table()
        for attr in table.attributes.keys():
            if attr == "name":
                vartable.name = table.getAttribute('name')
                if attr == "description":
                    vartable.description = table.getAttribute('description')
                if attr == "temporal_mode":
                    vartable.temporal_mode = table.getAttribute('temporal_mode')
                if attr == "means":
                    vartable.means = table.getAttribute('means')
                if attr == "props":
                    for prop in table.getAttribute('props').split(", "):
                        if prop == "add":
                            vartable.can_add = True
                        elif prop == "edit":
                            vartable.can_edit = True
                        elif prop == "delete":
                            vartable.can_delete = True

        vartable.fields = createObjFields(table)
        vartable.indexes = createObjIndexes(table)
        vartable.constraints = createObjConstraints(table)

        # vartable.validating()
        tables.append(vartable)

    return tables


def createObjFields(xml):

    # if xml.nodeName != "table":
    #     raise TypeError("Element is not table")

    fields = []

    FieldElement = xml.getElementsByTagName("field")
    for field in FieldElement:
        varfield = Field()
        for attr in field.attributes.keys():
            if attr == "position":
                varfield.position = field.getAttribute('position')
            if attr == "name":
                varfield.name = field.getAttribute('name')
            if attr == "rname":
                varfield.rname = field.getAttribute('rname')
            if attr == "description":
                varfield.description = field.getAttribute('description')
            if attr == "domain":
                varfield.domain = field.getAttribute('domain')
            if attr == "props":
                for prop in field.getAttribute('props').split(", "):
                    if prop == "input":
                        varfield.can_input = True
                    elif prop == "edit":
                        varfield.can_edit = True
                    elif prop == "show_in_grid":
                        varfield.show_in_grid = True
                    elif prop == "show_in_details":
                        varfield.show_in_details = True
                    elif prop == "is_mean":
                        varfield.is_mean = True
                    elif prop == "autocalculated":
                        varfield.autocalculated = True
                    elif prop == "required":
                        varfield.required = True

        # varfield.validating()
        fields.append(varfield)

    return fields


def createObjConstraints(xml):

    # if xml.nodeName != "table":
    #     raise TypeError("Element is not table")

    constraints = []

    ConstraintElement = xml.getElementsByTagName("constraint")
    for constraint in ConstraintElement:
        varconstraint = Constraint()
        for attr in constraint.attributes.keys():
            if attr == "name":
                varconstraint.name = constraint.getAttribute('name')
            if attr == "constraint_type":
                varconstraint.constraint_type = constraint.getAttribute('constraint_type')
            if attr == "reference":
                varconstraint.reference = constraint.getAttribute('reference')
            if attr == "expression":
                varconstraint.expression = constraint.getAttribute('expression')
            if attr == "kind":
                varconstraint.kind = constraint.getAttribute('kind')
            if attr == "items":
                varconstraint.items = constraint.getAttribute('items')
            if attr == "props":
                for prop in constraint.getAttribute('props').split(", "):
                    if prop == "has_value_edit":
                        varconstraint.has_value_edit = True
                    elif prop == "cascading_delete":
                        varconstraint.cascading_delete = True
                    elif prop == "full_cascading_delete":
                        varconstraint.cascading_delete = True

        # varconstraint.validating()
        constraints.append(varconstraint)

    return constraints


def createObjIndexes(xml):

    # if xml.nodeName != "table":
    #     raise TypeError("Element is not table")

    indexes = []

    IndexElement = xml.getElementsByTagName("index")
    for index in IndexElement:
        varindex = Index()
        for attr in index.attributes.keys():
            if attr == "name":
                varindex.name = index.getAttribute('name')
            if attr == "kind":
                varindex.kind = index.getAttribute('kind')
            if attr == "field":
                varindex.field = index.getAttribute('field')
            if attr == "props":
                for prop in index.getAttribute('props').split(", "):
                    if prop == "fulltext":
                        varindex.fulltext = True
                    elif prop == "uniqueness":
                        varindex.uniqueness = True

        # varindex.validating()
        indexes.append(varindex)

    return indexes
