from rocrate_validator import services, models
from pathlib import Path

bia_crate = Path(__file__).parents[1] / "model" / "example" / "S-BIAD1494" / "ro-crate-version"

settings = services.ValidationSettings(
    rocrate_uri=bia_crate,
    profile_identifier='ro-crate-1.1'
)

result = services.validate(settings)

if result.has_issues():
    for issue in result.get_issues():
        print(f"\"{issue.check.identifier}\": {issue.message}")
else:
    print("ro-crate metadata passes validation!")


