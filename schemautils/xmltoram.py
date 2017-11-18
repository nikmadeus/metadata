from metadata import Schema, Domain, Table, Field, Index, Constraint
from xml.dom.minidom import parse
import custom_exceptions


def readxmlfile(path):
    dom = parse(path)
    schemas = []
    try:
        for child in dom.childNodes:
            schemas.append(parsing_schema(child))
    except Exception as e:
        print(str(e))
    return schemas


def checking_node(node):
    if node.nodeType == node.TEXT_NODE:
        if node.nodeValue.strip() == '':
            return True
        else:
            raise custom_exceptions.UnsupportedTagError('Node is not supported \"' + node.nodeValue + '\"')


def parsing_attributes(attr_dict, attributes):
    for attr in attributes.keys():
        if attr != 'props':
            if attr not in attr_dict:
                raise custom_exceptions.UnsupportedAttributeError('Attribute ' + attr + ' is not supported.')
            else:
                attr_dict[attr] = attributes.get(attr).value
        else:
            props = attributes.get(attr).value.split(', ')
            for prop in props:
                if prop not in attr_dict:
                    raise custom_exceptions.UnsupportedAttributeError('Attribute ' + prop + ' is not supported.')
                else:
                    attr_dict[prop] = True


def validating_schema(schema):
    schema.validating()  # Валидация объекта схемы
    for table in schema.tables.values():  # Валидация каждой из таблиц схемы
        for constraint in table.constraints:  # Валидация каждого ограничения таблицы
            constraint.validating()
        for index in table.indexes:  # Валидация табличных индексов
            index.validating()


def parsing_schema(dom_schema):
    try:
        schema = Schema()
        parsing_attributes(schema.attributes, dom_schema.attributes)
    except custom_exceptions.UnsupportedAttributeError as ex:
        raise Exception('Creating of schema is failed. ' + str(ex))
    try:
        for child in dom_schema.childNodes:
            if checking_node(child):
                continue
            elif child.tagName == 'domains':
                parsing_domain(schema, child)
            elif child.tagName == 'tables':
                parsing_table(schema, child)
            elif child.tagName != 'custom':
                raise custom_exceptions.UnsupportedTagError('Tag is not correct: ' + child.tagName)
    except Exception as ex:
        raise Exception('Schema ' + schema.__getattribute__('name') + ': ' + str(ex))
    validating_schema(schema)


def parsing_domain(schema, dom):
    domains = dom.childNodes
    for domain_element in domains:
        if checking_node(domain_element):
            continue
        elif domain_element.tagName != 'domain':
            raise custom_exceptions.UnsupportedTagError('Tag is not correct: ' + domain_element.tagName)
        domain = Domain(schema)
        parsing_attributes(domain.attributes, domain_element.attributes)
        domain.validating()


def parsing_table(schema, dom):
    tables = dom.childNodes
    for table_element in tables:
        if checking_node(table_element):
            continue
        elif table_element.tagName != 'table':
            raise custom_exceptions.UnsupportedTagError('Tag is not correct: ' + table_element.tagName)
        table = Table(schema)
        parsing_attributes(table.attributes, table_element.attributes)
        table.validating()

        for child in table_element.childNodes:  # Для каждого элемента таблицы выполняется проверка
            if checking_node(child):
                continue
            elif child.tagName == 'field':
                field = Field(table)
                parsing_attributes(field.attributes, child.attributes)
                field.validating()
            elif child.tagName == 'index':
                parsing_index(table, child)
            elif child.tagName == 'constraint':
                parsing_constraint(table, child)
            else:
                raise custom_exceptions.UnsupportedTagError('Tag is not correct: ' + table_element.tagName)


def parsing_index(table, index_element):
    index = Index(table)
    parsing_attributes(index.attributes, index_element.attributes)


def parsing_constraint(table, constraint_element):
    constraint = Constraint(table)
    parsing_attributes(constraint.attributes, constraint_element.attributes)
