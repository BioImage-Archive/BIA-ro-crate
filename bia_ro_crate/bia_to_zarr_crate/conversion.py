from .bia_client import api_client
import logging
from bia_integrator_api import models
from ome2024_ngff_challenge.zarr_crate.rembi_extension import Biosample, ImageAcquistion, Specimen
from ome2024_ngff_challenge.zarr_crate.zarr_extension import ZarrCrate
from bia_ro_crate.licences import to_url

logger = logging.getLogger("__main__." + __name__)


def fetch_bia_data(image_uuid) -> tuple[list[models.ImageAcquisitionProtocol], list[models.BioSample], models.Study]:

    image = api_client.get_image(image_uuid)
    
    if not image:
        return None

    dataset = api_client.get_dataset(image.submission_dataset_uuid)
    study = api_client.get_study(dataset.submitted_in_study_uuid)
    
    creation_process_uuid = image.creation_process_uuid
    creation_process = api_client.get_creation_process(creation_process_uuid)

    if not creation_process:
        return None

    image_acquisition_processes_list = [
        api_client.get_image_acquisition_protocol(iap_uuid) for iap_uuid in creation_process.image_acquisition_protocol_uuid 
    ]

    specimen = api_client.get_specimen(creation_process.subject_specimen_uuid)

    bio_sample_list = []
    if specimen:
        bio_sample_list = [ api_client.get_bio_sample(bio_sample_uuid) for bio_sample_uuid in specimen.sample_of_uuid ]
        

    return image_acquisition_processes_list, bio_sample_list, study



def create_ro_crate_for_image(image_uuid) -> dict:

    logging.info("Fetching data")
    image_acquisition_processes_list, bio_sample_list, study = fetch_bia_data(image_uuid)


    crate = ZarrCrate()

    zarr_root = crate.add_dataset(
        "./",
        properties={
            "name": study.title,
            "description": study.description,
            "licence": to_url(study.licence),
        },
    )

    bio_sample_crate_list = []
    for bio_sample in bio_sample_list:
        taxon_ids = [ {"@id": taxon.ncbi_id}  for taxon in bio_sample.organism_classification]
        bio_sample_crate = crate.add(
            Biosample(crate, properties={"organism_classification": taxon_ids})
        )
        bio_sample_crate_list.append(bio_sample_crate)
    
    specimen_crate = crate.add(Specimen(crate, bio_sample_crate_list))
    

    image_acquisition_crate_list = []
    for image_acquisition in image_acquisition_processes_list:
        imaging_types = [ {"@id": imaging_method} for imaging_method in image_acquisition.fbbi_id ]
        image_acquisition_crate = crate.add(
            ImageAcquistion(crate, specimen_crate, properties={"fbbi_id": imaging_types})
        )
        image_acquisition_crate_list.append(image_acquisition_crate)

    zarr_root["resultOf"] = image_acquisition_crate_list

    metadata_dict = crate.metadata.generate()

    return metadata_dict
