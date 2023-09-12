import os
import csv

from modules.database_information import TableInfo


class Token:

    def __init__(self, name, comment, type = "column", alternative_name = None) -> None:
        if name == None: raise ValueError('"name" required.')
        if type == None: raise ValueError('"type" required.')
        if type != 'table' and type != 'column': raise ValueError('"type" is "table" or "column" required.')

        self.name = name
        self.comment = comment
        self.type = type

        if alternative_name == None or len(alternative_name) == 0:
            self.alternative_name = self.build_alternative_name(name, type)
        else:
            self.alternative_name = alternative_name


    def to_array(self):
        return [self.name, self.alternative_name, self.comment, self.type]


    def to_hash(self):
        return f"{self.name}{self.comment}{self.type}" if self.comment != None else f"{self.name}{self.type}"


    @staticmethod
    def build_alternative_name(name, type):
        if name.find('_') != -1:
            parts = name.split('_')
        else:
            parts = []
            start = 0
            while True:
                pos = name.find(r'[A-Z]', start + 1)
                if pos == -1:
                    parts.append(name[start:])
                    break
                if start == pos: continue
                parts.append(name[start:pos])
                start = pos
        
        parts = [s.capitalize() for s in parts]
        if type == 'column':
            parts[0] = parts[0].lower()
        
        return ''.join(parts)


class Table:
    def __init__(self, csv_filename):
        self.token_table = self.read_token_table(csv_filename)
        self.dictionary = self.table_to_dictionary(self.token_table)

        dict_names = list(self.dictionary.keys())
        self.default_dictionary = self.dictionary[dict_names[0]] if len(dict_names) > 0 else {}


    def get_dictionary(self, table_name = None):
        return self.dictionary.get(table_name, self.default_dictionary)


    @staticmethod
    def read_token_table(csv_filename):
        token_table = {}
        if os.path.isfile(csv_filename):
            with open(csv_filename, encoding='utf-8') as f:
                reader = csv.reader(f)
                table = None
                for row in reader:
                    if len(row) == 0: continue

                    [name, alternative_name, comment, type] = row

                    if name == 'name' and alternative_name == 'alternative_name' and comment == 'comment' and type == 'type':
                        if table != None: token_table[table[0].name] = table
                        table = []
                        continue
                    if table == None: continue

                    table.append(Token(name, comment, type, alternative_name))
                if table != None and len(table) > 0: token_table[table[0].name] = table
        return token_table


    @staticmethod
    def table_to_dictionary(token_table):
        token_dictionaries = {}
        for table_name in token_table:
            token_dictionary = {}
            for row in token_table[table_name]:
                token_dictionary[row.to_hash()] = row.alternative_name
            token_dictionaries[table_name] = token_dictionary
        return token_dictionaries


class Utility:
    def __init__(self, token_dictionary) -> None:
        self.token_dictionary = token_dictionary


    def row(self, obj):
        return self.token(obj).to_array()


    def token(self, obj):
        if type(obj) is TableInfo:
            token = Token(obj.name, obj.comment, "table")
        else:
            token = Token(obj.column_name, obj.comment, "column")

        hash = token.to_hash()
        if hash in self.token_dictionary:
            token.alternative_name = self.token_dictionary[hash]
        else:
            self.token_dictionary[hash] = token.alternative_name

        obj.alternative_name = token.alternative_name

        return token
