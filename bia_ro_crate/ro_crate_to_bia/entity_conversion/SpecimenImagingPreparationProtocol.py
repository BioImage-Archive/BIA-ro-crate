from uuid import UUID
from bia_ro_crate.ro_crate_to_bia.pydantic_ld.ROCrateModel import ROCrateModel
from bia_shared_datamodels import uuid_creation, semantic_models
from bia_integrator_api.models import Study as APIStudy
import bia_ro_crate.ro_crate_to_bia.ingest_models as ROCrateModels
from pydantic_ld.ROCrateModel import ROCrateModel


def create_api_specimen_imaging_preparation_protocol(
    crate_objects_by_id: dict[str, ROCrateModel], study_uuid: str
) -> None:
    ro_crate_sipp = [
        (
            obj
            for obj in crate_objects_by_id.values()
            if isinstance(obj, ROCrateModels.SpecimenImagingPreparationProtocol)
        )
    ]

    sipp_list = []
    for sipp in ro_crate_sipp:
        sipp_list.append(convert_specimen_imaging_preparation_protocol(sipp, crate_objects_by_id, study_uuid))
    
    print(sipp_list)


def convert_specimen_imaging_preparation_protocol(
    ro_crate_sipp: ROCrateModels.SpecimenImagingPreparationProtocol,
    crate_objects_by_id: dict[str, ROCrateModel],
    study_uuid: UUID,
) -> semantic_models.SpecimenImagingPreparationProtocol:
    sipp = {
        "uuid": uuid_creation.create_specimen_imaging_preparation_protocol_uuid(ro_crate_sipp.id, study_uuid),
        "title": ro_crate_sipp.title,
        "protocol_description": ro_crate_sipp.protocol_description,
    }

    return semantic_models.SpecimenImagingPreparationProtocol(**sipp)
