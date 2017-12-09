from itertools import count

from additionalfiles.dbd_const import SQL_DBD_Init

def ram2sqlite(schema, connect):

    cursor = connect.cursor()

    # Создание (и иногда заполнение) таблиц:
    # dbd$constraint_details
    # dbd$constraints
    # dbd$data_types
    # dbd$domains
    # dbd$fields
    # dbd$index_details
    # dbd$indices
    # dbd$schemas
    # dbd$settings
    # dbd$tables
    cursor.executescript(SQL_DBD_Init)

    # Добавление схемы в таблицу dbd$schemas
    cursor.execute("INSERT INTO dbd$schemas (name) VALUES ('{}')".format(schema.name))

    # Заполнение таблицы dbd$domains (для поля data_type_id заглушка 1)
    # ai - итератор для заполнения uuid
    ai = count()
    cursor.executemany(
    """INSERT INTO dbd$domains (
        name,
        description,
        length,
        char_length,
        precision,
        scale,
        width,
        align,
        show_null,
        show_lead_nulls,
        thousands_separator,
        summable,
        case_sensitive,
        data_type_id,
        uuid)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [(
            d.name,
            d.descr,
            d.length,
            d.char_length,
            d.precision,
            d.scale,
            d.width,
            d.align,
            d.show_null,
            d.show_lead_nulls,
            d.thousands_separator,
            d.summable,
            d.case_sensitive,
            1,
            next(ai)
        ) for d in schema.domains]
    )
    # Создание (временной) таблицы dbd$TMP__REL__Domain__DataType хранящей отношение имени домена и имени типа данных
    cursor.execute("CREATE TABLE dbd$TMP__REL__Domain__DataType(domain_name varchar NOT NULL, datatype_name varchar NOT NULL)")
    # Заполнение таблицы dbd$TMP__REL__Domain__DataType
    cursor.executemany("INSERT INTO dbd$TMP__REL__Domain__DataType VALUES(?, ?)", [(d.name, d.type) for d in schema.domains])
    # Заполнение поля data_type_id в таблице dbd$domains при помощи временной таблицы
    # dbd$TMP__REL__Domain__DataType (join'ы все дела)
    cursor.execute("""
    UPDATE dbd$domains
    SET data_type_id = (
    SELECT dbd$data_types.id
    FROM dbd$domains as dom
    JOIN dbd$TMP__REL__Domain__DataType
    ON dbd$domains.name = dbd$TMP__REL__Domain__DataType.domain_name
    JOIN dbd$data_types
    ON dbd$TMP__REL__Domain__DataType.datatype_name = dbd$data_types.type_id
    WHERE dom.name = name)
    """)
    # Удаление таблицы dbd$TMP__REL__Domain__DataType
    cursor.execute("DROP TABLE dbd$TMP__REL__Domain__DataType")

    connect.commit()