# BIA-ro-crate
A CLI tool to convert between BioImage Archive API objects and JSON objects related to RO-crate, zarr, etc.


## Install
```
poetry env use python3.10
poetry install
```

## BIA Image to zarr v4 metadata

Creates ro-crate-metadata.json for an image following ome zarr v4 structure from an image (use uuid of image)

Example use:
```
poetry run bia-ro-crate image-crate 42db9fb5-0f2a-4310-b40b-bc358a6e48b9   
```

Should create a folder 42db9fb5-0f2a-4310-b40b-bc358a6e48b9 with an ro-crate.json inside.

## BIA ingest 

Creates json BIA api objects for the objects in an ro-crate json.

Example use:

```
poetry run bia-ro-crate ingest -c bia_ro_crate/model/example/S-BIAD1494/ro-crate-version
```

This outputs a single json of all the BIA API objects (path can be change with -o option)