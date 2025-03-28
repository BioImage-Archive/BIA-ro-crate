from bia_shared_datamodels import uuid_creation, semantic_models
from bia_integrator_api.models import Study as APIStudy
import bia_ro_crate.ro_crate_to_bia.ingest_models as ROCrateModels
from pydantic_ld.ROCrateModel import ROCrateModel


def create_api_study(crate_objects_by_id: dict[str, ROCrateModel]) -> None:
    ro_crate_studies = (
        obj
        for obj in crate_objects_by_id.values()
        if isinstance(obj, ROCrateModels.Study)
    )

    ro_crate_studies_list = list(ro_crate_studies)

    if len(ro_crate_studies_list) != 1:
        raise ValueError(
            f"Expected exactly one Study object, found {len(ro_crate_studies_list)}"
        )

    study = convert_study(ro_crate_studies_list[0], crate_objects_by_id)

    print(study)


def convert_study(
    ro_crate_study: ROCrateModels.Study, crate_objects_by_id: dict[str, ROCrateModel]
) -> APIStudy:
    accession_id = "S-BIADTEST01"

    contributors = []
    for contributor_id in ro_crate_study.contributor:
        contributors.append(convert_contributor(crate_objects_by_id[contributor_id], crate_objects_by_id))

    study = {
        "accession_id": accession_id,
        "uuid": str(uuid_creation.create_study_uuid(accession_id)),
        "version": 1,
        "title": ro_crate_study.title,
        "description": ro_crate_study.description,
        "release_date": ro_crate_study.datePublished,
        "licence": ro_crate_study.licence,
        "acknowledgement": ro_crate_study.acknowledgement,
        "keyword": ro_crate_study.keyword,
        "author": contributors,
    }

    return APIStudy(**study)


def convert_contributor(
    contributor: ROCrateModels.Contributor, crate_objects_by_id: dict[str, ROCrateModel]
) -> semantic_models.Contributor:

    affiliations = []
    for affiliation_id in contributor.affiliation:
        affiliations.append(convert_affiliation(crate_objects_by_id[affiliation_id.id]))

    contributor_dictionary = {
        "display_name": contributor.display_name,
        "address": contributor.address,
        "website": contributor.website,
        "role": contributor.role,
        "affiliation": affiliations
    }

    if contributor.id.startswith("http://orcid.org/"):
        contributor_dictionary["orcid"] = contributor.id
    elif contributor.id.startswith("https://ror.org/"):
        contributor_dictionary["rorid"] = contributor.id

    return semantic_models.Contributor(**contributor_dictionary)


def convert_affiliation(
    affiliation: ROCrateModels.Affiliaiton,
) -> semantic_models.Affiliation:
    affiliation_dictionary = {
        "display_name": affiliation.display_name,
        "address": affiliation.address,
        "website": affiliation.website,
    }

    if affiliation.id.startswith("https://ror.org/"):
        affiliation_dictionary["rorid"] = affiliation.id

    return semantic_models.Affiliation(**affiliation_dictionary)


def convert_external_reference(
    external_reference: ROCrateModels.ExternalReference,
) -> semantic_models.ExternalReference:

    link_type_map = {}

    link_type = None
    for key in link_type_map.keys():
        if str(external_reference.link).startswith(key):
            link_type = link_type_map[key]
            break

    external_reference_dictionary = {
        "link": external_reference.link,
        "description": external_reference.linkDescription,
        "link_type": link_type,
    }

    return semantic_models.ExternalReference(**external_reference_dictionary)
