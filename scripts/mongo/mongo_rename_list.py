
# Attributes that need to be renamed for Mongo
ATTRIBUTES_TO_UPDATE = [
    "coverage.Temporal.StartTime",
    "coverage.Temporal.StopTime",
    "coverage.Temporal",
    "coverage.Spectral.Bandpass",
    "coverage.Spectral.CentralWavelength",
    "coverage.Spatial",
    "resolution.Spatial",
]

ATTRIBUTE_UPDATE_PAIRS = [(x, x.replace('.', '_')) for x in ATTRIBUTES_TO_UPDATE]

def update_json_text(json_text):
    assert json_text is not None, "json_text cannot be None"

    for attr, updated_attr in ATTRIBUTE_UPDATE_PAIRS:
        json_text = json_text.replace(attr, updated_attr)

    return json_text
