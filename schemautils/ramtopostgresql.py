import pypyodbc
import psycopg2


class RamToPSData:
    def __init__(self, tables, ddl_file="resources/ps_ddl.sql", ms_server_name="(localdb)\\v11.0",
                 database_name='Northwind',
                 postgresql_user="postgres",
                 postgresql_password='root',
                 is_sql_expr_con=True):
        self.tables = tables
        self.ms_driver = '{SQL Server Native Client 11.0}' if is_sql_expr_con else '{SQL Server}'
        self.connect_ms_dbd = pypyodbc.connect(
            driver=self.ms_driver,
            server=ms_server_name,
            database=database_name,
            trusted_Connection='yes'
        )

        tmp_cursor = psycopg2.connect("dbname='postgres' user='{0}' password='{1}'".format(
            postgresql_user,
            postgresql_password
        )).cursor()
        tmp_cursor.execute("DROP DATABASE IF EXISTS '{0}'".format(database_name))
        tmp_cursor.execute("Create DATABASE IF NOT EXISTS '{0}'".format(database_name))

        self.connect_postgres = psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(
            database_name,
            postgresql_user,
            postgresql_password
        ))
        # Выполнение ddl инструкций и формирование БД в PostgreSQL
        self.connect_postgres.cursor().execute(open(ddl_file, "r").read())

    def transfer(self):
        for table in self.tables:
            self.transfer_table(table.name)

    def transfer_table(self, table):
        table_name = table.name
        fields = [field.name for field in table.fields]
        param = self.get_param(len(fields))
        fields = ", ".join(fields)

        ms_dbd_cursor = self.connect_ms_dbd.cursor()
        ms_dbd_cursor.execute("Select {0} from \"{1}\";".format(fields, table_name))
        ps_cursor = self.connect_postgres.cursor()

        ps_cursor.execute("BEGIN;")
        ps_cursor.execute("ALTER TABLE \"{0}\" DISABLE TRIGGER ALL;".format(table_name))
        row = ms_dbd_cursor.fetchone()
        while row is not None:
            ps_cursor.execute("Insert into \"{0}\" ({1}) VALUES({2});".format(table_name, fields, param), row)
            row = ms_dbd_cursor.fetchone()
        ms_dbd_cursor.close()
        ps_cursor.execute("ALTER TABLE \"{0}\" ENABLE TRIGGER ALL;".format(table_name))
        ps_cursor.execute("COMMIT;")
        ps_cursor.close()

    @staticmethod
    def get_param(count):
        ret = "%s," * count
        return ret[:-1]
