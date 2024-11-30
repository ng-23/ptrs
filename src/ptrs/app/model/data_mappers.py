import sqlite3
from ptrs import utils
from ptrs.app.model import entities


class SQLiteDataMapper:
    def __init__(self):
        self._db = None

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

    def _exec_dml_command(self, query: str, args: tuple = (), update=False) -> int | None:
        """
        Executes a general Data Manipulation Language (DML) command (e.g. INSERT, UPDATE) on the SQLite database.
        """

        cursor = self._db.execute(query, args)
        self._db.commit()
        if not update:
            inserted_row_id = cursor.lastrowid
            cursor.close()

            return inserted_row_id
        cursor.close()


class PotholeMapper(SQLiteDataMapper):
    def __init__(self):
        super().__init__()

    def create(self, pothole: entities.Pothole):
        query = """INSERT INTO Potholes (street_addr,latitude,longitude,size,location,other_info,repair_status,
        repair_type,repair_priority,report_date,expected_completion) VALUES (?,?,?,?,?,?,?,?,?,?,?)"""

        pothole.pothole_id = super()._exec_dml_command(query, args=pothole.to_tuple(incl_id=False))

        return utils.ModelState(valid=True, data=pothole)

    def read(self, query_params: dict):
        query = """SELECT pothole_id,street_addr,latitude,longitude,size,location,other_info,repair_status,
        repair_type,repair_priority,report_date,expected_completion FROM Potholes"""

        if len(query_params) > 0:
            query += " WHERE "

            # TODO: could this possibly introduce an SQL injection vulnerability?
            for param in query_params:
                if not entities.Pothole.has_property(param):
                    return utils.ModelState(valid=False, message=f"Pothole has no property {param} to query by")
            query += " AND ".join([f"{param}=?" for param in query_params])

        records = super()._exec_dql_command(query, args=tuple(query_params.values()), return_one=False)

        potholes = [entities.Pothole(**dict(record)) for record in records]

        return utils.ModelState(valid=True, message=f"Found {len(potholes)} Potholes matching query", data=potholes)


class WorkOrderMapper(SQLiteDataMapper):
    def __init__(self):
        super().__init__()

    def create(self, work_order: entities.WorkOrder):
        query = """INSERT INTO WorkOrders (pothole_id,assignment_date,repair_status,estimated_man_hours) VALUES (?,?,?,?)"""

        work_order.work_order_id = super()._exec_dml_command(query, args=work_order.to_tuple(incl_id=False))

        return utils.ModelState(valid=True, data=work_order)

    def update(self, query_params: dict):
        query = """UPDATE WorkOrders"""

        if len(query_params) > 0:
            query += " SET "

            for param in query_params:
                if not entities.WorkOrder.has_property(param):
                    return utils.ModelState(valid=False, message=f"Work Order has no property {param} to query by")
            query += ", ".join([f"{param}=?" if param != "work_order_id" else "" for param in query_params])

        query = query[:-2] + " WHERE work_order_id=?;"

        super()._exec_dml_command(query, args=tuple(query_params.values()), update=True)

        query = """SELECT work_order_id,pothole_id,assignment_date,repair_status,estimated_man_hours FROM WorkOrders WHERE work_order_id=?"""
        work_order = dict(super()._exec_dql_command(query, args=(query_params["work_order_id"],), return_one=True))

        return utils.ModelState(valid=True, data=work_order)

    def read(self, query_params: dict):
        query = """SELECT work_order_id,pothole_id,assignment_date,repair_status,estimated_man_hours FROM WorkOrders"""

        if len(query_params) > 0:
            query += " WHERE "

            # TODO: could this possibly introduce an SQL injection vulnerability?
            for param in query_params:
                if not entities.WorkOrder.has_property(param):
                    return utils.ModelState(valid=False, message=f"Work Order has no property {param} to query by")
            query += " AND ".join([f"{param}=?" for param in query_params])

        records = super()._exec_dql_command(query, args=tuple(query_params.values()), return_one=False)

        work_orders = [entities.WorkOrder(**dict(record)) for record in records]

        return utils.ModelState(valid=True, message=f"Found {len(work_orders)} Work Orders matching query", data=work_orders)
