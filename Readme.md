# BIA-ro-crate
A CLI tool to convert between BioImage Archive API objects and RO-crate (specifically include those used in the ome-zarr v4 stastandard). 


## Install
```
poetry env use python3.10
poetry install
```

## Running

Example use:
```
poetry run bia-ro-crate 42db9fb5-0f2a-4310-b40b-bc358a6e48b9   
```

Should create a folder 42db9fb5-0f2a-4310-b40b-bc358a6e48b9 with an ro-crate.json inside.