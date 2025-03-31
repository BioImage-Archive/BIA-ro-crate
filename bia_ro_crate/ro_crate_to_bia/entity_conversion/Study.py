from bia_shared_datamodels import uuid_creation
import bia_integrator_api.models as APIModels
import bia_ro_crate.ro_crate_to_bia.ingest_models as ROCrateModels
from bia_ro_crate.ro_crate_to_bia.pydantic_ld.ROCrateModel import ROCrateModel
from bia_ro_crate.licences import to_code


def create_api_study(crate_objects_by_id: dict[str, ROCrateModel]) -> APIModels.Study:
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

    return study


def convert_study(
    ro_crate_study: ROCrateModels.Study, crate_objects_by_id: dict[str, ROCrateModel]
) -> APIModels.Study:
    accession_id = "S-BIADTEST01"

    contributors = []
    for contributor_id in ro_crate_study.contributor:
        contributors.append(
            convert_contributor(
                crate_objects_by_id[contributor_id], crate_objects_by_id
            )
        )

    external_references = []
    # TODO add logic and to models to handle external links

    study = {
        "accession_id": accession_id,
        "uuid": str(uuid_creation.create_study_uuid(accession_id)),
        "version": 1,
        "title": ro_crate_study.title,
        "description": ro_crate_study.description,
        "release_date": ro_crate_study.datePublished,
        "licence": to_code(str(ro_crate_study.licence)),
        "acknowledgement": ro_crate_study.acknowledgement,
        "keyword": ro_crate_study.keyword,
        "author": contributors,
        "see_also": external_references,
    }

    return APIModels.Study(**study)


def convert_contributor(
    contributor: ROCrateModels.Contributor, crate_objects_by_id: dict[str, ROCrateModel]
) -> APIModels.Contributor:

    affiliations = []
    for affiliation_id in contributor.affiliation:
        affiliations.append(convert_affiliation(crate_objects_by_id[affiliation_id.id]))

    contributor_dictionary = {
        "display_name": contributor.display_name,
        "address": contributor.address,
        "website": contributor.website,
        "role": contributor.role,
        "affiliation": affiliations,
    }

    if contributor.id.startswith("https://orcid.org/"):
        contributor_dictionary["orcid"] = contributor.id
    elif contributor.id.startswith("https://ror.org/"):
        contributor_dictionary["rorid"] = contributor.id

    return APIModels.Contributor(**contributor_dictionary)


def convert_affiliation(
    affiliation: ROCrateModels.Affiliaiton,
) -> APIModels.Affiliation:
    affiliation_dictionary = {
        "display_name": affiliation.display_name,
        "address": affiliation.address,
        "website": affiliation.website,
    }

    if affiliation.id.startswith("https://ror.org/"):
        affiliation_dictionary["rorid"] = affiliation.id

    return APIModels.Affiliation(**affiliation_dictionary)


def convert_external_reference(
    external_reference: ROCrateModels.ExternalReference,
) -> APIModels.ExternalReference:

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

    return APIModels.ExternalReference(**external_reference_dictionary)
