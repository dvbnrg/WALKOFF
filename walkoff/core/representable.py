from walkoff.core.jsonelementcreator import JsonElementCreator
from walkoff.core.jsonelementreader import JsonElementReader


class Representable(object):
    @classmethod
    def create(cls, representation, creator=JsonElementCreator):
        """
        Creates a ExecutionElement from a representation

        Args:
            representation: Representation of the ExecutionElement
            creator (cls, optional): The creator class to use to construct the ExecutionElement.
                Defaults to JsonElementCreator

        Returns:
            (ExecutionElement) The created execution element
        """
        return creator.create(representation, element_class=cls)

    def read(self, reader=None):
        """
        Reads an ExecutionElement and converts it to some representation

        Args:
            reader (cls, optional): The reader to use. Defaults to JsonElementReader

        Returns:
            The representation of the ExecutionElement generated by the reader
        """
        if reader is None:
            reader = JsonElementReader
        return reader.read(self)
