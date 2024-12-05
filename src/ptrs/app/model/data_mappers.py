import sqlite3
from ptrs.app import utils, exceptions
from ptrs.app.model import entities


class SQLiteDataMapper:
    def __init__(self, enable_foreign_keys=False):
        self._db = None
        self._enable_foreign_keys = enable_foreign_keys

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, db: sqlite3.Connection):
        self._db = db
        if self._enable_foreign_keys:
            self._db.execute("PRAGMA foreign_keys = 1") # see https://stackoverflow.com/questions/29420910/how-do-i-enforce-foreign-keys

    def _exec_dql_command(self, stmt: str, args: tuple = (), return_one=False) -> list:
        """
        Executes a general Data Query Language (DQL) command (e.g. SELECT) on the SQLite database.
        Largely the same as query_db() function from https://flask.palletsprojects.com/en/stable/patterns/sqlite3/.
        """
        cursor = self._db.execute(stmt, args)
        result_vals = cursor.fetchall()
        cursor.close()

        if return_one:
            return result_vals[0] if result_vals else []
        else:
            return result_vals

    def _exec_dml_command(self, stmt: str, args: tuple = (), do_insert=True) -> int:
        """
        Executes a general Data Manipulation Language (DML) command (e.g. INSERT, UPDATE) on the SQLite database.
        """
        cursor = self._db.execute(stmt, args)
        self._db.commit()
        res = None

        if do_insert:
            # applies only to INSERT
            res = cursor.lastrowid
        else:
            # applies to UPDATE, DELETE 
            res = cursor.rowcount # see https://stackoverflow.com/questions/2316003/get-number-of-modified-rows-after-sqlite3-execute-in-python?noredirect=1&lq=1

        cursor.close()
        return res


class PotholeMapper(SQLiteDataMapper):
    NON_UPDATABLE_FIELDS = {"pothole_id"}
    
    def __init__(self, enable_foreign_keys=False):
        super().__init__(enable_foreign_keys=enable_foreign_keys)

    def _check_invalid_fields(self, fields:list) -> list:
        invalid_fields = [] # empty if all fields are valid

        for field in fields:
            if not entities.Pothole.has_property(field):
                invalid_fields.append(field)
        
        return invalid_fields
    
    def _check_non_updatable_fields(self, fields:list):
        non_updatable_fields = []

        for field in fields:
            if field in self.NON_UPDATABLE_FIELDS:
                non_updatable_fields.append(field)

        return non_updatable_fields
    
    def _build_read_statement(self, query_params:dict={}, sort_params:dict={}):
        """
        Prepares a read statement from the given query and sort parameters

        If no query parameters are provided, a statement to select all Potholes will be returned
        """

        stmt = """SELECT pothole_id,street_addr,latitude,longitude,size,location,other_info,repair_status,
        repair_type,repair_priority,report_date FROM Potholes"""

        if len(query_params) > 0:
            stmt += " WHERE "

            invalid_params = self._check_invalid_fields(list(query_params.keys()))
            if len(invalid_params) != 0:
                raise exceptions.InvalidQueryParams(
                    {"message":f"{len(invalid_params)} query parameters are not fields of Potholes", "data":invalid_params},
                    )
            
            # TODO: could this possibly introduce a SQL injection vulnerability?
            stmt += " AND ".join([f"{param} {query_params[param]["filter"]} ?" for param in query_params])

        if len(sort_params) > 0:
            stmt += " ORDER BY "

            invalid_params = self._check_invalid_fields(list(sort_params.keys()))
            if len(invalid_params) != 0:
                raise exceptions.InvalidSortParams(
                    {"message":f"{len(invalid_params)} sort parameters are not fields of Potholes", "data":invalid_params},
                    )

            stmt += ", ".join([f"{param} {sort_params[param]}" for param in sort_params]) # TODO: possible SQL injection issue?

        return stmt
    
    def _build_update_statement(self, query_params:dict, update_fields:dict):
        """
        Prepares an update statement form the given query parameters and fields to update
        """

        stmt = """UPDATE Potholes SET """

        if len(query_params) == 0:
            raise exceptions.InvalidQueryParams(
                {"message":"Cannot find Potholes to update as no query parameters were specified", "data":[]},
                )
        
        if len(update_fields) == 0:
            raise exceptions.InvalidUpdateFields(
                {"message":"Must specify at least 1 Pothole field to update", "data":[]},
                )
        

        invalid_fields = self._check_non_updatable_fields(list(update_fields.keys()))
        if len(invalid_fields) != 0:
            raise exceptions.InvalidUpdateFields(
                {"message":f"{len(invalid_fields)} fields are not updatable fields of Potholes", "data":invalid_fields},
                )

        invalid_fields = self._check_invalid_fields(list(update_fields.keys()))
        if len(invalid_fields) != 0:
            raise exceptions.InvalidUpdateFields(
                {"message":f"{len(invalid_fields)} fields are not fields of Potholes", "data":invalid_fields},
                )

        invalid_params = self._check_invalid_fields(list(query_params.keys()))
        if len(invalid_params) != 0:
            raise exceptions.InvalidQueryParams(
                {"message":f"{len(invalid_params)} query parameters are not fields of Potholes", "data":invalid_params},
                )
        
        stmt += ", ".join([f"{field} = ?" for field in update_fields])

        stmt += " WHERE "
        stmt += " AND ".join([f"{param} {query_params[param]["filter"]} ?" for param in query_params])

        return stmt

    def create(self, pothole: entities.Pothole):
        """
        Insert a new Pothole into the database
        """

        stmt = """INSERT INTO Potholes (street_addr,latitude,longitude,size,location,other_info,repair_status,
        repair_type,repair_priority,report_date) VALUES (?,?,?,?,?,?,?,?,?,?)"""

        id = super()._exec_dml_command(stmt, args=pothole.to_tuple(incl_id=False), do_insert=True)
        pothole.pothole_id = id

        return utils.ModelState(valid=True, message=f"Successfully created new Pothole with id {id}", data=[pothole])

    def read(self, query_params:dict={}, sort_params:dict={}):
        """
        Select 1 or more exisiting Potholes from the database

        If no query parameters are specified, all Potholes are selected.
        """

        try:
            stmt = self._build_read_statement(query_params=query_params, sort_params=sort_params)
        except Exception as e:
            return utils.ModelState(valid=False, message=e.args[0]["message"], data=e.args[0]["data"], errors=[e])

        records = super()._exec_dql_command(
            stmt, 
            args=tuple([query_params[param]["val"] for param in query_params]), 
            return_one=False
            )

        potholes = [entities.Pothole(**dict(record)) for record in records]

        return utils.ModelState(valid=True, message=f"Found {len(potholes)} Potholes matching query", data=potholes)
    
    def update(self, query_params: dict, update_fields:dict):
        """
        Update 1 or more existing Potholes in the database
        """

        try:
            stmt = self._build_update_statement(query_params, update_fields)
        except Exception as e:
            return utils.ModelState(valid=False, message=e.args[0]["message"], data=e.args[0]["data"], errors=[e])

        args = tuple(list(update_fields.values()) + [query_params[param]["val"] for param in query_params])

        num_updated = super()._exec_dml_command(
            stmt, 
            args=args, 
            do_insert=False,
            )

        updated_records = super()._exec_dql_command(
            self._build_read_statement(query_params=query_params), 
            args=(args[1],), # index 1 contains the query parameters (don"t need the update fields for a select)
            return_one=False,
            )

        return utils.ModelState(
            valid=True, 
            message=f"Successfully updated {num_updated} Potholes", 
            data=[entities.Pothole(**dict(record)) for record in updated_records],
            )


class WorkOrderMapper(SQLiteDataMapper):
    NON_UPDATABLE_FIELDS = {"work_order_id", "pothole_id"}

    def __init__(self, enable_foreign_keys=False):
        super().__init__(enable_foreign_keys=enable_foreign_keys)

    def _check_invalid_fields(self, fields:list) -> list:
        invalid_fields = []

        for field in fields:
            if not entities.WorkOrder.has_property(field):
                invalid_fields.append(field)
        
        return invalid_fields
    
    def _check_non_updatable_fields(self, fields:list):
        non_updatable_fields = []

        for field in fields:
            if field in self.NON_UPDATABLE_FIELDS:
                non_updatable_fields.append(field)

        return non_updatable_fields
    
    def _build_read_statement(self, query_params:dict={}, sort_params:dict={}):
        """
        Prepares a read statement from the given query and sort parameters

        If no query parameters are provided, a statement to select all Work Orders will be returned
        """

        stmt = """SELECT work_order_id,pothole_id,assignment_date,repair_status,estimated_man_hours,expected_completion,notes FROM WorkOrders"""

        if len(query_params) > 0:
            stmt += " WHERE "

            invalid_params = self._check_invalid_fields(list(query_params.keys()))
            if len(invalid_params) != 0:
                raise exceptions.InvalidQueryParams(
                    {"message":f"{len(invalid_params)} query parameters are not fields of Work Orders", "data":invalid_params},
                    )
            stmt += " AND ".join([f"{param}=?" for param in query_params])

        if len(sort_params) > 0:
            stmt += " ORDER BY "

            invalid_params = self._check_invalid_fields(list(sort_params.keys()))
            if len(invalid_params) != 0:
                raise exceptions.InvalidSortParams(
                    {"message":f"{len(invalid_params)} sort parameters are not fields of Work Orders", "data":invalid_params},
                    )

            stmt += ", ".join([f"{param} {sort_params[param]}" for param in sort_params])

        return stmt
    
    def _build_update_statement(self, query_params:dict, update_fields:dict):
        stmt = """UPDATE WorkOrders SET """

        if len(query_params) == 0:
            raise exceptions.InvalidQueryParams(
                {"message":"Cannot find Work Orders to update as no query parameters were specified", "data":query_params},
                )
        
        if len(update_fields) == 0:
            raise exceptions.InvalidUpdateFields(
                {"message":"Must specify at least 1 Work Order field to update", "data":[]},
                )
        
        invalid_fields = self._check_non_updatable_fields(list(update_fields.keys()))
        if len(invalid_fields) != 0:
            raise exceptions.InvalidUpdateFields(
                {"message":f"{len(invalid_fields)} fields are not updatable fields of Work Orders", "data":invalid_fields},
                )

        invalid_fields = self._check_invalid_fields(list(update_fields.keys()))
        if len(invalid_fields) != 0:
            raise exceptions.InvalidUpdateFields(
                {"message":f"{len(invalid_fields)} fields are not fields of Work Orders", "data":invalid_fields},
                )

        invalid_params = self._check_invalid_fields(list(query_params.keys()))
        if len(invalid_params) != 0:
            raise exceptions.InvalidUpdateFields(
                {"message":f"{len(invalid_params)} query parameters are not fields of Work Orders", "data":invalid_params},
                )
        
        stmt += ", ".join([f"{field}=?" for field in update_fields])

        stmt += " WHERE "
        stmt += " AND ".join([f"{param}=?" for param in query_params])

        return stmt

    def create(self, work_order: entities.WorkOrder) -> entities.WorkOrder:
        """
        Insert a new Work Order into the database
        """

        stmt = """INSERT INTO WorkOrders (pothole_id,assignment_date,repair_status,estimated_man_hours,expected_completion,notes) VALUES (?,?,?,?,?,?)"""

        id = super()._exec_dml_command(stmt, args=work_order.to_tuple(incl_id=False))
        work_order.work_order_id = id

        return utils.ModelState(
            valid=True, 
            message=f"Successfully created new Work Order with id {id}", 
            data=[work_order],
            )

    def read(self, query_params: dict={}, sort_params:dict={}):
        """
        Select 1 or more existing Work Orders from the database

        If no query parameters are specified, all Work Orders will be selected
        """

        try:
            stmt = self._build_read_statement(query_params=query_params, sort_params=sort_params)
        except Exception as e:
            return utils.ModelState(
                valid=False, 
                message=e.args[0]["message"], 
                data=e.args[0]["data"], 
                errors=e,
                )

        records = super()._exec_dql_command(
            stmt, 
            args=tuple(query_params[param]["val"] for param in query_params), 
            return_one=False,
            )

        work_orders = [entities.WorkOrder(**dict(record)) for record in records]

        return utils.ModelState(
            valid=True, 
            message=f"Found {len(work_orders)} Work Orders matching query", 
            data=work_orders,
            )
    
    def update(self, query_params:dict, update_fields:dict):
        try:
            stmt = self._build_update_statement(query_params, update_fields)
        except Exception as e:
            return utils.ModelState(
                valid=False, 
                message=e.args[0]["message"], 
                data=e.args[0]["data"],
                )
        
        args = tuple(list(update_fields.values()) + [query_params[param]["val"] for param in query_params])

        num_updated = super()._exec_dml_command(
            stmt, 
            args=args, 
            do_insert=False,
            )
        
        updated_records = super()._exec_dql_command(
            self._build_read_statement(query_params=query_params),
            args=(args[1],),
            return_one=False,
            )

        return utils.ModelState(
            valid=True, 
            message=f"Successfully updated {num_updated} Work Orders", 
            data=[entities.WorkOrder(**dict(record)) for record in updated_records],
            )
