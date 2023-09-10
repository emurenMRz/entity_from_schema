class column:
    """A record class for information_schema.columns"""

    def __init__(self, record) -> None:
        self.table_catalog = record[0]
        self.table_schema = record[1]
        self.table_name = record[2]
        self.column_name = record[3]
        self.ordinal_position = record[4]
        self.column_default = record[5]
        self.is_nullable = record[6]
        self.data_type = record[7]
        self.character_maximum_length = record[8]
        self.character_octet_length = record[9]
        self.numeric_precision = record[10]
        self.numeric_precision_radix = record[11]
        self.numeric_scale = record[12]
        self.datetime_precision = record[13]
        self.interval_type = record[14]
        self.interval_precision = record[15]
        self.character_set_catalog = record[16]
        self.character_set_schema = record[17]
        self.character_set_name = record[18]
        self.collation_catalog = record[19]
        self.collation_schema = record[20]
        self.collation_name = record[21]
        self.domain_catalog = record[22]
        self.domain_schema = record[23]
        self.domain_name = record[24]
        self.udt_catalog = record[25]
        self.udt_schema = record[26]
        self.udt_name = record[27]
        self.scope_catalog = record[28]
        self.scope_schema = record[29]
        self.scope_name = record[30]
        self.maximum_cardinality = record[31]
        self.dtd_identifier = record[32]
        self.is_self_referencing = record[33]
        self.is_identity = record[34]
        self.identity_generation = record[35]
        self.identity_start = record[36]
        self.identity_increment = record[37]
        self.identity_maximum = record[38]
        self.identity_minimum = record[39]
        self.identity_cycle = record[40]
        self.is_generated = record[41]
        self.generation_expression = record[42]
        self.is_updatable = record[43]

        self.is_unique = False
        self.comment = None
        self.alternative_name = None


    def column_line(self) -> str:
        s = f"{self.column_name} {self.data_type}"
        if self.is_nullable == 'No': s += ' NOT NULL'
        if self.is_unique == True: s += ' UNIQUE'
        if self.column_default != None: s += f" DEFAULT {self.column_default}"
        return s