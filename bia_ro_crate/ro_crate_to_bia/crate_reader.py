import json
import os
from jsonschema import validate, ValidationError
from pathlib import Path
from pydantic_ld.ROCrateModel import ROCrateModel

from ingest_models import (
    Study,
    Dataset,
    Protocol,
    BioSample,
    SpecimenImagingPreparationProtocol,
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
    pass


def load_entities(data: dict) -> dict[str, ROCrateModel]:
    # TODO: maybe loading using ro-crate libaries would be better
    entities = data.get("@graph", [])
    crate_objects_by_id = {}
    for entity in entities:
        entity_type = entity.get("@type")
        for model in [
            Study,
            Dataset,
            Protocol,
            BioSample,
            SpecimenImagingPreparationProtocol,
        ]:
            if model.model_config.model_type in entity_type:
                object: ROCrateModel = model(**entity)
                crate_objects_by_id[object.id] = object
        else:
            print(f"No suitable bia type found for {entity}")
    return crate_objects_by_id


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


# Example usage
if __name__ == "__main__":
    crate_path = "/path/to/ro_crate.json"

    entities = process_ro_crate(crate_path)
    for entity in entities:
        print(entity)
