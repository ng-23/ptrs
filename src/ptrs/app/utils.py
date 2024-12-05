from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List
from flask import Request

API_FILTERS = {'gt':'>','lt':'<','gte':'>=','lte':'<='}
API_SORT_BY_PARAM = "sort_by" # denotes the name of the query string parameter that indicates sorting
API_SORT_OPERATORS = {"+":'ASC',"-":'DESC'} # if present in the part of the query string following the sort by param, these indicate the sort method


# code largely from Python example in Wikipedia page about observer pattern
# see https://en.wikipedia.org/wiki/Observer_pattern
class Observer(ABC):
    def notify(self, *args, **kwargs):
        pass


class Observable(ABC):
    @abstractmethod
    def register_observer(self, observer: Observer):
        pass

    @abstractmethod
    def notify_observers(self, *args, **kwargs):
        pass


@dataclass(frozen=True)
class ModelState:
    """
    Represents the state of the Model layer after the processing of a request by the user

    Intended to be consumed by an Observer of a Service (e.g. a View) for further processing
    """
    valid: bool = False
    message: str = ""
    data: List[any] = field(default_factory=list) # see https://stackoverflow.com/questions/53632152/why-cant-dataclasses-have-mutable-defaults-in-their-class-attributes-declaratio
    errors: List[Exception] = field(default_factory=list)  


def distill_query_params(req: Request):
    """
    Distills query parameters from a user request into parameter, filter, value, and sort by components

    A typical URL query string is of the format site.com/endpoint/?foo=10. Here, the query operates on objects with field foo equal to 10.

    For operations like >, >=, <, etc., the query string needs encoded in a different way. For PTRS, this encoding takes the format of
    foo=filter:value. 

    Sorting is also done through the URL query string. Sorting has its own encoding, which takes the format of
    sortBy=operatorvalue,operatorvalue. Operator indicates the sort direction (e.g. ascending, descending) and is prepended to
    the value. Should the sort need to be done on multiple values, commas can be inserted.

    References:
     - https://www.moesif.com/blog/technical/api-design/REST-API-Design-Filtering-Sorting-and-Pagination/
     - https://stackoverflow.com/questions/56516021/ordering-and-sorting-in-restful-api 
    """

    raw_query_params = dict(req.args)

    query_params = {} # maps a query param to a filter (e.g. >, >=) and a value
    sort_params = {} # maps a value to a sort operator

    for param, val in raw_query_params.items():
        if param == API_SORT_BY_PARAM:
            # special case - this query param indicates we need to interpret
            # the rest of val string as sorting options

            # first break at any commas
            sort_vals = val.split(",")

            for sort_val  in sort_vals:
                # if present, these should be of format operatorval
                # so the actual sort operators is just prepended to the val
                found_sort_op = None
                for sort_op in API_SORT_OPERATORS:
                    split_by_op = sort_val.split(sort_op)
                    if len(split_by_op) != 1:
                        # the sort operator must be present at least once somewhere in sort val
                        # we only require that it be at the front of the sort value
                        if not split_by_op[0]:
                            # sort operator is at front of sort val (and potentially elsewhere in it, but we don't care)
                            found_sort_op = sort_op
                            break
                        # the sort operator is in the val somewhere but not at the front
                        # so we don't know how to interpret it
                        raise Exception(f"Invalid sort value format. Parsing value {sort_val} for operator {sort_op} is ambiguous.")
                if found_sort_op is None:
                    raise Exception(f"Cannot find valid sort operator for sort value {sort_val}. Valid sort operators are {API_SORT_OPERATORS}")
                sort_params[sort_val[sort_val.index(found_sort_op)+1:]] = API_SORT_OPERATORS[found_sort_op]   
        else:
            split_val = val.split(":")

            if len(split_val) == 1:
                # val must not have a filter, default to equals
                query_params[param] = {"filter":"=", "val":val}
            else:
                # there's at least 1 colon
                # filter must come first so it should be at index 0
                filter = split_val[0]
                
                if not filter:
                    # val must be of format :foo:bar:...
                    # where colon is 1st char so filter is essentially empty
                    # in this case, just interpret it literally
                    query_params[param] = {"filter":"=", "val":val}
                    continue
                
                # colon isn't 1st char so there are other chars before it that make up the filter
                if filter not in API_FILTERS:
                    raise Exception(f"Invalid filter for query parameter {param} with value {val}. Valid filters are {API_FILTERS}")
                
                # filter is present and valid
                # store it separately and leave rest of val string the same, even if it has additional colons
                query_params[param] = {"filter":API_FILTERS[filter], "val":val[val.index(":")+1:]}

    # TODO: this should probably return a specialized object so we can be sure the necessary key/val pairs are all there
    return query_params, sort_params 

