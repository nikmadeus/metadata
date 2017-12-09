"""
Модуль с классами представления схемы базы в RAM.
validating() - функция валидации(проверки на соответствие аттрибутов)
"""


class DatabaseSchema:
    def __init__(self):
        self.fulltext_engine = None
        self.version = None
        self.name = None
        self.description = None

        self.domains = []
        self.tables = []

    # def validating(self):
    #     if self.__dict__['name'] is not None:
    #         raise Exception('The schema name is not defined')


class Domain:
    def __init__(self):

        self.id = None
        self.name = None
        self.type = None
        self.description = None
        self.data_type_id = None
        self.length = None
        self.char_length = None
        self.precision = None
        self.scale = None
        self.width = None
        self.align = None
        self.show_null = False
        self.show_lead_nulls = False
        self.thousands_separator = False
        self.summable = False
        self.case_sensitive = False
        self.uuid = None

    # def validating(self):
    #     if self.__dict__['name'] is not None:
    #         raise Exception('The domain name is not defined')
    #     if self.__dict__['type'] is not None:
    #         raise Exception('The domain type is not defined ' + str(self.__getattribute__('name')))


class Table:
    def __init__(self):

        self.id = None
        self.schema_id = None
        self.name = None
        self.description = None
        self.can_add = False
        self.can_edit = False
        self.can_delete = False
        self.temporal_mode = None
        self.means = None
        self.uuid = None

        self.fields = []
        self.constraints = []
        self.indexes = []

    # def validating(self):
    #     if self.__dict__['name'] is not None:
    #         raise Exception('The table name is not defined')


class Field:
    def __init__(self):

        self.id = None
        self.table_id = None
        self.position = None
        self.name = None
        self.russian_short_name = None
        self.description = None
        self.domain_id = None
        self.can_input = False
        self.can_edit = False
        self.show_in_grid = False
        self.show_in_details = False
        self.is_mean = False
        self.autocalculated = False
        self.required = False
        self.uuid = None

    # def validating(self):
    #     if self.__dict__['name'] is None:
    #         raise Exception('The field name is not defined')


class Constraint:
    def __init__(self):

        self.id = None
        self.table_id = None
        self.name = None
        self.constraint_type = None
        self.reference = None
        self.unique_key_id = None
        self.has_value_edit = False
        self.cascading_delete = False
        self.expression = None
        self.uuid = None

    # def validating(self):
    #     if self.__dict__['constraint_type'] is not None:
    #         raise Exception('Constraint type is not defined')
    #     elif self.__getattribute__('constraint_type') != 'FOREIGN' and self.__dict__['reference'] is not None:
    #         raise Exception('Constraint which is not an external key has the reference')


class ConstraintDetail:

    def __init__(self):

        self.id = None
        self.constraint_id = None
        self.position = None
        self.field_id = None

    def validating(self):
        if not self.constraint_id or not self.field_id:
            self.__dict__ = None
            raise Exception('Attributes constraind_id and field_id are not found')


class Index:
    def __init__(self):

        self.id = None
        self.table_id = None
        self.name = None
        self.local = None
        self.kind = None
        self.uuid = None

        self.fields = []

    # def validating(self):
    #     if self.__dict__['name'] is not None:
    #         raise Exception('Index name is not defined')


class IndexDetail:

    def __init__(self):

        self.id = None
        self.index_id = None
        self.position = None
        self.field_id = None
        self.expression = None
        self.descend = None

    def validating(self):
        if not self.index_id or not self.field_id:
            self.__dict__ = None
            raise Exception('Attributes index_id and field_id are not found')
