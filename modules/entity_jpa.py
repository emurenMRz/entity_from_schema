import os
from string import Template


convert_type = {
    'smallint': 'short',
    'integer': 'int',
    'bigint': 'BigInteger',
    'decimal': 'BigDecimal',
    'numeric': 'BigDecimal',
    'money': 'BigDecimal',
    'real': 'float',
    'double precision': 'long',
    'serial': 'int',
    'bigserial': 'long',

    'boolean': 'boolean',

    'varchar': 'String',
    'character': 'String',
    'character varying': 'String',
    'char': 'String',
    'text': 'String',

    'bytea': 'byte[]',
    'json': 'String',
    'jsonb': 'String',

    'date': 'Date',
    'time': 'Time',
    'time with time zone': 'Time',
    'time without time zone': 'Time',
    'timestamp': 'Timestamp',
    'timestamp with time zone': 'Timestamp',
    'timestamp without time zone': 'Timestamp'
}


convert_nullable = {
    'short': 'Short',
    'int': 'Integer',
    'long': 'Long',
    'float': 'Float',
    'boolean': 'Boolean',
}

with open(f"template/entity.template") as f:
     entity_template = Template(f.read())
with open(f"template/entity_column.template") as f:
     entity_column_template = Template(f.read())
with open(f"template/entity_key.template") as f:
     entity_key_template = Template(f.read())
with open(f"template/entity_key_column.template") as f:
     entity_key_column_template = Template(f.read())
with open(f"template/repository.template") as f:
     repository_template = Template(f.read())
with open(f"template/service.template") as f:
     service_template = Template(f.read())


def convert_data_type(data_type, nullable = True):
    type = convert_type[data_type] if data_type in convert_type else data_type
    if nullable:
        type = convert_nullable[type] if type in convert_nullable else type
    return type


def build_column(table, column):
    target_column = column.comment if column.comment != None else column.column_name
    data_type = convert_data_type(column.data_type, column.is_nullable)
    variable_name = column.alternative_name

    column_options = ""
    if not column.is_nullable: column_options += ", nullable = false"
    if column.is_unique: column_options += ", unique = true"

    id = "\n\t@Id" if column.column_name in table.primary_keys else ""
    
    return entity_column_template.safe_substitute(
        target_column = target_column,
        id = id,
        column_name = column.column_name,
        column_data_type = column.data_type,
        column_options = column_options,
        data_type = data_type,
        variable_name = variable_name
        )


def make_entity_class(table, base_dir = 'class/entity'):
    target_schema = table.comment if table.comment != None else table.name
    entity_name = table.alternative_name
    table_comment = f'\n@Table(comment = "{table.comment}")' if table.comment != None else ""

    columns = ''
    for column in table.columns.values():
        columns += build_column(table, column)

    os.makedirs(base_dir, exist_ok = True)
    with open(f"{base_dir}/{entity_name}.java", 'w', encoding='utf-8') as f:
        f.write(entity_template.safe_substitute(
             target_schema = target_schema,
             table_name = table.name,
             table_comment = table_comment,
             entity_name = entity_name,
             columns = columns
             ))


def build_key_column(column):
    target_column = column.comment if column.comment != None else column.column_name
    data_type = convert_data_type(column.data_type, column.is_nullable)
    variable_name = column.alternative_name

    return entity_key_column_template.safe_substitute(
        target_column = target_column,
        data_type = data_type,
        variable_name = variable_name
        )


def make_key_class(table, base_dir = 'class/entity'):
    target_schema = table.comment if table.comment != None else table.name
    entity_name = table.alternative_name

    columns = ''
    for key in table.primary_keys:
        columns += build_key_column(table.columns[key])

    os.makedirs(base_dir, exist_ok = True)
    with open(f"{base_dir}/{entity_name}Key.java", 'w', encoding='utf-8') as f:
        f.write(entity_key_template.safe_substitute(
             target_schema = target_schema,
             entity_name = entity_name,
             columns = columns
             ))


def make_repository_interface(table, base_dir = 'class/repository'):
    target_schema = table.comment if table.comment != None else table.name
    entity_name = table.alternative_name
    if len(table.primary_keys) > 1:
        id_type = f"{entity_name}Key"
    else:
        id_type = convert_data_type(table.columns[table.primary_keys[0]].data_type)

    os.makedirs(base_dir, exist_ok = True)
    with open(f"{base_dir}/{entity_name}Repository.java", 'w', encoding='utf-8') as f:
        f.write(repository_template.safe_substitute(
             target_schema = target_schema,
             entity_name = entity_name,
             id_type = id_type
             ))


def make_service_class(table, base_dir = 'class/service'):
    target_schema = table.comment if table.comment != None else table.name
    entity_name = table.alternative_name
    repository_name = entity_name[0].lower() + entity_name[1:]

    os.makedirs(base_dir, exist_ok = True)
    with open(f"{base_dir}/{entity_name}Service.java", 'w', encoding='utf-8') as f:
        f.write(service_template.safe_substitute(
             target_schema = target_schema,
             entity_name = entity_name,
             repository_name = repository_name,
             ))


def make_entity_jpa(table):
    make_entity_class(table)

    length = len(table.primary_keys)
    if length > 0:
        if length > 1:
            make_key_class(table)
        make_repository_interface(table)
        make_service_class(table)
