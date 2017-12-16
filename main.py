"""
XML => RAM AND RAM => XML
"""
import argparse
import os.path
import xml.dom.minidom as md

from schemautils.xmltoram import xmltoram
from schemautils.ramtoxml import ramtoxml
from schemautils.ramtosqlite import ramtosqlite
from schemautils.sqlitetoram import sqlitetoram
from schemautils.postgresql_ddl import genPSDDL
from schemautils.mssqltoram import mssqltoram

xmlfile = "prjadm.xml"
sqlitefile = "sqlite.db"
mssqlfile = "resources/northwind.sql"

if not os.path.exists(xmlfile):
    print("Error! XML file ", xmlfile, " does not exist!")
    raise FileNotFoundError
else:
    xml = md.parse(xmlfile)
    print("XML file path: ", os.path.abspath(xmlfile))

    # xml to ram
    schema = xmltoram(xml)

    # ram to xml
    resxml = ramtoxml(schema)
    resxml.normalize()
    print(resxml.toprettyxml())

# ram to sqlite
if os.path.exists(sqlitefile):
    print("Database ", sqlitefile, " already exists!")
    os.remove(sqlitefile)
    print("Database ", sqlitefile, " removed!")

ramtosqlite(schema, sqlitefile)
print("Database created succesfully!")
print("Database path: ", os.path.abspath(sqlitefile))
print("")

# sqlite to ram
if os.path.exists(sqlitefile):
    sqlitetoram(sqlitefile)
else:
    print("Error! Database not found!")
    print("SQLite -> RAM failed!")

# generation PosgreSQL instructions
resDDL = genPSDDL(schema)
print(resDDL)
print("")

if os.path.exists(mssqlfile):
    print("Database ", mssqlfile, " is founded!")
    # mssql to ram
    # res = mssqltoram(schema, mssqlfile)
    # print(res)

parser = argparse.ArgumentParser(description="You can work with schema for database using different modules.")
#
# parser.add_argument("-x2sq", "--xmltosqlite",
#                     help="filepath to db schema xml file which will be parse into sqlite database file "
#                          "(currently - into '.db' file) with same location and name",
#                     metavar='xml_path')
# parser.add_argument("-sq2x", "--sqlitetoxml",
#                     help="filepath to db schema in sqlite db-file which will be parse into xml file",
#                     metavar='sqlite_db_to_xml_path')
# parser.add_argument("-ms2ddl", "--mssqltoddl",
#                     help="ddl file path - Northwind db in MS SQL Server which will be parse into this ddl file",
#                     metavar='ddl_file_path')
# parser.add_argument("-ms2psql", "--mssqltopostgresql",
#                     help="password - for postgresql user, use transfer between MS Sql Server and PostgreSql ",
#                     metavar='pass')

# args = parser.parse_args()
# no_arguments = True
# if args.xmltosqlite:

#     no_arguments = False
# if args.sqlitetoxml:

#     no_arguments = False
# if args.mssqltoddl:

#     no_arguments = False
# if args.mssqltopostgresql:

#     no_arguments = False
# if no_arguments:
#     print("No arguments")
#     parser.print_help()
