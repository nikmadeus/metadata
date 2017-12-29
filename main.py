"""
The main module for work with the scheme of databases
"""
import argparse
import os.path
import xml.dom.minidom as md

import psycopg2
import pypyodbc
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from schemautils.xmltoram import xmltoram
from schemautils.ramtoxml import ramtoxml
from schemautils.ramtosqlite import ramtosqlite
from schemautils.sqlitetoram import sqlitetoram
from schemautils.postgresql_ddl import genPSDDL
from schemautils.mssqltoram import mssqltoram

# xmlfile = "resources/tasks.xml"
xmlfile = "resources/prjadm.xml"
sqlitefile = "resources/sqlite.db"
ps_ddl_path = "resources/ps_ddl.sql"
ms_path = "resources/northwind.sql"
database_name = "Northwind"
postgresql_user = "postgres"
postgresql_password = 'root'
ms_server_name="(localdb)\\v11.0"

# Parsing
if not os.path.exists(xmlfile):
    print("Error! XML file ", xmlfile, " does not exist!")
    raise FileNotFoundError
else:
    xml = md.parse(xmlfile)
    print("XML file path: ", os.path.abspath(xmlfile))

    # xml to ram
    schema = xmltoram(xml)

    # ram to xml
    resXML = ramtoxml(schema)
    resXML.normalize()
    print("XML file test_prjadm.xml with schema was created!")
    # print(resxml.toprettyxml())
    print("")

# Databases

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
    print("Error! Database ", sqlitefile, " not found!")
    print("SQLite -> RAM failed!")

# PosgreSQL DDL instructions
resDDL = genPSDDL(schema)
print(resDDL)
connect = psycopg2.connect("dbname='postgres' user='{0}' password='{1}'".format(
            postgresql_user,
            postgresql_password
        ))
connect.autocommit = True
tmp_curs = connect.cursor()
tmp_curs.execute("DROP DATABASE IF EXISTS '{0}'".format(database_name))
tmp_curs.execute("Create DATABASE IF NOT EXISTS '{0}'".format(database_name))
connect_postgres = psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(
    database_name,
    postgresql_user,
    postgresql_password
))
with connect_postgres.cursor() as cursor:
    cursor.execute(open(ps_ddl_path, "r").read())

# MS SQL to ram
if os.path.exists(ms_path):
    print("File ", ms_path, " is founded!")
    schema = mssqltoram()
    print(schema.name)


parser = argparse.ArgumentParser(description="The program is ready to use")
#
# parser.add_argument("-x2sq", "--xmltosqlite",
#                     help="filepath to db schema xml file which will be parse into sqlite database file "(currently - into '.sqlite' file) with same location and name", metavar='xml_path')
# parser.add_argument("-sq2x", "--sqlitetoxml",
#                     help="filepath to db schema in sqlite db-file which will be parse into xml file", metavar='sqlite_db_to_xml_path')
# parser.add_argument("-ms2ddl", "--mssqltoddl",
#                     help="ddl file path - Northwind db in MS SQL Server which will be parse into this ddl file", metavar='ddl_file_path')
# parser.add_argument("-ms2psql", "--mssqltopostgresql", help="password - for postgresql user, use transfer between MS Sql Server and PostgreSql ", metavar='pass')

# args = parser.parse_args()
# was_no_arguments = True
# if args.xmltosqlite:
#     parse_xml(args.xmltosqlite)
#     was_no_arguments = False
# if args.sqlitetoxml:
#     parse_sq_schema(args.sqlitetoxml)
#     was_no_arguments = False
# if args.mssqltoddl:
#     parse_mssql(args.mssqltoddl)
#     was_no_arguments = False
# if args.mssqltopostgresql:
#     transfer_mssql_psql(args.mssqltopostgresql)
#     was_no_arguments = False
# if was_no_arguments:
#     print("No arguments")
#     parser.print_help()
