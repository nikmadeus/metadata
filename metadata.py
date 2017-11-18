"""
Модуль с классами представления базы в RAM.
validating() - функция валидации(проверки на соответствие аттрибутов)
"""
import custom_exceptions


class Schema:
    def __init__(self):

        self.fulltext_engine = None
        self.version = None
        self.name = None
        self.description = None

        self.domains = {}
        self.tables = {}

    def validating(self):
        if self.__getattribute__('name') is None:
            raise custom_exceptions.PropertyError('The schema name is not defined')


class Domain:
    def __init__(self, schema):
        self.schema = schema

        self.id = None
        self.name = None
        self.description = None
        self.type = None
        self.data_type_id = None
        self.length = None
        self.char_length = None
        self.precision = None
        self.scale = None
        self.width = None
        self.align = None
        self.show_null = None
        self.show_lead_nulls = None
        self.thousands_separator = None
        self.summable = None
        self.case_sensitive = None
        self.uuid = None

    def validating(self):
        if self.__getattribute__('name') is None:
            raise custom_exceptions.PropertyError('The domain name is not defined')
        if self.__getattribute__('type') is None:
            raise custom_exceptions.PropertyError('The domain type is not defined ' + str(self.__getattribute__('name')))
        if self.__getattribute__('type') not in self.schema.data_types:
            raise custom_exceptions.UnsupportedDataTypeError('Domain type is not correct ' + str(self.__getattribute__('name')))
        if self.__getattribute__('name') in self.schema.domains.keys():
            raise custom_exceptions.UniqueViolationError('Domain ' + str(self.__getattribute__('name')) + ' already exists')


class Table:
    def __init__(self, schema):
        self.schema = schema

        self.name = None,
        self.description = None,
        self.add = None,
        self.edit = None,
        self.delete = None,
        self.temporal_mode = None,
        self.means = None

        self.fields = {}
        self.indexes = []
        self.constraints = []

    def validating(self):
        if self.__getattribute__('name') is None:
            raise custom_exceptions.PropertyError('The table name is not defined')
        if self.__getattribute__('name') in self.schema.tables:
            raise custom_exceptions.UniqueViolationError('Table ' + str(self.__getattribute__('name')) + ' already exists')


class Field:
    def __init__(self, table):
        self.table = table
        self.domain = None

        self.name = None
        self.rname = None
        self.domain = None
        self.type = None
        self.description = None
        self.input = None
        self.edit = None
        self.show_in_grid = None
        self.show_in_details = None
        self.is_mean = None
        self.autocalculated = None
        self.required = None


    def validating(self):
        if self.__dict__['name'] is None:
            raise custom_exceptions.PropertyError('The field name is not defined')
        if self.__getattribute__('name') in self.table.fields:
            raise custom_exceptions.UniqueViolationError('Field ' + str(self.__getattribute__('name')) + ' already exists')
        if self.__dict__['domain'] is None and self.__dict__['type'] is None:
            raise custom_exceptions.PropertyError('Domain and type of field ' + str(self.__getattribute__('name')) + ' are not defined')
        if self.__dict__['domain'] is not None and self.__getattribute__('domain') not in self.table.schema.domains:
            raise custom_exceptions.ReferenceError('Domain of field ' + str(self.__getattribute__('name')) + ' is not correct')
        if self.__dict__['type'] is not None and self.__getattribute__('type') not in self.table.schema.data_types:
            raise custom_exceptions.ReferenceError('Type of field ' + str(self.__getattribute__('name')) + ' is not correct')


class Constraint:

    def __init__(self, table):
        self.table = table

        self.name = None
        self.kind = None
        self.items = None
        self.reference = None
        self.constraint = None
        self.has_value_edit = None
        self.cascading_delete = None
        self.full_cascading_delete = None
        self.expression = None

        self.details = []
        self.table.constraints.append(self)

    def validating(self):
        if 'kind' not in self.__dict__:
            raise custom_exceptions.PropertyError('Constraint type of the table is not defined')
        elif self.__getattribute__('kind') == 'PRIMARY' and any([key for key in self.table.constraints if key.__getattribute__('kind') == 'PRIMARY' and key != self]):
            raise custom_exceptions.UniqueViolationError('More than one primary key are defined')
        elif self.__getattribute__('kind') != 'FOREIGN' and (self.__dict__['reference'] is not None or self.__dict__['constraint'] is not None):
            raise custom_exceptions.ReferenceError('Constraint which is not an external key has the reference')
        elif self.__dict__['reference'] is not None and not self.__getattribute__('reference') in self.table.schema.tables:
            raise custom_exceptions.ReferenceError('Constraint has the reference to the nonexistent table')
        elif self.__dict__['items'] is not None and not self.__getattribute__('items') in self.table.fields:
            raise custom_exceptions.ReferenceError('Constraint is set on the nonexistent field')


class Index:

    def __init__(self, table):
        self.table = table

        self.name = None
        self.field = None
        self.local = None
        self.uniqueness = None
        self.fulltext = None

        self.details = []
        self.table.indexes.append(self)

    def validating(self):
        if self.__dict__['field'] is not None and self.__getattribute__('field') not in self.table.fields:
            raise custom_exceptions.ReferenceError('The index refers to the nonexistent field')
