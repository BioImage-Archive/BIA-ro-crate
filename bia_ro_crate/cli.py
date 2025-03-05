import typer
import logging
import json
from typing import Annotated, Optional
from uuid import UUID
from .bia_to_zarr_crate.conversion import create_ro_crate_for_image
from pathlib import Path
import os
from rich.logging import RichHandler


bia_ro_crate = typer.Typer()

logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger()


@bia_ro_crate.command('image-crate')
def image_crate(
    uuid_list: Annotated[list[UUID], typer.Argument(help="UUIDs of images for which to create ro-crate json.")],
    output_dir: Annotated[
        Optional[Path], 
        typer.Option(
            "--output-dir", "-o",
            case_sensitive=False,
            help="path where to create the ro-crate. Each will be a ro-crate.json file nested inside a directory named by uuid of the image.",
        )
    ] = Path(__file__).parents[1]
):
    
    for uuid in uuid_list:
        ro_crate_metadata = create_ro_crate_for_image(str(uuid))

        image_dir = output_dir / str(uuid)
        if not os.path.isdir(image_dir):
            if os.path.exists(image_dir):
                raise NotADirectoryError(f"{image_dir} exists but is not a directory.")
            os.mkdir(image_dir)

        with open(image_dir/"ro-crate.json", 'w') as f:
            f.write(json.dumps(ro_crate_metadata, indent=2)) 

