from bia_ro_crate.ro_crate_to_bia.pydantic_ld.ROCrateModel import ROCrateModel
from bia_shared_datamodels import uuid_creation
from bia_integrator_api.models import AnnotationMethod as APIAnnotationMethod
import bia_ro_crate.ro_crate_to_bia.ingest_models as ROCrateModels
import logging

logger = logging.getLogger("__main__." + __name__)

def create_api_image_acquisition_protocol(
    crate_objects_by_id: dict[str, ROCrateModel], study_uuid: str
) -> list[APIAnnotationMethod]:
    ro_crate_annotation_method = (
        obj
        for obj in crate_objects_by_id.values()
        if isinstance(obj, ROCrateModels.AnnotationMethod)
    )

    annotation_method_list = []
    for annotation_method in ro_crate_annotation_method:
        annotation_method_list.append(
            convert_annotation_method(
                annotation_method, crate_objects_by_id, study_uuid
            )
        )

    return annotation_method_list


def convert_annotation_method(
    ro_crate_annotation_method: ROCrateModels.AnnotationMethod,
    crate_objects_by_id: dict[str, ROCrateModel],
    study_uuid: str,
) -> APIAnnotationMethod:
    iap = {
        "uuid": uuid_creation.create_annotation_method_uuid(
            ro_crate_annotation_method.id, study_uuid
        ),
        "title_id": ro_crate_annotation_method.title,
        "protocol_description": ro_crate_annotation_method.protocol_description,
        "annotation_criteria": ro_crate_annotation_method.annotation_criteria,
        "annotation_coverage": ro_crate_annotation_method.annotation_coverage,
        "method_type": ro_crate_annotation_method.method_type,
        "annotation_source_indicator": ro_crate_annotation_method.annotation_source_indicator,
    }

    return APIAnnotationMethod(**iap)
