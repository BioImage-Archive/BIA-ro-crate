from uuid import UUID
from bia_ro_crate.ro_crate_to_bia.pydantic_ld.ROCrateModel import ROCrateModel
from bia_shared_datamodels import uuid_creation, semantic_models
import bia_integrator_api.models as APIModels
import bia_ro_crate.ro_crate_to_bia.ingest_models as ROCrateModels
from pydantic_ld.ROCrateModel import ROCrateModel


def create_api_bio_sample(
    crate_objects_by_id: dict[str, ROCrateModel], study_uuid: str
) -> None:
    ro_crate_bio_sample = [
        (
            obj
            for obj in crate_objects_by_id.values()
            if isinstance(obj, ROCrateModels.BioSample)
        )
    ]

    bio_sample_list = []
    for bio_sample in ro_crate_bio_sample:
        bio_sample_list.append(
            convert_bio_sample(bio_sample, crate_objects_by_id, study_uuid)
        )

    print(bio_sample_list)


def convert_bio_sample(
    ro_crate_bio_sample: ROCrateModels.BioSample,
    crate_objects_by_id: dict[str, ROCrateModel],
    study_uuid: UUID,
) -> APIModels.BioSample:

    taxons = []
    for taxon_id in ro_crate_bio_sample.organism_classification:
        taxons.append(convert_taxon(crate_objects_by_id[taxon_id]))

    bio_sample = {
        "uuid": uuid_creation.create_bio_sample_uuid(
            ro_crate_bio_sample.id, study_uuid
        ),
        "title_id": ro_crate_bio_sample.title,
        "taxon": taxons,
        "biological_entity_description": ro_crate_bio_sample.biological_entity_description,
        "intrinsic_variable_description": ro_crate_bio_sample.intrinsic_variable_description,
        "extrinsic_variable_description": ro_crate_bio_sample.extrinsic_variable_description,
        "experimental_variable_description": ro_crate_bio_sample.experimental_variable_description,
    }

    return APIModels.BioSample(**bio_sample)


def convert_taxon(ro_crate_taxon: ROCrateModels.Taxon) -> semantic_models.Taxon:
    taxon = {
        "common_name": ro_crate_taxon.common_name,
        "scientific_name": ro_crate_taxon.scientific_name,
    }

    if ro_crate_taxon.id.startswith("NCBITaxon:"):
        taxon["id"] = ro_crate_taxon.id
    
    return semantic_models.Taxon(**taxon)
