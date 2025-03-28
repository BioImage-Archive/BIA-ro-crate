import typer
import logging
import json
from typing import Annotated, Optional
from uuid import UUID
from pydantic import RootModel, BaseModel
from bia_ro_crate.ro_crate_to_bia.crate_reader import crate_read, process_ro_crate
from bia_ro_crate.ro_crate_to_bia.entity_conversion import (
    AnnotationMethod,
    BioSample,
    Dataset,
    ImageAcquisitionProtocol,
    Protocol,
    SpecimenImagingPreparationProtocol,
    Study,
)
from .bia_to_zarr_crate.conversion import create_ro_crate_for_image
from pathlib import Path
import os
from rich.logging import RichHandler

bia_ro_crate = typer.Typer()

logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger()


@bia_ro_crate.command("image-crate")
def image_crate(
    uuid_list: Annotated[
        list[UUID],
        typer.Argument(help="UUIDs of images for which to create ro-crate json."),
    ],
    output_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--output-dir",
            "-o",
            case_sensitive=False,
            help="path where to create the ro-crate. Each will be a ro-crate.json file nested inside a directory named by uuid of the image.",
        ),
    ] = Path(__file__).parents[1],
):

    for uuid in uuid_list:
        ro_crate_metadata = create_ro_crate_for_image(str(uuid))

        image_dir = output_dir / str(uuid)
        if not os.path.isdir(image_dir):
            if os.path.exists(image_dir):
                raise NotADirectoryError(f"{image_dir} exists but is not a directory.")
            os.mkdir(image_dir)

        logging.info(f"Saving ro-crate.json in {image_dir}")
        with open(image_dir / "ro-crate.json", "w") as f:
            f.write(json.dumps(ro_crate_metadata, indent=2))


@bia_ro_crate.command("ingest")
def convert(
    output_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--output-dir",
            "-o",
            case_sensitive=False,
        ),
    ] = Path(__file__).parents[1],
):
    crate_path = (
        Path(__file__).parents[0]
        / "model"
        / "example"
        / "S-BIAD1494"
        / "ro-crate-version"
    )

    crate = crate_read(crate_path)

    entities = process_ro_crate(crate_path)

    api_objects = []

    study = Study.create_api_study(entities)
    api_objects.append(study)

    study_uuid = study.uuid

    api_objects += Dataset.create_api_dataset(entities, study_uuid)
    api_objects += AnnotationMethod.create_api_image_acquisition_protocol(
        entities, study_uuid
    )
    api_objects += Protocol.create_api_protocol(entities, study_uuid)
    api_objects += BioSample.create_api_bio_sample(entities, study_uuid)
    api_objects += ImageAcquisitionProtocol.create_api_image_acquisition_protocol(
        entities, study_uuid
    )
    api_objects += SpecimenImagingPreparationProtocol.create_api_specimen_imaging_preparation_protocol(
        entities, study_uuid
    )

    ApiModels = RootModel[list]
    write_out = ApiModels(api_objects)

    with open(output_dir / "combined_metadata.json", "w") as f:
        f.write(write_out.model_dump_json(indent=2))
