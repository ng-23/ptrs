import sqlite3
from ptrs.app.model import entities


class SQLiteDataMapper:
    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, db: sqlite3.Connection):
        self._db = db

    def _exec_dql_query(self, query, args=(), return_one=True):
        """
        Executes a general Data Query Language (DQL) statement on the SQLite database

        Largely the same as query_db() function from https://flask.palletsprojects.com/en/stable/patterns/sqlite3/
        """

        cursor = self._db.execute(query, args)
        result_vals = cursor.fetchall()
        cursor.close()

        if return_one:
            return result_vals[0] if result_vals else []
        else:
            return result_vals

    def _exec_dml_query(self, query, args=()):
        """
        Executes a general Data Manipulation Language (DML) statement on the SQLite database
        """

        cursor = self._db.execute(query, args)
        self._db.commit()
        inserted_row_id = cursor.lastrowid
        cursor.close()

        return inserted_row_id


class PotholeMapper(SQLiteDataMapper):
    def __init__(self) -> None:
        super().__init__()

    def create(self, pothole: entities.Pothole):
        query = """INSERT INTO potholes (street_addr,latitude,longitude,size,location,other,repair_status,repair_type,repair_priority,report_date,expected_completion) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?)"""

        return super()._exec_dml_query(query, args=pothole.to_tuple(incl_id=False))

    def read_by_id(self, id: int):
        query = """SELECT id,street_addr,latitude,longitude,size,location,other,repair_status,repair_type,repair_priority,report_date,expected_completion FROM potholes WHERE id=?"""
        return entities.Pothole(
            **dict(super()._exec_dql_query(query, args=(id,), return_one=True))
        )
