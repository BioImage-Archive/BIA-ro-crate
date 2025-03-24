from uuid import UUID
from bia_ro_crate.ro_crate_to_bia.pydantic_ld.ROCrateModel import ROCrateModel
from bia_shared_datamodels import uuid_creation, semantic_models
from bia_integrator_api.models import Study as APIStudy
import bia_ro_crate.ro_crate_to_bia.ingest_models as ROCrateModels
from pydantic_ld.ROCrateModel import ROCrateModel


def create_api_image_acquisition_protocol(
    crate_objects_by_id: dict[str, ROCrateModel], study_uuid: str
) -> None:
    ro_crate_iap = [
        (
            obj
            for obj in crate_objects_by_id.values()
            if isinstance(obj, ROCrateModels.ImageAcquisitionProtocol)
        )
    ]

    iap_list = []
    for iap in ro_crate_iap:
        iap_list.append(convert_image_acquisition_protocol(iap, crate_objects_by_id, study_uuid))
    
    print(iap_list)


def convert_image_acquisition_protocol(
    ro_crate_iap: ROCrateModels.ImageAcquisitionProtocol,
    crate_objects_by_id: dict[str, ROCrateModel],
    study_uuid: UUID,
) -> semantic_models.ImageAcquisitionProtocol:
    iap = {
        "uuid": uuid_creation.create_image_acquisition_protocol_uuid(ro_crate_iap.id, study_uuid),
        "title": ro_crate_iap.title,
        "protocol_description": ro_crate_iap.protocol_description,
    }

    return semantic_models.ImageAcquisitionProtocol(**iap)
