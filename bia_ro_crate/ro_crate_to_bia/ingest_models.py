from pydantic import BaseModel, Field
import bia_shared_datamodels.semantic_models as sm
import bia_shared_datamodels.bia_data_model as dm
from typing_extensions import Annotated, Optional

from .pydantic_ld.LDModel import LDModel
from bia_ro_crate.ro_crate_to_bia.pydantic_ld.FieldContext import FieldContext


class Contributor(LDModel):
    name: Annotated[str, FieldContext("http://schema.org/name")] = Field()

class Study(LDModel):
    title: Annotated[str, FieldContext("http://schema.org/name")] = Field()
    contributor: Annotated[Contributor, FieldContext("http://schema.org/author")] = Field()
    description: Annotated[str, FieldContext("http://schema.org/description")] = Field()

class BioSample(LDModel):
    description: Annotated[str, FieldContext("http://schema.org/description")] = Field()















