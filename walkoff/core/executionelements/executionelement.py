import uuid

from walkoff.core.representable import Representable


class ExecutionElement(Representable):
    def __init__(self, uid=None):
        """Initializes a new ExecutionElement object. This is the parent class.
        
        Args:
            uid (str, optional): The UID of this ExecutionElement. Constructed from a UUID4 hex string
        """
        self.uid = str(uuid.uuid4()) if uid is None else uid

    def regenerate_uids(self, with_children=True):
        """
        Regenerates the UIDs of the execution element and its children

        Args:
            with_children (bool optional): Regenerate the childrens' UIDs of this object? Defaults to True
        """
        self.uid = str(uuid.uuid4())
        if with_children:
            for field, value in ((field, getattr(self, field)) for field in dir(self)
                                 if not callable(getattr(self, field))):
                if isinstance(value, list):
                    self.__regenerate_uids_of_list(value)
                elif isinstance(value, dict):
                    self.__regenerate_uids_of_dict(value)
                elif isinstance(value, ExecutionElement):
                    value.regenerate_uids()

    @staticmethod
    def __regenerate_uids_of_dict(value):
        for dict_element in (element for element in value.values() if
                             isinstance(element, ExecutionElement)):
            dict_element.regenerate_uids()

    @staticmethod
    def __regenerate_uids_of_list(value):
        for list_element in (list_element_ for list_element_ in value
                             if isinstance(list_element_, ExecutionElement)):
            list_element.regenerate_uids()

    def __repr__(self):
        representation = self.read()
        uid = representation.pop('uid', None)
        out = '<{0} at {1} : uid={2}'.format(self.__class__.__name__, hex(id(self)), uid)
        for key, value in representation.items():
            if self.__is_list_of_dicts_with_uids(value):
                out += ', {0}={1}'.format(key, [list_value['uid'] for list_value in value])
            else:
                out += ', {0}={1}'.format(key, value)

        out += '>'
        return out

    @staticmethod
    def __is_list_of_dicts_with_uids(value):
        return (isinstance(value, list)
                and all(isinstance(list_value, dict) and 'uid' in list_value for list_value in value))
