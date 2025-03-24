from .LDModel import LDModel
from .FieldContext import FieldContext
from pydantic import Field
from rdflib import RDF, URIRef
from typing import Annotated


class ROCrateModel(LDModel):
    id: Annotated[str, FieldContext(RDF.type)] = Field(alias="@id")
    type: Annotated[str, FieldContext(RDF.type)] = Field(alias="@type")

    @classmethod
    def get_model_type(cls) -> URIRef:
        required_type = cls.model_config.get("model_type")
        return URIRef(required_type)
