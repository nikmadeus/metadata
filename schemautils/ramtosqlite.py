from os.path import splitext
import uuid
from dbd_const import SQL_DBD_Init
import sqlite3
from os import remove
from os.path import isfile
import errno
import metadata
import traceback


def silent_rem(filename):
    try:
        remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred


def silent_rem_file(filename):
    if isfile(filename):
        silent_rem(filename)


def init_id_from_seq(seq_result):
    if seq_result is not None:
        return seq_result[0]
    else:
        return 0


class SchemaToSqliteDatabase:
    def __init__(self, db_path_i=None, schema_i=None):
        self.schema = schema_i if schema_i.__class__ == metadata.Schema else metadata.Schema()
        self.db_path_name = splitext(db_path_i)[0] if db_path_i is not None else ""
        self.connect = None
        self.cursor = None

    def create_db_file(self):
        if self.db_path_name != "":
            try:
                silent_rem_file(self.db_path_name + ".db")
                self.connect = sqlite3.connect(self.db_path_name + ".db")
                self.cursor = self.connect.cursor()
                self.cursor.executescript(SQL_DBD_Init)
                print("Database file with empty tables was successfully created")
                return True
            except Exception as ex:
                print("Error occurred! Error:")
                print(ex)
                traceback.print_exc()
                print("Database file with empty tables was not created")
                print("Error catched in 'create_db_file' method of 'SchemaToSqliteDatabase' class")
                return False
        else:
            print("Database path name contains empty string")
            return False

    def _put_schema(self):
        self.cursor.execute("insert into dbd$schemas values (null, ?)", (self.schema.name,))

    def _put_domains(self):
        self.cursor.execute("""create temporary table domains_tmp (do_n, do_d, ty_name, do_l, do_c_l, do_pr,
                       do_sc, do_w, do_al, do_sn, do_sln, do_ts, do_sum, do_cs, do_uuid);""")
        for domain in self.schema.domains:
            d_name = domain.name
            d_description = domain.description
            d_type_name = domain.type
            d_length = domain.length
            d_char_length = domain.char_length
            d_precision = domain.precision
            d_scale = domain.scale
            d_width = domain.width
            d_align = domain.align
            d_show_null = ("show_null" in domain.props)
            d_show_lead_nulls = ("show_lead_nulls" in domain.props)
            d_thousands_separator = ("thousands_separator" in domain.props)
            d_summable = ("summable" in domain.props)
            d_case_sensitive = ("case_sensitive" in domain.props)
            d_uuid = uuid.uuid4().hex
            self.cursor.execute("insert into domains_tmp values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (d_name,
                                                                                                    d_description,
                                                                                                    d_type_name,
                                                                                                    d_length,
                                                                                                    d_char_length,
                                                                                                    d_precision,
                                                                                                    d_scale,
                                                                                                    d_width, d_align,
                                                                                                    d_show_null,
                                                                                                    d_show_lead_nulls,
                                                                                                    d_thousands_separator,
                                                                                                    d_summable,
                                                                                                    d_case_sensitive,
                                                                                                    d_uuid))
        self.cursor.executescript("""insert into dbd$domains select null, d.do_n, d.do_d, t.id, d.do_l, d.do_c_l, d.do_pr,
                          d.do_sc, d.do_w, d.do_al, d.do_sn, d.do_sln, d.do_ts, d.do_sum, d.do_cs, d.do_uuid
                          from domains_tmp d inner join dbd$data_types t on d.ty_name = t.type_id;

                          DROP table domains_tmp;""")
        self.connect.commit()

    def _put_tables(self):
        self.cursor.execute("""create temporary table tables_tmp (sch_name, name, desc, c_add, can_ed, can_del,
                                 tmp_mode, means, uuid)""")
        for table in self.schema.tables:
            t_name = table.name
            t_description = table.description
            t_can_add = ("add" in table.props)
            t_can_edit = ("edit" in table.props)
            t_can_delete = ("delete" in table.props)
            t_temporal_mode = table.temporal_mode
            t_means = table.means
            t_uuid = uuid.uuid4().hex
            self.cursor.execute("insert into tables_tmp values (?,?,?,?,?,?,?,?,?);", (self.schema.name, t_name,
                                                                                       t_description, t_can_add,
                                                                                       t_can_edit, t_can_delete,
                                                                                       t_temporal_mode, t_means,
                                                                                       t_uuid,))
        self.cursor.executescript("""insert into dbd$tables select null, sch.id, t.name, t.desc, t.c_add, t.can_ed,
                                    t.can_del, t.tmp_mode, t.means, t.uuid
                                    from tables_tmp t inner join dbd$schemas sch on t.sch_name = sch.name;

                                  DROP table tables_tmp;""")
        self.connect.commit()

    def _put_fields(self):
        self.cursor.execute("""create temporary table fields_tmp (t_name, fi_pos, fi_n, fi_rn, fi_d, d_name, fi_ci, fi_ce,
                            fi_sig, fi_sid, fi_im, fi_ac, fi_req, fi_uuid,
                            d_ty_name, d_l, d_c_l, d_pr, d_sc, d_w, d_al, d_sn, d_sln, d_ts, d_sum, d_cs);""")
        for table in self.schema.tables:
            t_name = table.name
            for fld_name, fld_obj in table.fields.items():
                f_name = fld_name
                f_rname = fld_obj.rname
                f_description = fld_obj.description
                f_d_name = fld_obj.domain_name

                if f_d_name == "":
                    f_d_name = None
                d_type_name = fld_obj.domain.type
                d_length = fld_obj.domain.length
                d_char_length = fld_obj.domain.char_length
                d_precision = fld_obj.domain.precision
                d_scale = fld_obj.domain.scale
                d_width = fld_obj.domain.width
                d_align = fld_obj.domain.align
                d_show_null = ("show_null" in fld_obj.domain.props)
                d_show_lead_nulls = ("show_lead_nulls" in fld_obj.domain.props)
                d_thousands_separator = ("thousands_separator" in fld_obj.domain.props)
                d_summable = ("summable" in fld_obj.domain.props)
                d_case_sensitive = ("case_sensitive" in fld_obj.domain.props)

                f_can_input = ("input" in fld_obj.props)
                f_can_edit = ("edit" in fld_obj.props)
                f_sh_in_grid = ("show_in_grid" in fld_obj.props)
                f_sh_in_det = ("show_in_details" in fld_obj.props)
                f_is_mean = ("is_mean" in fld_obj.props)
                f_au_calc = ("autocalculated" in fld_obj.props)
                f_required = ("required" in fld_obj.props)
                f_uuid = uuid.uuid4().hex

                f_pos = fld_obj.position
                self.cursor.execute("insert into fields_tmp values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
                                    "?,?);", (t_name, f_pos, f_name, f_rname, f_description, f_d_name, f_can_input,
                                              f_can_edit, f_sh_in_grid, f_sh_in_det, f_is_mean, f_au_calc, f_required,
                                              f_uuid, d_type_name, d_length, d_char_length, d_precision, d_scale,
                                              d_width, d_align, d_show_null, d_show_lead_nulls, d_thousands_separator,
                                              d_summable, d_case_sensitive))
        self.cursor.executescript("""insert into dbd$domains select distinct null, null, null, ty.id, f.d_l,
                                       f.d_c_l, f.d_pr, f.d_sc, f.d_w, f.d_al, f.d_sn, f.d_sln, f.d_ts, f.d_sum,
                                       f.d_cs, null
                                       from fields_tmp f inner join dbd$data_types ty on f.d_ty_name = ty.type_id
                                       where d_name is NULL;
                                     insert into dbd$fields select
                                       null, fields.id as _table_id, fi_pos, fi_n, fi_rn,
                                       fi_d, domains.id as _d_id, fi_ci, fi_ce, fi_sig, fi_sid, fi_im, fi_ac,
                                       fi_req, fi_uuid
                                       from (fields_tmp
                                         inner join dbd$tables on fields_tmp.t_name = dbd$tables.name) fields
                                       inner join (
                                         select dbd$domains.*, dbd$data_types.id as t_id, dbd$data_types.type_id
                                         from dbd$domains, dbd$data_types
                                         where dbd$domains.data_type_id = dbd$data_types.id) domains on
                                       (fields_tmp.d_name = domains.name)
                                       or (fields_tmp.d_name is NULL
                                       and fields_tmp.d_ty_name = domains.type_id
                                       and ifnull(fields_tmp.d_l, "NULL") = ifnull(domains.length, "NULL")
                                       and ifnull(fields_tmp.d_c_l, "NULL") = ifnull(domains.char_length, "NULL")
                                       and ifnull(fields_tmp.d_pr, "NULL") = ifnull(domains.precision, "NULL")
                                       and ifnull(fields_tmp.d_sc, "NULL") = ifnull(domains.scale, "NULL")
                                       and ifnull(fields_tmp.d_w, "NULL") = ifnull(domains.width, "NULL")
                                       and ifnull(fields_tmp.d_al, "NULL") = ifnull(domains.align, "NULL")
                                       and ifnull(fields_tmp.d_sn, "NULL") = ifnull(domains.show_null, "NULL")
                                       and ifnull(fields_tmp.d_sln, "NULL") = ifnull(domains.show_lead_nulls, "NULL")
                                       and ifnull(fields_tmp.d_ts, "NULL") = ifnull(domains.thousands_separator, "NULL")
                                       and ifnull(fields_tmp.d_sum, "NULL") = ifnull(domains.summable, "NULL")
                                       and ifnull(fields_tmp.d_cs, "NULL") = ifnull(domains.case_sensitive, "NULL"));

                                     DROP TABLE fields_tmp;""")
        self.connect.commit()

    def _put_constraints(self):
        self.cursor.executescript("""create temporary table constraints_tmp (c_id, c_t_name, c_n, c_t, c_ref_t_n, c_hve, c_cd,c_exp,c_uuid);
                                     create temporary table con_details_tmp (cd_c_id, cd_pos, f_name, c_t_name);""")
        c_id = self.cursor.execute("SELECT seq from sqlite_sequence where name = 'dbd$constraints'").fetchone()
        self.cursor.execute("UPDATE sqlite_sequence set seq = seq + ? where name = 'dbd$constraints'",
                            (self.schema.con_num,)).fetchone()
        self.connect.commit()
        c_id = init_id_from_seq(c_id)
        for table in self.schema.tables:
            con_pos = 0
            t_constraints = table.pr_constraints + table.fr_constraints + table.ch_constraints
            t_name = table.name
            for t_constraint in t_constraints:
                c_id += 1
                c_name = t_constraint.name
                c_type = t_constraint.const_type
                c_ref_t_n = getattr(t_constraint, "ref_name", None)
                c_has_v_ed = ("has_value_edit" in getattr(t_constraint, "props", ""))
                if c_type == "FOREIGN":
                    c_cas_del = ("cascading_delete" in t_constraint.props)
                else:
                    c_cas_del = None
                c_expr = getattr(t_constraint, "expression", None)
                c_uuid = uuid.uuid4().hex
                self.cursor.execute("insert into constraints_tmp values (?,?,?,?,?,?,?,?,?);", (c_id, t_name,
                                                                                                c_name, c_type,
                                                                                                c_ref_t_n, c_has_v_ed,
                                                                                                c_cas_del, c_expr,
                                                                                                c_uuid))
                con_pos += 1
                con_f_name = t_constraint.item_name
                self.cursor.execute("insert into con_details_tmp values (?,?,?,?);",
                                    (c_id, con_pos, con_f_name, t_name))
        self.connect.commit()
        self.cursor.executescript("""insert into dbd$constraints
                                       select con.c_id, t.id, con.c_n, con.c_t, ca.c_id,
                                        con.c_hve, con.c_cd, con.c_exp, con.c_uuid
                                       from (constraints_tmp con left join (select c_id, c_t_name
                                         from constraints_tmp where c_t="PRIMARY") ca on con.c_ref_t_n=ca.c_t_name)
                                       inner join dbd$tables t on con.c_t_name=t.name;

                                     insert into dbd$constraint_details
                                       select null, cd_tabl.c_id, cd_tabl.pos, f.id
                                       from (select cd.cd_c_id c_id, cd.cd_pos pos, cd.f_name, tabls.id tab_id
                                         from con_details_tmp cd
                                         inner join dbd$tables tabls
                                           on cd.c_t_name = tabls.name) cd_tabl
                                         inner join dbd$fields f
                                           on cd_tabl.f_name = f.name
                                           and cd_tabl.tab_id = f.table_id;

                                     DROP TABLE constraints_tmp;
                                     DROP TABLE con_details_tmp;""")
        self.connect.commit()

    def _put_indices(self):
        self.cursor.executescript("""create temporary table indices_tmp (ind_id, ind_t_name, ind_name, ind_loc, 
        ind_kind, ind_uuid); create temporary table ind_details_tmp (ind_d_ind_id, ind_d_pos, ind_d_f_name, 
        ind_d_t_name, ind_d_expr, ind_d_desc);""")
        in_id = self.cursor.execute("SELECT seq from sqlite_sequence where name = 'dbd$indices'").fetchone()
        self.cursor.execute("UPDATE sqlite_sequence set seq = seq + ? where name = 'dbd$indices'",
                            (self.schema.ind_num,)).fetchone()
        self.connect.commit()
        in_id = init_id_from_seq(in_id)
        for table in self.schema.tables:
            ind_pos = 0
            t_name = table.name
            t_indices = table.indices
            for t_index in t_indices:
                in_id += 1
                in_name = t_index.name
                in_loc = ("local" in t_index.props)
                in_kind = next((x for x in ("uniqueness", " fulltext", " simple") if x in t_index.props.lower()), "simple")
                in_uuid = uuid.uuid4().hex
                self.cursor.execute("insert into indices_tmp values (?,?,?,?,?,?);", (in_id, t_name, in_name,
                                                                                      in_loc, in_kind, in_uuid))
                ind_pos += 1
                in_f_name = t_index.field_name
                in_expr = t_index.expression
                in_desc = ("descend" in t_index.props)
                self.cursor.execute("insert into ind_details_tmp values (?,?,?,?,?,?);", (in_id, ind_pos,
                                                                                          in_f_name, t_name, in_expr,
                                                                                          in_desc))

        self.cursor.executescript("""insert into dbd$indices select i.ind_id, t.id, i.ind_name,
                                       i.ind_loc, i.ind_kind, i.ind_uuid
                                       from indices_tmp i inner join dbd$tables t on i.ind_t_name=t.name;

                                     insert into dbd$index_details select null, id.ind_d_ind_id, id.ind_d_pos, f_t.f_id,
                                       id.ind_d_expr, id.ind_d_desc
                                       from ind_details_tmp id inner join (select f.id as f_id, f.name as f_name,
                                         t.name as t_name from dbd$fields f inner join dbd$tables t
                                         on f.table_id=t.id) f_t on id.ind_d_f_name = f_t.f_name
                                           and id.ind_d_t_name=f_t.t_name;

                                     DROP TABLE indices_tmp;
                                     DROP TABLE ind_details_tmp;;""")
        self.connect.commit()

    def create_schema_db(self):
        if self.create_db_file():
            try:
                self._put_schema()
                self._put_domains()
                self._put_tables()
                self._put_fields()
                self._put_constraints()
                self._put_indices()
                self.connect.commit()
                print("Database schema was successfully writen into '.db' file.")
                return True

            except Exception as ex:
                print("Error occurred!")
                print(ex)
                traceback.print_exc()
                print("Invalid db file was created!")
                print("Error was in 'create_schema_db' method of 'SchemaToSqliteDatabase' class")
                return False
        else:
            print('Error - database file was not created')
            return False
