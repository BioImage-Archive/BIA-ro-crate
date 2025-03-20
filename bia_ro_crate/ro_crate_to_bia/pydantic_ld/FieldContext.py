from typing import Optional
from rdflib import URIRef

class FieldContext():

    uri : URIRef
    isIdField : str

    def __init__(self, uri: str, isIdField: Optional[bool] = False ):
        self.uri = URIRef(uri)
        self.isIdField = isIdField
