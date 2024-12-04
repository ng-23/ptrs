
# see https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
# to get messages/data from an Exception, just pass a dict of format {'message':str, 'data':[]}, since *args is a list

class DataMapperException(Exception):
    '''
    Raised by a DataMapper when an error occurs
    '''

class InvalidQueryParams(DataMapperException):
    '''
    Raised by a DataMapper when invalid query parameters are provided for a database action
    '''

class InvalidSortParams(DataMapperException):
    '''
    Raised by a DataMapper when invalid sort parameters are provided for a database action
    '''

class InvalidUpdateFields(DataMapperException):
    '''
    Raised by a DataMapper when invalid fields are provided for a database update action
    '''