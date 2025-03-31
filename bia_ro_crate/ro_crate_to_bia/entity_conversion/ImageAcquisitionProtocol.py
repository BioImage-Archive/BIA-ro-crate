from uuid import UUID
from bia_ro_crate.ro_crate_to_bia.pydantic_ld.ROCrateModel import ROCrateModel
from bia_shared_datamodels import uuid_creation
from bia_integrator_api.models import ImageAcquisitionProtocol as APIIAP
import bia_ro_crate.ro_crate_to_bia.ingest_models as ROCrateModels


def create_api_image_acquisition_protocol(
    crate_objects_by_id: dict[str, ROCrateModel], study_uuid: str
) -> list[APIIAP]:
    ro_crate_iap = (
        obj
        for obj in crate_objects_by_id.values()
        if isinstance(obj, ROCrateModels.ImageAcquisitionProtocol)
    )

    iap_list = []
    for iap in ro_crate_iap:
        iap_list.append(
            convert_image_acquisition_protocol(iap, crate_objects_by_id, study_uuid)
        )

    return iap_list


def convert_image_acquisition_protocol(
    ro_crate_iap: ROCrateModels.ImageAcquisitionProtocol,
    crate_objects_by_id: dict[str, ROCrateModel],
    study_uuid: UUID,
) -> APIIAP:

    title = None
    if ro_crate_iap.title:
        title = ro_crate_iap.title
    elif ro_crate_iap.id:
        title = ro_crate_iap.id

    iap = {
        "uuid": str(
            uuid_creation.create_image_acquisition_protocol_uuid(
                ro_crate_iap.id, study_uuid
            )
        ),
        "title_id": title,
        "protocol_description": ro_crate_iap.protocol_description,
        "imaging_instrument_description": ro_crate_iap.imaging_instrument_description,
        "imaging_method_name": ro_crate_iap.imaging_method_name,
        "fbbi_id": ro_crate_iap.fbbi_id,
        "version": 1,
    }

    return APIIAP(**iap)
