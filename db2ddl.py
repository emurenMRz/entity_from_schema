import modules.database_information as DBINFO

if __name__ == '__main__':
    databases = DBINFO.get_database_name_list()
    print(databases)

    for name in databases:
        print(name)
        for table in DBINFO.get_table_list(name):
            print(f"\tCREATE TABLE {table.name} (")
            for column in table.columns.values():
                print(f"\t    {column.column_line()},")
            for value in table.foreign_keys:
                print(f"\t    CONSTRAINT {value['constraint_name']} FOREIGN KEY {value['column_name']} REFERENCES {value['table_name']}({value['column_name']})")
            print(f"\t    PRIMARY KEY ({', '.join(table.primary_keys)})")
            for index, constraint_type in enumerate(table.constraints):
                data = table.constraints[constraint_type]
                print(f"\t    {constraint_type}({', '.join(data)})")
            print(f"\t)")

            if table.comment != None:
                print(f"\tCOMMENT ON TABLE {table.name} IS '{table.comment}'")
            for column in table.columns.values():
                if column.comment != None:
                    print(f"\tCOMMENT ON COLUMN {table.name}.{column.column_name} IS '{column.comment}'")
