class Entity:
    @classmethod  # see https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner
    def has_property(cls, property_name: str) -> bool:
        # see https://stackoverflow.com/questions/17735520/determine-if-given-class-attribute-is-a-property-or-not-python-object
        # properties are class-level attributes, not instance, so we must use type(self) or self.__class__ to check
        if not hasattr(cls, property_name):
            return False

        if not isinstance(getattr(cls, property_name), property):
            return False

        return True

    def to_tuple(self):
        return tuple(vars(self).values())

    def to_json(self):
        res = {}

        for attr in vars(type(self)):
            if isinstance(getattr(type(self), attr), property):
                res[attr] = getattr(self, attr)

        return res

    def __repr__(self):
        return f"{type(self).__name__}{self.to_json()}"


class Pothole(Entity):
    VALID_SIZES = set(range(1, 11))
    VALID_LOCATIONS = {"left_lane", "right_lane", "middle_lane", "turn_lane", "curbside"}
    VALID_REPAIR_STATUSES = {"not repaired", "temporarily repaired", "repaired"}
    VALID_REPAIR_TYPES = {"asphalt", "concrete", "unknown"}
    VALID_REPAIR_PRIORITIES = {"major", "medium", "minor"}

    def __init__(
            self,
            street_addr: str,
            latitude: float,
            longitude: float,
            size: int,
            location: str,
            other_info: str,
            repair_status: str,
            repair_type: str,
            repair_priority: str,
            report_date: str,
            expected_completion: str,
            pothole_id: int | None = None,
    ):
        self.pothole_id = pothole_id
        self.street_addr = street_addr
        self.latitude = latitude
        self.longitude = longitude
        self.size = size
        self.location = location
        self.other_info = other_info
        self.repair_status = repair_status
        self.repair_type = repair_type
        self.repair_priority = repair_priority
        self.report_date = report_date
        self.expected_completion = expected_completion

    @property
    def pothole_id(self):
        return self._pothole_id

    @property
    def street_addr(self):
        return self._street_addr

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def size(self):
        return self._size

    @property
    def location(self):
        return self._location

    @property
    def other_info(self):
        return self._other_info

    @property
    def repair_status(self):
        return self._repair_status

    @property
    def repair_type(self):
        return self._repair_type

    @property
    def repair_priority(self):
        return self._repair_priority

    @property
    def report_date(self):
        return self._report_date

    @property
    def expected_completion(self):
        return self._expected_completion

    @pothole_id.setter
    def pothole_id(self, pothole_id: int | None):
        self._pothole_id = pothole_id

    @street_addr.setter
    def street_addr(self, street_addr: str):
        self._street_addr = street_addr

    @latitude.setter
    def latitude(self, latitude: float):
        self._latitude = latitude

    @longitude.setter
    def longitude(self, longitude: float):
        self._longitude = longitude

    @size.setter
    def size(self, size: int):
        if size not in self.VALID_SIZES:
            raise ValueError(f"Size must be one of {self.VALID_SIZES}, got '{size}' instead")
        self._size = size

    @location.setter
    def location(self, location: str):
        location = location.lower()
        if location not in self.VALID_LOCATIONS:
            raise ValueError(f"Location must be one of {self.VALID_LOCATIONS}, got '{location}' instead")
        self._location = location

    @other_info.setter
    def other_info(self, other_info: str):
        self._other_info = other_info

    @repair_status.setter
    def repair_status(self, repair_status: str):
        repair_status = repair_status.lower()
        if repair_status not in self.VALID_REPAIR_STATUSES:
            raise ValueError(f"Repair Status must be one of {self.VALID_REPAIR_STATUSES}, got '{repair_status}' instead")
        self._repair_status = repair_status

    @repair_type.setter
    def repair_type(self, repair_type: str):
        repair_type = repair_type.lower()
        if repair_type not in self.VALID_REPAIR_TYPES:
            raise ValueError(f"Repair Type must be one of {self.VALID_REPAIR_TYPES}, got '{repair_type}' instead")
        self._repair_type = repair_type

    @repair_priority.setter
    def repair_priority(self, repair_priority: str):
        repair_priority = repair_priority.lower()
        if repair_priority not in self.VALID_REPAIR_PRIORITIES:
            raise ValueError(f"Repair Priority must be one of {self.VALID_REPAIR_PRIORITIES}, got '{repair_priority}' instead")
        self._repair_priority = repair_priority

    @report_date.setter
    def report_date(self, report_date: str):
        self._report_date = report_date

    @expected_completion.setter
    def expected_completion(self, expected_completion: str):
        self._expected_completion = expected_completion

    def to_tuple(self, incl_id=False):
        attrs = super().to_tuple()
        if incl_id:
            return attrs
        else:
            return attrs[1:]


class WorkOrder(Entity):
    VALID_REPAIR_STATUSES = {"not repaired", "temporarily repaired", "repaired"}

    def __init__(
            self,
            pothole_id: int,
            assignment_date: str,
            repair_status: str,
            estimated_man_hours: int,
            work_order_id: int | None = None,
    ):
        self.work_order_id = work_order_id
        self.pothole_id = pothole_id
        self.assignment_date = assignment_date
        self.repair_status = repair_status
        self.estimated_man_hours = estimated_man_hours

    @property
    def work_order_id(self):
        return self._work_order_id

    @property
    def pothole_id(self):
        return self._pothole_id

    @property
    def assignment_date(self):
        return self._assignment_date

    @property
    def repair_status(self):
        return self._repair_status

    @property
    def estimated_man_hours(self):
        return self._estimated_man_hours

    @work_order_id.setter
    def work_order_id(self, work_order_id: int | None):
        self._work_order_id = work_order_id

    @pothole_id.setter
    def pothole_id(self, pothole_id: int):
        self._pothole_id = pothole_id

    @assignment_date.setter
    def assignment_date(self, assignment_date: str):
        self._assignment_date = assignment_date

    @repair_status.setter
    def repair_status(self, repair_status: str):
        repair_status = repair_status.lower()
        if repair_status not in self.VALID_REPAIR_STATUSES:
            raise ValueError(f"Repair Type must be one of {self.VALID_REPAIR_STATUSES}, got '{repair_status}' instead")
        self._repair_status = repair_status

    @estimated_man_hours.setter
    def estimated_man_hours(self, estimated_man_hours: int):
        self._estimated_man_hours = estimated_man_hours

    def to_tuple(self, incl_id=False):
        attrs = super().to_tuple()
        if incl_id:
            return attrs
        else:
            return attrs[1:]
