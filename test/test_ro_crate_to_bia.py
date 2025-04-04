from pathlib import Path
from typer.testing import CliRunner
from bia_ro_crate.cli import bia_ro_crate
import json

runner = CliRunner()


def test_ingest_ro_crate_metadata(tmp_path: Path):

    crate_path = (
        Path(__file__).parents[1]
        / "bia_ro_crate"
        / "model"
        / "example"
        / "S-BIAD1494"
        / "ro-crate-version"
    )

    result = runner.invoke(bia_ro_crate, ["ingest", "-c", crate_path, "-o", tmp_path])

    assert result.exit_code == 0

    with open(tmp_path / "combined_metadata.json") as f:
        cli_out = json.loads(f.read())

    with open(Path(__file__).parent / "ro_crate_to_bia" / "output.json") as f:
        expected_out = json.loads(f.read())

    assert cli_out == expected_out
