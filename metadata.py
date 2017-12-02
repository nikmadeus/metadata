"""
Модуль с классами представления базы в RAM.
validating() - функция валидации(проверки на соответствие аттрибутов)
"""


class ShowException(Exception):
    print(Exception)
    pass


class DatabaseSchema:
    def __init__(self):
        self.fulltext_engine = None
        self.version = None
        self.name = None
        self.description = None

        self.domains = []
        self.tables = []

    def validating(self):
        if self.__getattribute__('name') is None:
            raise ShowException('The schema name is not defined')


class Domain:
    def __init__(self):

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
            raise ShowException('The domain name is not defined')
        if self.__getattribute__('type') is None:
            raise ShowException('The domain type is not defined ' + str(self.__getattribute__('name')))


class Table:
    def __init__(self):

        self.id = None
        self.schema_id = None
        self.name = None
        self.description = None
        self.can_add = None
        self.can_edit = None
        self.can_delete = None
        self.temporal_mode = None
        self.means = None
        self.uuid = None

        self.fields = []
        self.constraints = []
        self.indexes = []

    def validating(self):
        if self.__getattribute__('name') is None:
            raise ShowException('The table name is not defined')
        if self.__getattribute__('name') in self.schema.tables:
            raise ShowException('Table ' + str(self.__getattribute__('name')) + ' already exists')


class Field:
    def __init__(self):

        self.id = None
        self.table_id = None
        self.position = None
        self.name = None
        self.russian_short_name = None
        self.description = None
        self.domain_id = None
        self.can_input = None
        self.can_edit = None
        self.show_in_grid = None
        self.show_in_details = None
        self.is_mean = None
        self.autocalculated = None
        self.required = None
        self.uuid = None

    def validating(self):
        if self.__dict__['name'] is None:
            raise ShowException('The field name is not defined')
        if self.__getattribute__('name') in self.table.fields:
            raise ShowException('Field ' + str(self.__getattribute__('name')) + ' already exists')
        if self.__dict__['domain'] is None and self.__dict__['type'] is None:
            raise ShowException('Domain and type of field ' + str(self.__getattribute__('name')) + ' are not defined')


# class Constraint:
#     def __init__(self):
#
#         self.id = None
#         self.table_id = None
#         self.name = None
#         self.constraint_type = None
#         self.reference = None
#         self.unique_key_id = None
#         self.has_value_edit = None
#         self.cascading_delete = None
#         self.expression = None
#         self.uuid = None
#
#     def validating(self):
#         if 'constraint_type' not in self.__dict__:
#             raise ShowException('Constraint type of the table is not defined')
#         elif self.__getattribute__('constraint_type') == 'PRIMARY' and any([key for key in self.table.constraints if key.__getattribute__('constraint_type') == 'PRIMARY' and key != self]):
#             raise ShowException('More than one primary key are defined')
#         elif self.__getattribute__('constraint_type') != 'FOREIGN' and (self.__dict__['reference'] is not None or self.__dict__['constraint'] is not None):
#             raise ShowException('Constraint which is not an external key has the reference')
#         elif self.__dict__['items'] is not None and not self.__getattribute__('items') in self.table.fields:
#             raise ShowException('Constraint is set on the nonexistent field')


class PrimaryConstraint:
    const_type = "PRIMARY"

    def __init__(self, item_i=None, name_i=None):
        if type(item_i) == str:
            self.item_name = item_i
            self.item = None
        else:
            if type(item_i) == Field:
                self.item_name = item_i.name
                self.item = item_i
            else:
                self.item_name = None
                self.item = None
        self.name = name_i


class ForeignConstraint:
    const_type = "FOREIGN"

    def __init__(self, item_i=None, ref_item=None, props_i="", name_i=None):
        if type(item_i) == str:
            self.item_name = item_i
            self.item = None
        else:
            if type(item_i) == Field:
                self.item_name = item_i.name
                self.item = item_i
            else:
                self.item_name = None
                self.item = None
        if type(ref_item) == str:
            self.ref_name = ref_item
            self.reference = None
        else:
            if type(ref_item) == Table:
                self.ref_name = ref_item.name
                self.reference = ref_item
            else:
                self.ref_name = None
                self.ref_item = None
        self.props = props_i
        self.name = name_i

        self.position = None


class CheckConstraint:
    const_type = "CHECK"

    def __init__(self, expression_i="", field_item=None, name_i=None):
        self.expression = expression_i
        self.name = name_i
        if field_item.__class__ == Field:
            self.item = field_item
            self.item_name = field_item.name
        else:
            if field_item.__class__ == str:
                self.item = None
                self.item_name = field_item
            else:
                self.item = None
                self.item_name = None


# class ConstraintDetail:
#     def __init__(self):
#         self.id = None
#         self.constraint_id = None
#         self.position = None
#         self.field_id = None
#
#     def validating(self):
#         if not self.constraint_id or not self.field_id:
#             self.__dict__ = None
#             raise ShowException('')


class Index:
    def __init__(self):
        self.id = None
        self.table_id = None
        self.name = None
        self.local = None
        self.kind = None
        self.uuid = None

        self.fields = []

    def validating(self):
        if self.__dict__['field'] is not None and self.__getattribute__('field') not in self.table.fields:
            raise ShowException('The index refers to the nonexistent field')


# class IndexDetail:
#     def __init__(self):
#         self.id = None
#         self.index_id = None
#         self.position = None
#         self.field_id = None
#         self.expression = None
#         self.descend = None
#
#     def validating(self):
#         if not self.index_id or not self.field_id:
#             self.__dict__ = None
#             raise ShowException('')
