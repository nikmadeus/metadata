import re, os
from xml.dom.minidom import parse, parseString


class xmltoddl:
    def __init__(self):
        self.ddlInterface = None
        self._setDefaults()
        self.reset()

    def reset(self):
        self.ddls = []

    def _setDefaults(self):
        self.dbmsType = 'postgres'
        self.params = {
            'drop-tables': True,
            'output_primary_keys': True,
            'output_references': True,
            'output_indexes': True,
            'add_dataset': True,
        }

    def createTables(self, xml):
        self.ddls = []

        tbls = xml.getElementsByTagName('table')

        for tbl in tbls:
            self.createTable(tbl)

        xml.unlink()
        return self.ddls