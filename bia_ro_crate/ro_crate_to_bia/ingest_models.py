from pydantic import BaseModel, Field, AnyUrl, ConfigDict
from rdflib import RDF
import bia_shared_datamodels.semantic_models as sm
import bia_shared_datamodels.bia_data_model as dm
from typing_extensions import Annotated, Optional, Union

from bia_ro_crate.ro_crate_to_bia.pydantic_ld.ROCrateModel import ROCrateModel
from bia_ro_crate.ro_crate_to_bia.pydantic_ld.FieldContext import FieldContext
from bia_ro_crate.ro_crate_to_bia.pydantic_ld.LDModel import ObjectReference

# Studies and Publications


class Study(ROCrateModel):
    title: Annotated[str, FieldContext("http://schema.org/name")] = Field()
    contributor: Annotated[
        list[str], FieldContext("http://schema.org/author", isIdField=True)
    ] = Field(min_length=1)
    description: Annotated[str, FieldContext("http://schema.org/description")] = Field()
    licence: Annotated[AnyUrl, FieldContext("http://schema.org/license")] = Field()
    datePublished: Annotated[str, FieldContext("http://schema.org/datePublished")] = (
        Field()
    )
    keyword: Annotated[list[str], FieldContext("http://schema.org/keywords")] = Field(
        default_factory=list
    )
    acknowledgement: Annotated[
        Optional[str], FieldContext("http://schema.org/acknowledgements")
    ] = Field(default=None)
    hasPart: Annotated[
        list[ObjectReference], FieldContext("http://schema.org/hasPart")
    ] = Field()

    model_config = ConfigDict(model_type="http://bia/Study")


class Publication(ROCrateModel):
    title: Annotated[str, FieldContext("http://schema.org/name")] = Field()
    author_names: Annotated[str, FieldContext("http://bia/authorNames")] = Field()

    model_config = ConfigDict(model_type="http://bia/Publication")


# Contributors and Affiliations


class Contributor(ROCrateModel):
    display_name: Annotated[str, FieldContext("http://schema.org/name")] = Field()
    address: Annotated[str, FieldContext("http://schema.org/address")] = Field(
        default=None
    )
    website: Annotated[AnyUrl, FieldContext("http://bia/website")] = Field(default=None)
    affiliation: Annotated[
        list[ObjectReference],
        FieldContext("http://schema.org/affiliation"),
    ] = Field(default_factory=list)
    role: Annotated[str, FieldContext("http://bia/role")] = Field(default=None)

    model_config = ConfigDict(model_type="http://bia/Contributor")


class Affiliaiton(ROCrateModel):
    display_name: Annotated[str, FieldContext("http://schema.org/name")] = Field()
    address: Annotated[str, FieldContext("http://schema.org/address")] = Field(
        default=None
    )
    website: Annotated[AnyUrl, FieldContext("http://bia/website")] = Field(default=None)

    model_config = ConfigDict(model_type="http://bia/Affiliation")


# Grants and funding


class Grant(ROCrateModel):
    pass

    model_config = ConfigDict(model_type="http://bia/Grant")


class FundingBody(ROCrateModel):
    pass

    model_config = ConfigDict(model_type="http://bia/FundingBody")


# External References


class ExternalReference(ROCrateModel):
    link: Annotated[AnyUrl, FieldContext("http://schema/url")] = Field()
    linkDescription: Annotated[
        Optional[str], FieldContext("http://schema/description")
    ] = Field(default=None)

    model_config = ConfigDict(model_type="http://bia/ExternalReference")


# Datasets and associations?


class Dataset(ROCrateModel):
    title: Annotated[str, FieldContext("http://schema.org/name")] = Field()
    description: Annotated[
        Optional[str], FieldContext("http://schema.org/description")
    ] = Field(default=None)

    model_config = ConfigDict(model_type="http://bia/Dataset")


class Association(ROCrateModel):

    model_config = ConfigDict(model_type="http://bia/Association")


# Images, Image represntations


class Image(ROCrateModel):

    model_config = ConfigDict(model_type="http://bia/Image")


# CreationProcess, Specimen


class Specimen(ROCrateModel):
    biological_entity: Annotated[
        list[str], FieldContext("http://bia/biologicalEntity", isIdField=True)
    ] = Field(default_factory=list)
    imaging_preparation_protocol: Annotated[
        list[str], FieldContext("http://bia/imagingPreparationProtocol", isIdField=True)
    ] = Field(default_factory=list)

    model_config = ConfigDict(model_type="http://bia/Specimen")


class CreationProcess(ROCrateModel):
    image_acqusition_protocol: Annotated[
        list[str], FieldContext("http://bia/imageAcquisitionProtocol", isIdField=True)
    ] = Field(default_factory=list)
    specimen: Annotated[
        Optional[str], FieldContext("http://bia/specimen", isIdField=True)
    ] = Field(default=None)
    protocol: Annotated[
        list[str], FieldContext("http://bia/protocol", isIdField=True)
    ] = Field(default_factory=list)
    annotation_method: Annotated[
        list[str], FieldContext("http://bia/annotationMethod", isIdField=True)
    ] = Field(default_factory=list)

    model_config = ConfigDict(model_type="http://bia/CreationProcess")


# BioSample, Taxon


class BioSample(ROCrateModel):
    biological_entity_description: Annotated[
        str, FieldContext("http://bia/biologicalEntityDescription")
    ] = Field()
    experimental_variable_description: Annotated[
        Optional[str], FieldContext("http://bia/experimentalVariableDescription")
    ] = Field(default=None)
    extrinsic_variable_description: Annotated[
        Optional[str], FieldContext("http://bia/extrinsicVariableDescription")
    ] = Field(default=None)
    intrinsic_variable_description: Annotated[
        Optional[str], FieldContext("http://bia/intrinsicVariableDescription")
    ] = Field(default=None)
    organism_classification: Annotated[
        list[ObjectReference], FieldContext("http://bia/taxon")
    ] = Field(default=list)

    model_config = ConfigDict(model_type="http://bia/BioSample")


class Taxon(ROCrateModel):
    common_name: Annotated[Optional[str], FieldContext("http://bia/commonName")] = (
        Field(default=None)
    )
    scientific_name: Annotated[
        Optional[str], FieldContext("http://bia/scientificName")
    ] = Field(default=None)

    model_config = ConfigDict(model_type="http://bia/Taxon")


# Protocols, Signal-channel information for specimen preparation


class Protocol(ROCrateModel):
    title: Annotated[Optional[str], FieldContext("http://schema.org/name")] = Field(
        default=None
    )
    protocol_description: Annotated[
        str, FieldContext("http://schema.org/description")
    ] = Field()

    model_config = ConfigDict(model_type="http://bia/Protocol")


class SpecimenImagingPreparationProtocol(Protocol):
    signal_channel_information: Annotated[
        list[str], FieldContext("http://bia/signalChannelInformation", isIdField=True)
    ] = Field(default_factory=list)

    model_config = ConfigDict(
        model_type="http://bia/SpecimenImagingPreparationProtocol"
    )


class SignalChannelInformation(ROCrateModel):
    signal_contrast_mechanism_description: Annotated[
        Optional[str], FieldContext("http://bia/signalContrastMechanismDescription")
    ] = Field(default=None)
    channel_content_description: Annotated[
        Optional[str], FieldContext("http://bia/channelContentDescription")
    ] = Field(default=None)
    channel_biological_entity: Annotated[
        Optional[str], FieldContext("http://bia/channelBiologicalEntity")
    ] = Field(default=None)

    # TODO make channel number it's own property, because id can't be the number if there's more than one set of channel informations.
    channel_number: Annotated[int, FieldContext("http://bia/channelNumber")] = Field()

    model_config = ConfigDict(model_type="http://bia/SignalChannelInformation")


class ImageAcquisitionProtocol(Protocol):
    imaging_instrument_description: Annotated[
        str, FieldContext("http://bia/imagingInstrumentDescription")
    ] = Field()
    imaging_method_name: Annotated[
        list[str], FieldContext("http://bia/imagingMethodName")
    ] = Field(default_factory=list)
    fbbi_id: Annotated[list[str], FieldContext("http://bia/fbbiId")] = Field(
        default=list
    )

    model_config = ConfigDict(model_type="http://bia/ImageAcquisitionProtocol")


class AnnotationMethod(Protocol):
    annotation_criteria: Annotated[
        Optional[str], FieldContext("http://bia/annotationCriteria")
    ] = Field(default=None)
    annotation_coverage: Annotated[
        Optional[str], FieldContext("http://bia/annotationCoverage")
    ] = Field(default=None)
    transformation_description: Annotated[
        Optional[str], FieldContext("http://bia/transformationDescription")
    ] = Field(default=None)
    spatial_information: Annotated[
        Optional[str], FieldContext("http://bia/spatialInformation")
    ] = Field(default=None)
    method_type: Annotated[Optional[str], FieldContext("http://bia/methodType")] = (
        Field(default=None)
    )
    annotation_source_indicator: Annotated[
        Optional[str], FieldContext("http://bia/annotationSourceIndicator")
    ] = Field(default=None)

    model_config = ConfigDict(model_type="http://bia/AnnotationMethod")


class ImageAnyalysisMethod(Protocol):
    features_analysed: Annotated[
        Optional[str], FieldContext("http://bia/featuresAnalysed")
    ] = Field(default=None)

    model_config = ConfigDict(model_type="http://bia/ImageAnalysisMethod")


class ImageCorrelationMethod(Protocol):
    fiducials_used: Annotated[
        Optional[str], FieldContext("http://bia/fiducialsUsed")
    ] = Field(default=None)
    transformation_matrix: Annotated[
        Optional[str], FieldContext("http://bia/transformationMatrix")
    ] = Field(default=None)

    model_config = ConfigDict(model_type="http://bia/ImageCorrelationMethod")
