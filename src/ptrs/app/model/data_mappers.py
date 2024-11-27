import sqlite3
from ptrs import utils
from ptrs.app.model import entities


class SQLiteDataMapper:
    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, db: sqlite3.Connection):
        self._db = db

    def _exec_dql_command(self, query: str, args: tuple = (), return_one=False) -> list:
        """
        Executes a general Data Query Language (DQL) command (e.g. SELECT) on the SQLite database.
        Largely the same as query_db() function from https://flask.palletsprojects.com/en/stable/patterns/sqlite3/.
        """

        cursor = self._db.execute(query, args)
        result_vals = cursor.fetchall()
        cursor.close()

        if return_one:
            return result_vals[0] if result_vals else []
        else:
            return result_vals

    def _exec_dml_command(self, query: str, args: tuple = ()) -> int | None:
        """
        Executes a general Data Manipulation Language (DML) command (e.g. INSERT, UPDATE) on the SQLite database.
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

        pothole.id = super()._exec_dml_command(
            query, args=pothole.to_tuple(incl_id=False)
        )

        return utils.ModelState(valid=True, data=pothole)

    def read(self, query_params: dict, sort_and_order_by: dict | None = None):
        query = """SELECT id,street_addr,latitude,longitude,size,location,other,repair_status,repair_type,repair_priority,report_date,expected_completion FROM potholes"""

        if len(query_params) > 0:
            query += " WHERE "

            # TODO: could this possibly introduce a SQL injection vulnerability?
            for param in query_params:
                if not entities.Pothole.has_property(param):
                    return utils.ModelState(
                        valid=False,
                        message=f"Pothole has no property {param} to query by",
                    )
            query += " AND ".join([f"{param}=?" for param in query_params])

        records = super()._exec_dql_command(
            query, args=tuple(query_params.values()), return_one=False
        )

        potholes = [entities.Pothole(**dict(record)) for record in records]

        return utils.ModelState(
            valid=True,
            message=f"Found {len(potholes)} potholes matching query",
            data=potholes,
        )
