import psycopg2
import modules.datasource as DS
import modules.information_schema.column as COLUMN
import modules.information_schema.constraint as CONSTRAINT


def get_database_name_list():
    names = []
    with psycopg2.connect(DS.connect_parameter()) as conn:
        conn.set_client_encoding('UTF8')
        with conn.cursor() as cur:
            cur.execute("SELECT datname FROM pg_database WHERE datistemplate=false")
            for record in cur.fetchall():
                names.append(record[0])
    return names


def get_table_list(database_name):
    tables = []
    with psycopg2.connect(DS.connect_parameter(name = database_name)) as conn:
        conn.set_client_encoding('UTF8')
        with conn.cursor() as cur:
            cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")
            for record in cur.fetchall():
                tables.append(get_table_info(cur, record[0]))
    return tables


class TableInfo:
    pass


def get_table_info(cur, table_name) -> TableInfo:
    # column info
    sql = """
    SELECT
        *
    FROM
        information_schema.columns
    WHERE
        table_name = %s
    ORDER BY
        table_name, ordinal_position
    """
    cur.execute(sql, (table_name,))
    columns = {}
    index_for_columns = {}
    for record in cur.fetchall():
        column = COLUMN.column(record)
        columns[column.column_name] = column
        index_for_columns[column.ordinal_position] = column

    # constraint
    sql = """
    SELECT
        *
    FROM
        information_schema.table_constraints A
        INNER JOIN (
            SELECT
                *
            FROM
                information_schema.constraint_column_usage
            ) B
            USING (
                constraint_name,
                constraint_catalog,
                constraint_schema,
                table_catalog,
                table_schema
            )
    WHERE
        A.constraint_schema = 'public'
        AND constraint_type <> 'CHECK'
        AND A.table_name = %s
    """
    cur.execute(sql, (table_name, ))
    primary_keys = []
    foreign_keys = []
    constraints = {}
    for record in cur.fetchall():
        constraint = CONSTRAINT.constraint(record)
        if constraint.constraint_type == 'PRIMARY KEY':
            primary_keys.append(constraint.target_column_name)
        elif constraint.constraint_type == 'FOREIGN KEY':
            foreign_keys.append({
                'constraint_name': constraint.constraint_name,
                'table_name': constraint.target_table_name,
                'column_name': constraint.target_column_name,
            })
        elif constraint.constraint_type == 'UNIQUE':
            columns[constraint.target_column_name].is_unique = True
        else:
            constraints[constraint.constraint_type] = constraint

    # comment
    sql = """
    SELECT
        objsubid,
        description
    FROM
        pg_stat_user_tables A
        INNER JOIN pg_description B
        ON A.relid = B.objoid
    WHERE
        relname=%s
    ORDER BY
        B.objsubid
    """
    cur.execute(sql, (table_name,))
    table_comment = None
    for record in cur.fetchall():
        if record[0] == 0:
            table_comment = record[1]
        else:
            index_for_columns[record[0]].comment = record[1]

    table_info = TableInfo()
    setattr(table_info, 'name', table_name)
    setattr(table_info, 'columns', columns)
    setattr(table_info, 'primary_keys', primary_keys)
    setattr(table_info, 'foreign_keys', foreign_keys)
    setattr(table_info, 'constraints', constraints)
    setattr(table_info, 'comment', table_comment)
    setattr(table_info, 'alternative_name', None)

    return table_info
