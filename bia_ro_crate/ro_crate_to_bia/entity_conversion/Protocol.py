from uuid import UUID
from bia_ro_crate.ro_crate_to_bia.pydantic_ld.ROCrateModel import ROCrateModel
from bia_shared_datamodels import uuid_creation
from bia_integrator_api.models import Protocol as APIProtocol
import bia_ro_crate.ro_crate_to_bia.ingest_models as ROCrateModels

def create_api_protocol(
    crate_objects_by_id: dict[str, ROCrateModel], study_uuid: str
) -> list[APIProtocol]:
    ro_crate_protocol = (
        obj
        for obj in crate_objects_by_id.values()
        if isinstance(obj, ROCrateModels.Protocol)
    )

    protocol_list = []
    for protocol in ro_crate_protocol:
        protocol_list.append(
            convert_protocol(protocol, crate_objects_by_id, study_uuid)
        )

    return protocol_list


def convert_protocol(
    ro_crate_protocol: ROCrateModels.Protocol,
    crate_objects_by_id: dict[str, ROCrateModel],
    study_uuid: UUID,
) -> APIProtocol:
    
    title = None
    if ro_crate_protocol.title:
        title = ro_crate_protocol.title
    elif ro_crate_protocol.id:
        title = ro_crate_protocol.id

    protocol = {
        "uuid": str(uuid_creation.create_protocol_uuid(ro_crate_protocol.id, study_uuid)),
        "title_id": title,
        "protocol_description": ro_crate_protocol.protocol_description,
        "version": 1
    }

    return APIProtocol(**protocol)
