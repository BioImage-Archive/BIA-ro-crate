from uuid import UUID
from bia_ro_crate.ro_crate_to_bia.pydantic_ld.ROCrateModel import ROCrateModel
from bia_shared_datamodels import uuid_creation
import bia_integrator_api.models as APIModels
import bia_ro_crate.ro_crate_to_bia.ingest_models as ROCrateModels


def create_api_dataset(
    crate_objects_by_id: dict[str, ROCrateModel], study_uuid: str
) -> list[APIModels.Dataset]:
    ro_crate_datasets = (
        obj
        for obj in crate_objects_by_id.values()
        if isinstance(obj, ROCrateModels.Dataset)
    )

    dataset_list = []
    for dataset in ro_crate_datasets:
        dataset_list.append(
            convert_image_acquisition_protocol(dataset, crate_objects_by_id, study_uuid)
        )

    return dataset_list


def convert_image_acquisition_protocol(
    ro_crate_dataset: ROCrateModels.Dataset,
    crate_objects_by_id: dict[str, ROCrateModel],
    study_uuid: UUID,
) -> APIModels.Dataset:

    title = None
    if ro_crate_dataset.title:
        title = ro_crate_dataset.title
    elif ro_crate_dataset.id:
        title = ro_crate_dataset.id

    dataset = {
        "uuid": str(
            uuid_creation.create_image_acquisition_protocol_uuid(
                ro_crate_dataset.id, study_uuid
            )
        ),
        "submitted_in_study_uuid": study_uuid,
        "title_id": title,
        "description": ro_crate_dataset.description,
        "version": 1,
        "example_image_uri": []
    }

    return APIModels.Dataset(**dataset)
