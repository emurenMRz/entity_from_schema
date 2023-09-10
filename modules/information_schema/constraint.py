class constraint:
    """A record class for information_schema.table_constraints with information_schema.constraint_column_usage"""

    def __init__(self, record) -> None:
        self.constraint_name = record[0]
        self.constraint_catalog = record[1]
        self.constraint_schema = record[2]
        self.table_catalog = record[3]
        self.table_schema = record[4]
        self.table_name = record[5]
        self.constraint_type = record[6]
        self.is_deferrable = record[7]
        self.initially_deferred = record[8]
        self.enforced = record[9]
        self.target_table_name = record[10]
        self.target_column_name = record[11]


