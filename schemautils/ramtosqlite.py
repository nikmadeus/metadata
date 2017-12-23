from additionalfiles.dbd_const import SQL_DBD_Init
import sqlite3
import uuid


def ramtosqlite(schema, sqlitefile):
    connect = sqlite3.connect(sqlitefile)
    cursor = connect.cursor()

    # Создание таблиц из dbd_const
    cursor.executescript(SQL_DBD_Init)
    print("Database file ", sqlitefile, " with empty tables was successfully created")

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
    cursor.execute(
        """create temporary table tables_tmp (sch_name, name, desc, c_add, can_ed, can_del, tmp_mode, means, uuid)""")

    s_name = schema.name
    for table in schema.tables:
        t_name = table.name
        t_description = table.description
        t_can_add = table.can_add
        t_can_edit = table.can_edit
        t_can_delete = table.can_delete
        t_temporal_mode = table.temporal_mode
        t_means = table.means
        t_uuid = uuid.uuid4().hex

        cursor.execute("insert into tables_tmp values (?,?,?,?,?,?,?,?,?);", (s_name,
                                                                              t_name,
                                                                              t_description,
                                                                              t_can_add,
                                                                              t_can_edit,
                                                                              t_can_delete,
                                                                              t_temporal_mode,
                                                                              t_means,
                                                                              t_uuid))
    cursor.executescript("""insert into dbd$tables select null, s.id, t.name, t.desc, t.c_add, t.can_ed, t.can_del, t.tmp_mode, t.means, t.uuid
                            from tables_tmp t inner join dbd$schemas s on t.sch_name = s.name;

                            DROP table tables_tmp;""")

    # Добавление полей в таблицу dbd$fields
    cursor.execute("""create temporary table fields_tmp (t_name, fi_pos, fi_n, fi_rn, fi_d, fi_d_n, fi_ci, fi_ce,
                      fi_sig, fi_sid, fi_im, fi_ac, fi_req, fi_uuid);""")

    for table in schema.tables:
        t_name = table.name
        num_pos = 0
        for field in table.fields:
            num_pos += 1
            f_name = field.name
            f_rname = field.rname
            f_description = field.description
            if domain.name is not None:
                f_d_name = domain.name
            else:
                f_d_name = None

            f_can_input = field.can_input
            f_can_edit = field.can_edit
            f_sh_in_grid = field.show_in_grid
            f_sh_in_det = field.show_in_details
            f_is_mean = field.is_mean
            f_au_calc = field.autocalculated
            f_required = field.required
            f_uuid = uuid.uuid4().hex

            f_pos = num_pos
            cursor.execute("insert into fields_tmp values (?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                           (t_name, f_pos, f_name, f_rname, f_description, f_d_name, f_can_input, f_can_edit,
                            f_sh_in_grid, f_sh_in_det, f_is_mean, f_au_calc, f_required, f_uuid))

    cursor.executescript("""insert into dbd$fields select null, t.id, fi_pos, fi_n, fi_rn,
                            fi_d, d.id, fi_ci, fi_ce, fi_sig, fi_sid, fi_im, fi_ac, fi_req, fi_uuid
                            from fields_tmp f inner join dbd$tables t on f.t_name = t.name inner join dbd$domains d on f.fi_d_n = d.name;

                            DROP table fields_tmp;""")
    # Добавление ограничений в таблицу dbd$constraints
    cursor.execute("""create temporary table constraints_tmp (t_name, c_id, c_n, c_t, c_ref_t_n, c_hve, c_cd, c_exp, c_uuid);""")

    for table in schema.tables:
        t_name = table.name
        for constraint in table.constraints:
            c_name = constraint.name
            c_con_t = constraint.constraint_type
            c_ref = constraint.reference
            c_un_k_id = constraint.unique_key_id
            c_has_val_ed = constraint.has_value_edit
            c_cas_del = constraint.cascading_delete
            c_expr = constraint.expression
            c_uuid = uuid.uuid4().hex

            cursor.execute("insert into constraints_tmp values (?,?,?,?,?,?,?,?,?);",
                           (t_name, c_name, c_con_t, c_ref, c_un_k_id, c_has_val_ed, c_cas_del, c_expr, c_uuid))
    cursor.executescript("""insert into dbd$constraints select null, t.id, c_id, c_n, c_t, c_ref_t_n, c_hve, c_cd, c_exp, c_uuid
                            from constraints_tmp c inner join dbd$tables t on c.t_name = t.name;

                            DROP table constraints_tmp;""")

    # Добавление индексов в таблицу dbd$indices
    cursor.execute("""create temporary table indices_tmp (t_name, i_n, i_l, i_k, i_uuid);""")

    for table in schema.tables:
        t_name = table.name
        for index in table.indexes:
            i_name = index.name
            i_loc = index.local
            i_kind = index.kind

            i_uuid = uuid.uuid4().hex

            cursor.execute("insert into indices_tmp values (?,?,?,?,?);",
                           (t_name, i_name, i_loc, i_kind, i_uuid))
    cursor.executescript("""insert into dbd$indices select null, t.id, i_n, i_l, i_k, i_uuid
                            from indices_tmp i inner join dbd$tables t on i.t_name = t.name;

                            DROP table indices_tmp;""")

    connect.close()
