import sqlite3
import inspect
import sys
SELECT_TABLES_SQL = "SELECT name FROM sqlite_master WHERE type = 'table';"
CREATE_TABLE_SQL = "CREATE TABLE {name} ({fields});"

SQLITE_TYPE_MAP = {
    int: "INTEGER",
    float: "REAL",
    str: "TEXT",
    bytes: "BLOB",
    bool: "INTEGER",
}


class Database:
    def __init__(self, path):
        self.conn = sqlite3.Connection(path)
    @property
    def tables(self):
        return [x[0] for x in self._execute(SELECT_TABLES_SQL).fetchall()]
    def _execute(self,sql,params=None):
        if params:
            return self.conn.execute(sql, params)
        return self.conn.execute(sql)
    def create(self, table):
        self._execute(table._get_create_sql())

class Table:
    @classmethod
    def _get_name(cls):
        return cls.__name__.lower()
    @classmethod
    def _get_create_sql(cls):
        keyChosen = False
        fields = []
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append((name, field.sql_type))
            elif isinstance(field, ForeignKey):
                fields.append((name, "INTEGER"))
            elif isinstance(field, PrimaryKey):
                if keyChosen:
                    print("Error: Cannot have two Primary Keys compisiteKey class should be made for this functionality")
                    sys.exit()
                keyChosen = True
                fields.append((name, "INTEGER PRIMARY KEY AUTOINCREMENT"))
        fields = [" ".join(x) for x in fields]
        return CREATE_TABLE_SQL.format(name=cls._get_name(), fields=", ".join(fields))

class Column:
    def __init__(self, type):
        self.type =type
    @property
    def sql_type(self):
        return SQLITE_TYPE_MAP[self.type]
    
class ForeignKey:
    def __init__(self, table):
        self.table = table
        
class PrimaryKey:
    pass

        

