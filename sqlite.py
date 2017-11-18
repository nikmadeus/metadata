import sqlite3
con = sqlite3.connect('dbd_const.db')

try:
    c = con.cursor()

    # Create table
    # c.execute('''create table dbd$schemas (
    #     id integer primary key autoincrement not null,
    #     name varchar not null)''')


    # сделать открытие транзакции и ее закрытие
    # c.execute("begin transaction;")
    c.execute("begin")

    c.executescript("""
        pragma foreign_keys = on;
    
    create table dbd$schemas (
        id integer primary key autoincrement not null,
        name varchar not null -- имя схемы
    );
    
    create table dbd$domains (
        id  integer primary key autoincrement default(null),
        name varchar unique default(null),  -- имя домена
        description varchar default(null),  -- описание
        data_type_id integer not null,      -- идентификатор типа (dbd$data_types)
        length integer default(null),       -- длина
        char_length integer default(null),  -- длина в символах
        precision integer default(null),    -- точность
        scale integer default(null),        -- количество знаков после запятой
        width integer default(null),        -- ширина визуализации в символах
        align char default(null),           -- признак выравнивания
        show_null boolean default(null),    -- нужно показывать нулевое значение?
        show_lead_nulls boolean default(null),      -- следует ли показывать лидирующие нули?
        thousands_separator boolean default(null),  -- нужен ли разделитель тысяч?
        summable boolean default(null),             -- признак того, что поле является суммируемым
        case_sensitive boolean default(null),       -- признак необходимости регистронезависимого поиска для поля
        uuid varchar unique not null COLLATE NOCASE -- уникальный идентификатор домена
    );
    
    create index "idx.FZX832TFV" on dbd$domains(data_type_id);
    create index "idx.4AF9IY0XR" on dbd$domains(uuid);
    
    create table dbd$tables (
        id integer primary key autoincrement default(null),
        schema_id integer default(null),      -- идетификатор схемы (dbd$schemas)
        name varchar unique,                  -- имя таблицы
        description varchar default(null),    -- описание
        can_add boolean default(null),        -- разрешено ли добавление в таблицу
        can_edit boolean default(null),       -- разрешено ли редактирование  таблице?
        can_delete boolean default(null),     -- разрешено ли удаление в таблице
        temporal_mode varchar default(null),  -- временная таблица или нет? Если временная, то какого типа?
        means varchar default(null),          -- шаблон описания записи таблицы
        uuid varchar unique not null COLLATE NOCASE  -- уникальный идентификатор таблицы
    );
    
    create index "idx.GCOFIBEBJ" on dbd$tables(name);
    create index "idx.2J02T9LQ7" on dbd$tables(uuid);
    
    create table dbd$fields (
        id integer primary key autoincrement default(null),
        table_id integer not null,             -- идентификатор таблицы (dbd$tables)
        position integer not null,             -- номер поля в таблице (для упорядочивания полей)
        name varchar not null,                 -- латинское имя поля (будет использовано в схеме Oracle)
        russian_short_name varchar not null,   -- русское имя поля для отображения пользователю в интерактивных режимах
        description varchar default(null),     -- описание
        domain_id integer not null,            -- идентификатор типа поля (dbd$domains)
        can_input boolean default(null),       -- разрешено ли пользователю вводить значение в поле?
        can_edit boolean default(null),        -- разрешено ли пользователю изменять значение в поле?
        show_in_grid boolean default(null),    -- следует ли отображать значение поля в браузере таблицы?
        show_in_details boolean default(null), -- следует ли отображать значение поля в полной информации о записи таблицы?
        is_mean boolean default(null),         -- является ли поле элементом описания записи таблицы?
        autocalculated boolean default(null),  -- признак того, что значение в поле вычисляется программным кодом
        required boolean default(null),        -- признак того, что поле дорлжно быть заполнено
        uuid varchar unique not null COLLATE NOCASE -- уникальный идентификатор поля
    );
    
    create index "idx.7UAKR6FT7" on dbd$fields(table_id);
    create index "idx.7HJ6KZXJF" on dbd$fields(position);
    create index "idx.74RSETF9N" on dbd$fields(name);
    create index "idx.6S0E8MWZV" on dbd$fields(domain_id);
    create index "idx.88KWRBHA7" on dbd$fields(uuid);
    
    create table dbd$settings (
        key varchar primary key not null,
        value varchar,
        valueb BLOB
    );
    
    create table dbd$constraints (
        id integer primary key autoincrement default (null),
        table_id integer not null,                           -- идентификатор таблицы (dbd$tables)
        name varchar default(null),                          -- имя ограничения
        constraint_type char default(null),                  -- вид ограничения
        reference integer default(null),        -- идентификатор таблицы (dbd$tables), на которую ссылается внешний ключ
        unique_key_id integer default(null),    -- (опционально) идентификатор ограничения (dbd$constraints) таблицы, на которую ссылается внешний ключ (*1*)
        has_value_edit boolean default(null),   -- признак наличия поля ввода ключа
        cascading_delete boolean default(null), -- признак каскадного удаления для внешнего ключа
        expression varchar default(null),       -- выражение для контрольного ограничения
        uuid varchar unique not null COLLATE NOCASE -- уникальный идентификатор ограничения
    );
    
    create index "idx.6F902GEQ3" on dbd$constraints(table_id);
    create index "idx.6SRYJ35AJ" on dbd$constraints(name);
    create index "idx.62HLW9WGB" on dbd$constraints(constraint_type);
    create index "idx.5PQ7Q3E6J" on dbd$constraints(reference);
    create index "idx.92GH38TZ4" on dbd$constraints(unique_key_id);
    create index "idx.6IOUMJINZ" on dbd$constraints(uuid);
    
    create table dbd$indices (
        id integer primary key autoincrement default(null),
        table_id integer not null,                          -- идентификатор таблицы (dbd$tables)
        name varchar default(null),                         -- имя индекса
        local boolean default(0),                           -- показывает тип индекса: локальный или глобальный
        kind char default(null),                            -- вид индекса (простой/уникальный/полнотекстовый)
        uuid varchar unique not null COLLATE NOCASE         -- уникальный идентификатор индекса
    );
    
    create index "idx.12XXTJUYZ" on dbd$indices(table_id);
    create index "idx.6G0KCWN0R" on dbd$indices(name);
    create index "idx.FQH338PQ7" on dbd$indices(uuid);
    
    create table dbd$data_types (
        id integer primary key autoincrement, -- идентификатор типа
        type_id varchar unique not null       -- имя типа
    );
    
    insert into dbd$data_types(type_id) values ('STRING');
    insert into dbd$data_types(type_id) values ('SMALLINT');
    insert into dbd$data_types(type_id) values ('INTEGER');
    insert into dbd$data_types(type_id) values ('WORD');
    insert into dbd$data_types(type_id) values ('BOOLEAN');
    insert into dbd$data_types(type_id) values ('FLOAT');
    insert into dbd$data_types(type_id) values ('CURRENCY');
    insert into dbd$data_types(type_id) values ('BCD');
    insert into dbd$data_types(type_id) values ('FMTBCD');
    insert into dbd$data_types(type_id) values ('DATE');
    insert into dbd$data_types(type_id) values ('TIME');
    insert into dbd$data_types(type_id) values ('DATETIME');
    insert into dbd$data_types(type_id) values ('TIMESTAMP');
    insert into dbd$data_types(type_id) values ('BYTES');
    insert into dbd$data_types(type_id) values ('VARBYTES');
    insert into dbd$data_types(type_id) values ('BLOB');
    insert into dbd$data_types(type_id) values ('MEMO');
    insert into dbd$data_types(type_id) values ('GRAPHIC');
    insert into dbd$data_types(type_id) values ('FMTMEMO');
    insert into dbd$data_types(type_id) values ('FIXEDCHAR');
    insert into dbd$data_types(type_id) values ('WIDESTRING');
    insert into dbd$data_types(type_id) values ('LARGEINT');
    insert into dbd$data_types(type_id) values ('COMP');
    insert into dbd$data_types(type_id) values ('ARRAY');
    insert into dbd$data_types(type_id) values ('FIXEDWIDECHAR');
    insert into dbd$data_types(type_id) values ('WIDEMEMO');
    insert into dbd$data_types(type_id) values ('CODE');
    insert into dbd$data_types(type_id) values ('RECORDID');
    insert into dbd$data_types(type_id) values ('SET');
    insert into dbd$data_types(type_id) values ('PERIOD');
    insert into dbd$data_types(type_id) values ('BYTE');
    insert into dbd$settings(key, value) values ('dbd.version', '%(dbd_version)s');
        """)

    c.execute("commit")

except con.Error:
    print("Failed!")
    c.execute("rollback")
# Save (commit) the changes
# c.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
c.close()
