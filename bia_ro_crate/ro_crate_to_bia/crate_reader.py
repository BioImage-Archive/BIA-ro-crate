import json
import os
from pathlib import Path
from pydantic_ld.ROCrateModel import ROCrateModel
from rocrate.rocrate import ROCrate
import ingest_models
import inspect
import pyld
from bia_ro_crate.ro_crate_to_bia.entity_conversion import (
    AnnotationMethod,
    BioSample,
    Dataset,
    FileReference,
    Image,
    ImageAcquisitionProtocol,
    Protocol,
    Specimen,
    SpecimenImagingPreparationProtocol,
    Study,
)

def read_json_from_ro_crate(crate_path: str) -> dict:
    crate_path: Path = Path(crate_path)

    if crate_path.is_dir():
        crate_metadata_path = crate_path / "ro-crate-metadata.json"
    else:
        crate_metadata_path = crate_path

    if not os.path.exists(crate_metadata_path):
        raise FileNotFoundError(f"File {crate_metadata_path} not found.")

    with open(crate_metadata_path, "r") as file:
        data = json.load(file)

    return data


def validate_json(data):
    return True


def load_entities(data: dict) -> dict[str, ROCrateModel]:
    # TODO: maybe loading using ro-crate libaries would be better
    context = data.get("@context", {})
    entities = data.get("@graph", [])
    crate_objects_by_id = {}
    classes = inspect.getmembers(
        ingest_models,
        lambda member: inspect.isclass(member) and member.__module__ == "ingest_models",
    )

    for entity in entities:
        entity_type = expand_entity(entity, context).get("@type")
        for name, model in classes:
            if model.model_config["model_type"] in entity_type:
                object: ROCrateModel = model(**entity)
                crate_objects_by_id[object.id] = object
        else:
            print(f"No suitable bia type found for {entity}")
    return crate_objects_by_id


def crate_read(path: Path):
    crate = ROCrate(path)
    return crate


def process_ro_crate(crate_path):
    data = read_json_from_ro_crate(crate_path)
    if validate_json(data):
        return load_entities(data)
    else:
        print("Invalid JSON data.")
        return []


def map_files_to_datasets(crate_path: str, datasets: list):
    crate_path = Path(crate_path)
    files = []

    for root, _, filenames in os.walk(crate_path):
        for filename in filenames:
            file_path = Path(root) / filename
            files.append(file_path)

    file_mapping = {}
    for file in files:
        for dataset in datasets:
            if dataset.id in str(file):
                if dataset.id not in file_mapping:
                    file_mapping[dataset.id] = []
                file_mapping[dataset.id].append(file)

    return file_mapping


def expand_entity(entity: dict, context: dict) -> str:
    document = {"@context": context, "@graph": [entity]}
    expanded = pyld.jsonld.expand(document)
    assert len(expanded) == 1
    return expanded[0]


# Example usage
if __name__ == "__main__":
    crate_path = (
        Path(__file__).parents[1]
        / "model"
        / "example"
        / "S-BIAD1494"
        / "ro-crate-version"
    )

    crate = crate_read(crate_path)

    entities = process_ro_crate(crate_path)


    Study.create_api_study(entities)

    study_uuid = "S-BIAD1494"

    AnnotationMethod.create_api_image_acquisition_protocol(entities, study_uuid)
    Protocol.create_api_protocol(entities, study_uuid)
    BioSample.create_api_bio_sample(entities, study_uuid)
    ImageAcquisitionProtocol.create_api_image_acquisition_protocol(entities, study_uuid)
    SpecimenImagingPreparationProtocol.create_api_specimen_imaging_preparation_protocol(entities, study_uuid)