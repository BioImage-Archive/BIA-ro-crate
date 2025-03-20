from bia_ro_crate.ro_crate_to_bia.ld_context.SimpleJSONLDContext import SimpleJSONLDContext
from bia_ro_crate.ro_crate_to_bia.pydantic_ld.FieldContext import FieldContext
from bia_ro_crate.ro_crate_to_bia.ld_context.ContextTerm import ContextTerm
from bia_ro_crate.ro_crate_to_bia.ingest_models import Study, BioSample, Contributor
from rdflib.graph import Graph
from pathlib import Path
import json

# bia_ontology = Graph()
# bia_ontology.parse(str(Path(__file__).parents[1]/"model"/"model.ttl"))

schema = Graph()
schema.parse("https://schema.org/version/latest/schemaorg-current-http.ttl")

dc = Graph()
dc.parse("https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_terms.ttl")

combined_ontology = schema + dc


prefixes={"schema": "http://schema.org/", "dc": "http://purl.org/dc/terms/", "bia": "http://bia/"}

context = SimpleJSONLDContext(prefixes=prefixes)

for ldclass in [Study, BioSample, Contributor]:
    ldclass.validate_ontology_field_consistency(combined_ontology)

    for field_term in ldclass.generate_field_context():
        context.add_term(field_term)

print(json.dumps(context.to_dict(),indent=2))