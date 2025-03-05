from bia_integrator_api.models import licence_type

def to_url(licence_code: licence_type) -> str:
    if licence_code == "CC0":
        return "https://creativecommons.org/public-domain/cc0/"
    elif licence_code == "CC_BY-SA_2.1_JP":
        return "https://creativecommons.org/licenses/by-sa/2.1/jp/"
    else:
        version = str(licence_code)[-3:]
        code = str(licence_code)[:-4][3:].replace("_","-").lower()
        return f"https://creativecommons.org/licenses/{code}/{version}/"