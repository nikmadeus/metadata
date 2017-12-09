"""
XML => RAM AND RAM => XML
"""
import argparse
import os.path
import xml.dom.minidom as md
from schemautils import xmltoram, ramtoxml

# TODO: ARGPARSE
from schemautils.postgresql_ddl import createPostgresqlDDL

xml = md.parse("tasks.xml")
xml = md.parse("prjadm.xml")
xml.normalize()

if os.path.exists('tasks.xml') == False and os.path.exists('prjadm.xml') == False:
    print("Error! Xml files does not exist!")
    raise FileNotFoundError
else:
    schema = xmltoram(xml)
    resxml = ramtoxml(schema)
    print(resxml.toprettyxml())

    postgresqlDDL = createPostgresqlDDL(schema)
    print(postgresqlDDL)

    parser = argparse.ArgumentParser()

    parser.add_argument("-x2sq", "--xmltosqlite",
                        help="filepath to db schema xml file that will be parse into sqlite database file "
                             "(currently - into '.db' file) with same location and name", metavar='xml_path')
    parser.add_argument("-sq2x", "--sqlitetoxml",
                        help="filepath to db schema in sqlite db-file that will be parse into xml file",
                        metavar='sqlite_db_to_xml_path')
    parser.add_argument("-ms2ddl", "--mssqltoddl",
                        help="ddl file path - Northwind db in MS SQL Server will be parse into this ddl file",
                        metavar='ddl_file_path')
    parser.add_argument("-ms2psql", "--mssqltopostgresql",
                        help="password - for postgresql user, use transfer between MS Sql Server and PostgreSql ",
                        metavar='pass')
