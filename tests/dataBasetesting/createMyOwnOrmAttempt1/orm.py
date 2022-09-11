from dataclasses import field
from logging import PlaceHolder
from pickle import NONE
import sqlite3
import inspect
CREATE_TABLE_SQL = "CREATE TABLE {name} ({fields});"
SELECT_TABLES_SQL = "SELECT name FROM sqlite_master WHERE type = 'table';"
INSERT_SQL = 'INSERT INTO {name} ({fields}) VALUES ({placeholders);'
SELECT_ALL_SQL = 'SELECT {fields} FROM {name};'
SELECT_WHERE_SQL = 'SELECT {fields} FROM {name} WHERE {query}'
SQLITE_TYPE_MAP = {
    int: "INTEGER",
    float: "REAL",
    str: "TEXT",
    bytes: "BLOB",
    bool: "INTEGER"
}


class Database:
    def __init__(self, path):
        self.conn = sqlite3.Connection(path)
    def _execute(self, sql,params=None):
        if params:
            return self.conn.execute(sql, params)
        return self.conn.execute(sql)

    @property
    def tables(self):
        return self._execute(SELECT_TABLES_SQL).fetchall()

    def create(self, table):
        [row[0] for row in self._execute(table._get_create_sql())]
    def save(self, instance):
        sql, values = instance.instance._get_insert_sql()
        cursor = self._execute(sql, values)
        instance._data['id'] = cursor.lastrowid
    def all(self, table):
        sql,fields = table._get_select_all_sql()
        result = []
        for row in self._execute(sql).fetchall():
            data= dict(zip(fields,row))
            result.append(table(**data))
        return result
    def get(self, table, id):
        sql, fields, params = table.get_select_where_sql(id=id)
        row = self._execute(sql, params).fetchone()
        data = dict(zip(fields, row))
        return table(**data)
class Table:
    def __init__(self, **kwargs):
        self._data = {
            'id': None
        }
        for key, value in kwargs.items():
            self._data[key] = value
    def __getattribute__(self, key):
        _data = object.__getattribute__(self, '_data')
        if key in _data:
            return _data[key]
        return object.__getattribute__(self,key)
    @classmethod
    def _get_name(cls):
        return cls.__name__.lower
    @classmethod 
    def _get_create_sql(cls):
        fields = [("id", "INTEGER PRIMARY KEY AUTOINCREMENT")]

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append((name,field.sql_type))
            elif isinstance(field, ForeignKey):
                fields.append((name + "_id", "INTEGER"))
        fields = [" ".join(x) for x in fields]
        return CREATE_TABLE_SQL.format(name=cls._get_name(), fields=", ".join(fields))
    def _get_insert_sql(self):
        fields = []
        placeholders = []
        values = []

        for name, field in inspect.getmembers(self.__class__):
            if isinstance(field, Column):
                fields.append(name)
                values.append(getattr(self,name))
                placeholders.append('?')
        sql = INSERT_SQL.format(name=self.__class__._get_name(), fields=", ".join(fields), PlaceHolder=", ".join(placeholders))
        return sql, values
    @classmethod
    def _get_select_all_sql(cls):
        fields = ['id']
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
class Column:
    def __init__(self,  type):
        self.type = type

    @property
    def sql_type(self):
        return SQLITE_TYPE_MAP[self.type]

class ForeignKey:
    def __init__(self, table):
        self.table = table

