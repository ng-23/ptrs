class Entity:
    def to_tuple(self):
        return tuple(vars(self).values())

    def __repr__(self):
        attrs_and_vals = {
            attr[1:]: getattr(self, attr)
            for attr in self.__dict__
            if attr.startswith("_")
        }  # assumes the attributes of the class are prefixed with an _
        return f"{attrs_and_vals}"


class Pothole(Entity):
    VALID_SIZES = set(range(1, 11))
    VALID_LOCATIONS = {
        "left_lane",
        "right_lane",
        "middle_lane",
        "turn_lane",
        "curbside",
    }
    VALID_REPAIR_TYPES = {"asphalt", "concrete", "unknown"}
    VALID_REPAIR_PRIORITIES = {"major", "medium", "minor"}

    def __init__(
            self,
            street_addr: str,
            latitude: float,
            longitude: float,
            size: int,
            location: str,
            other: str,
            repair_status: str,
            repair_type: str,
            repair_priority: str,
            report_date: str,
            expected_completion: str,
            id: int | None = None,
    ):
        # see https://realpython.com/python-getter-setter/ for why/how to write getters and setters in Python
        self.id = id
        self.street_addr = street_addr
        self.latitude = latitude
        self.longitude = longitude
        self.size = size
        self.location = location
        self.other = other
        self.repair_status = repair_status
        self.repair_type = repair_type
        self.repair_priority = repair_priority
        self.report_date = report_date
        self.expected_completion = expected_completion

    @property
    def id(self):
        return self._id

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
    def other(self):
        return self._other

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

    @id.setter
    def id(self, id: int | None):
        self._id = id

    @street_addr.setter
    def street_addr(self, street_addr: str):
        # TODO: verify that address actually exists and is within jurisdiction of local DPW
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
            raise ValueError(
                f"Size must be one of {self.VALID_SIZES}, got {size} instead"
            )
        self._size = size

    @location.setter
    def location(self, location: str):
        location = location.lower()
        if location not in self.VALID_LOCATIONS:
            raise ValueError(
                f"Location must be one of {self.VALID_LOCATIONS}, got {location} instead"
            )
        self._location = location

    @other.setter
    def other(self, other: str):
        self._other = other

    @repair_status.setter
    def repair_status(self, repair_status: str):
        self._repair_status = repair_status

    @repair_type.setter
    def repair_type(self, repair_type: str):
        repair_type = repair_type.lower()
        if repair_type not in self.VALID_REPAIR_TYPES:
            raise ValueError(
                f"Repair type must be one of {self.VALID_REPAIR_TYPES}, got {repair_type} instead"
            )
        self._repair_type = repair_type

    @repair_priority.setter
    def repair_priority(self, repair_priority: str):
        repair_priority = repair_priority.lower()
        if repair_priority not in self.VALID_REPAIR_PRIORITIES:
            raise ValueError(
                f"Repair priority must be one of {self.VALID_REPAIR_PRIORITIES}, got {repair_priority} instead"
            )
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
