import sqlite3
from additionalfiles.dbd_const import SQL_DBD_Init
import uuid


def ramtosqlite(schema, sqlitefile):
    connect = sqlite3.connect(sqlitefile)
    cursor = connect.cursor()

    # Создание таблиц из dbd_const
    cursor.executescript(SQL_DBD_Init)
    print("Database file with empty tables was successfully created")

    # Заполнение таблиц из внутреннего представления
    # Добавление схемы в таблицу dbd$schemas
    cursor.execute("insert into dbd$schemas (name) values ('{}')".format(schema.name))

    # Добавление доменов в таблицу dbd$domains
    cursor.execute("""create temporary table domains_tmp (do_n, do_d, ty_name, do_l, do_c_l, do_pr,
                           do_sc, do_w, do_al, do_sn, do_sln, do_ts, do_sum, do_cs, do_uuid);""")

    for domain in schema.domains:
        d_name = domain.name
        d_description = domain.description
        d_type_name = domain.type
        d_length = domain.length
        d_char_length = domain.char_length
        d_precision = domain.precision
        d_scale = domain.scale
        d_width = domain.width
        d_align = domain.align
        d_show_null = domain.show_null
        d_show_lead_nulls = domain.show_lead_nulls
        d_thousands_separator = domain.thousands_separator
        d_summable = domain.summable
        d_case_sensitive = domain.case_sensitive
        d_uuid = uuid.uuid4().hex

        cursor.execute("insert into domains_tmp values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (d_name,
                                                                                           d_description,
                                                                                           d_type_name,
                                                                                           d_length,
                                                                                           d_char_length,
                                                                                           d_precision,
                                                                                           d_scale,
                                                                                           d_width,
                                                                                           d_align,
                                                                                           d_show_null,
                                                                                           d_show_lead_nulls,
                                                                                           d_thousands_separator,
                                                                                           d_summable,
                                                                                           d_case_sensitive,
                                                                                           d_uuid))
    cursor.executescript("""insert into dbd$domains select null, d.do_n, d.do_d, t.id, d.do_l, d.do_c_l, d.do_pr,
                            d.do_sc, d.do_w, d.do_al, d.do_sn, d.do_sln, d.do_ts, d.do_sum, d.do_cs, d.do_uuid
                            from domains_tmp d inner join dbd$data_types t on d.ty_name = t.type_id;

                            DROP table domains_tmp;""")

    # Добавление таблиц в таблицу dbd$tables
    cursor.execute("""create temporary table tables_tmp (sch_name, name, desc, c_add, can_ed, can_del, tmp_mode, means, uuid)""")
    for table in schema.tables:
        t_name = table.name
        t_description = table.description
        t_can_add = table.can_add
        t_can_edit = table.can_edit
        t_can_delete = table.can_delete
        t_temporal_mode = table.temporal_mode
        t_means = table.means
        t_uuid = uuid.uuid4().hex

        cursor.execute("insert into tables_tmp values (?,?,?,?,?,?,?,?,?);", (schema.name,
                                                                              t_name,
                                                                              t_description,
                                                                              t_can_add,
                                                                              t_can_edit,
                                                                              t_can_delete,
                                                                              t_temporal_mode,
                                                                              t_means,
                                                                              t_uuid))
    cursor.executescript("""insert into dbd$tables select null, sch.id, t.name, t.desc, t.c_add, t.can_ed, t.can_del,
                            t.tmp_mode, t.means, t.uuid from tables_tmp t inner join dbd$schemas sch on t.sch_name = sch.name;

                            DROP table tables_tmp;""")

    # Добавление полей в таблицу dbd$fields
    # cursor.execute("""create temporary table fields_tmp (t_name, fi_n, fi_rn, fi_d, d_name, fi_ci, fi_ce,
    #                             fi_sig, fi_sid, fi_im, fi_ac, fi_req, fi_uuid,
    #                             d_ty_name, d_l, d_c_l, d_pr, d_sc, d_w, d_al, d_sn, d_sln, d_ts, d_sum, d_cs);""")

    # for field in table.fields:
    #     t_name = table.name
    #     f_name = field.name
    #     f_rname = field.russian_short_name
    #     f_description = field.description
    #     f_d_name = domain.name
    #     if f_d_name == "":
    #         f_d_name = None
    #     d_type_name = domain.type
    #     d_length = domain.length
    #     d_char_length = domain.char_length
    #     d_precision = domain.precision
    #     d_scale = domain.scale
    #     d_width = domain.width
    #     d_align = domain.align
    #
    #     d_show_null = domain.show_null
    #     d_show_lead_nulls = domain.show_lead_nulls
    #     d_thousands_separator = domain.thousands_separator
    #     d_summable = domain.summable
    #     d_case_sensitive = domain.case_sensitive
    #
    #     f_can_input = field.can_input
    #     f_can_edit = field.can_edit
    #     f_sh_in_grid = field.show_in_grid
    #     f_sh_in_det = field.show_in_details
    #     f_is_mean = field.is_mean
    #     f_au_calc = field.autocalculated
    #     f_required = field.required
    #     f_uuid = uuid.uuid4().hex
    #
    #     # f_pos = field.position
    #     cursor.execute("insert into dbd$fields values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
    #                    (t_name, f_name, f_rname, f_description, f_d_name, f_can_input,
    #                     f_can_edit, f_sh_in_grid, f_sh_in_det, f_is_mean, f_au_calc, f_required,
    #                     f_uuid, d_type_name, d_length, d_char_length, d_precision, d_scale,
    #                     d_width, d_align, d_show_null, d_show_lead_nulls, d_thousands_separator,
    #                     d_summable, d_case_sensitive))



    # for t in schema.tables:
    #     cursor.execute(
    #         """INSERT INTO dbd$fields (
    #             name,
    #             rname,
    #             description,
    #             domain,
    #             can_input,
    #             can_edit,
    #             show_in_grid,
    #             show_in_details,
    #             is_mean,
    #             aucalculated,
    #             uuid
    #             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    #         [(
    #             f.name,
    #             f.rname,
    #             f.description,
    #             f.domain,
    #             f.can_input,
    #             f.can_edit,
    #             f.show_in_grid,
    #             f.show_in_details,
    #             f.is_mean,
    #             f.autocalculated,
    #             f.uuid
    #         ) for f in t.fields]
    #     )

    connect.close()
