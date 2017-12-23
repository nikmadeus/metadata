"""
The program module with classes for representation of subjects of the scheme in RAM representation
"""


class DatabaseSchema:
    def __init__(self):
        self.id = None
        self.fulltext_engine = None
        self.version = None
        self.name = None
        self.description = None

        self.domains = []
        self.tables = []


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


class Field:
    def __init__(self):

        self.id = None
        self.table_id = None
        self.position = None
        self.name = None
        self.rname = None
        self.description = None
        self.domain = None
        self.can_input = False
        self.can_edit = False
        self.show_in_grid = False
        self.show_in_details = False
        self.is_mean = False
        self.autocalculated = False
        self.required = False
        self.uuid = None


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
        self.full_cascading_delete = False
        self.expression = None
        self.uuid = None


class ConstraintDetail:

    def __init__(self):

        self.id = None
        self.constraint_id = None
        self.position = None
        self.field_id = None


class Index:
    def __init__(self):

        self.id = None
        self.table_id = None
        self.name = None
        self.local = None
        self.kind = None
        self.uuid = None
        self.fulltext = False
        self.uniqueness = False

        self.fields = []


class IndexDetail:

    def __init__(self):

        self.id = None
        self.index_id = None
        self.position = None
        self.field_id = None
        self.expression = None
        self.descend = None
