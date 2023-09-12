import os
import argparse
import csv
import modules.database_information as DBINFO
import modules.token as T

from modules.entity_jpa import make_entity_jpa


def separate_table_proc(database_name, prev_tokens, make_entity):
    token_table = []
    for table in DBINFO.get_table_list(database_name):
        tu = T.Utility(prev_tokens.get_dictionary(table.name))

        token_table.append(["name", "alternative_name", "comment", "type"])
        token_table.append(tu.row(table))
        for column in table.columns.values():
            token_table.append(tu.row(column))
        token_table.append([])

        if make_entity != None:
            make_entity(table)

    return token_table


def one_table_proc(database_name, prev_tokens, make_entity):
    token_table = [["name", "alternative_name", "comment", "type"]]
    tu = T.Utility(prev_tokens.get_dictionary())
    tokens = {}
    for table in DBINFO.get_table_list(database_name):
        token_table.append(tu.row(table))
        for column in table.columns.values():
            token = tu.token(column)
            tokens[token.to_hash()] = token

        if make_entity != None:
            make_entity(table)

    for token in tokens.values():
        token_table.append(token.to_array())

    return token_table


def update_entity(database_name, options):
    csv_filename = f"token_table/{database_name}.csv"
    prev_tokens = T.Table(csv_filename)

    proc = separate_table_proc if options.separate_by_schema else one_table_proc
    make_entity = None if options.token_table_only else make_entity_jpa
    token_table = proc(database_name, prev_tokens, make_entity)

    with open(csv_filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(token_table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'update_entity',
                                     description = 'Create/update entity classes from DB schema.',
                                     epilog = '---  ---')
    parser.add_argument('-s', '--separate-by-schema', action = 'store_true', help = 'Create a token table for each schema.')
    parser.add_argument('-t', '--token-table-only', action = 'store_true', help = 'Outputs only token tables.')
    parser.add_argument('-d', '--database', action = 'store', help = 'Outputs only the specified database.')
    options = parser.parse_args()

    os.makedirs("token_table", exist_ok = True)

    if options.database != None:
        update_entity(options.database, options)
    else:
        for name in DBINFO.get_database_name_list():
            update_entity(name, options)