
class Pothole():
    VALID_SIZES = set(range(1,11))
    VALID_LOCATIONS = {'left_lane','right_lane','middle_lane','turn_lane','curbside',}
    VALID_REPAIR_TYPES = {'asphalt','concrete','unknown'}
    VALID_REPAIR_PRIORITIES = {'major','medium','minor'}

    def __init__(self, street_addr:str, size:int, location:str, repair_type:str, repair_priority:str, id:int|None=None):
        # see https://realpython.com/python-getter-setter/ for why/how to write getters and setters in Python
        self.id = id
        self.street_addr = street_addr
        self.size = size
        self.location = location
        self.repair_type = repair_type
        self.repair_priority = repair_priority

    @property
    def id(self):
        return self._id
    
    @property
    def street_addr(self):
        return self._street_addr
    
    @property
    def size(self):
        return self._size
    
    @property
    def location(self):
        return self._location
    
    @property
    def repair_type(self):
        return self._repair_type
    
    @property
    def repair_priority(self):
        return self._repair_priority
    
    @id.setter
    def id(self, id:int|None):
        self._id = id

    @street_addr.setter
    def street_addr(self, street_addr:str):
        # TODO: verify that address actually exists and is within jurisdiction of local DPW
        self._street_addr = street_addr

    @size.setter
    def size(self, size:int):
        if size not in self.VALID_SIZES:
            raise ValueError(f'Size must be one of {self.VALID_SIZES}, got {size} instead')
        self._size = size

    @location.setter
    def location(self, location:str):
        location = location.lower()
        if location not in self.VALID_LOCATIONS:
            raise ValueError(f'Location must be one of {self.VALID_LOCATIONS}, got {location} instead')
        self._location = location

    @repair_type.setter
    def repair_type(self, repair_type:str):
        repair_type = repair_type.lower()
        if repair_type not in self.VALID_REPAIR_TYPES:
            raise ValueError(f'Repair type must be one of {self.VALID_REPAIR_TYPES}, got {repair_type} instead')
        self._repair_type = repair_type

    @repair_priority.setter
    def repair_priority(self, repair_priority:str):
        repair_priority = repair_priority.lower()
        if repair_priority not in self.VALID_REPAIR_PRIORITIES:
            raise ValueError(f'Repair priority must be one of {self.VALID_REPAIR_PRIORITIES}, got {repair_priority} instead')
        self._repair_priority = repair_priority
        