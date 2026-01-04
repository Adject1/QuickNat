IMPORTANT_INFO = {
    "api_token": "eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjo4MDk4MDM1LCJleHAiOjE3MTgxOTYzMTJ9.e6rKUCmmJLIkLFShSsGKxWpiLKUEGLgR1MCJ_SmeN1G6NtcXbj_AvO35ePKJG9S-z3NuF8I1pKOLDd56OjgqhQ"
}

BASE_URL = "https://api.inaturalist.org/v1"

ANNOTATION_URL = BASE_URL + "/annotations"
ID_URL = BASE_URL + "/identifications"
OBSERVATION_URL = BASE_URL + "/observations"

HEADERS = {
    'Authorization': f'Bearer {IMPORTANT_INFO["api_token"]}',
    'Content-Type': 'application/json'
}

# Bugs evidence of presence - Attribute ID 22
ANNOTATION_EOP = {
    "f": 23,  # Feather
    "o": 24,  # Organism
    "s": 25,  # Scat
    "t": 26,  # Track
    "b": 27,  # Bone
    "e": 30,  # Egg
    "c": 35  # Construction
}

# Alive or Dead - Attribute ID 17
ANNOTATION_LIFE = {
    "a": 18,  # Alive
    "d": 19,  # Dead
    "c": 20  # Cannnot Be Determined
}

# Life Stage - Attribute ID 1
ANNOTATION_STAGE = {
    "a": 2,  # Adult
    "t": 3,  # Teneral
    "p": 4,  # Pupa
    "n": 5,  # Nymph
    "l": 6,  # Larva
    "e": 7,  # Egg
    "j": 8  # Juvenile
}

# Sex - Attribute ID 9
ANNOTATION_SEX = {
    "f": 10,  # Female
    "m": 11,  # Male
    "c": 20  # Cannot Be Determined
}

# This will be for all species I care about enough to identify
# Plus shortforms to make my IDs snappy af (literally the whole point of this)
SPECIES_IDS = {
    # Any key not in this dictionary will skip ID altogether
    "Pontia protodice": 59119,
    "Checkered White": 59119,
    "pp": 59119,
    "Small Milkweed Bug Complex": 1019598,
    "Complex Lygaeus kalmii": 1019598,
    "smbc": 1019598,
    "Lygaeus kalmii": 62045,
    "lk": 62045,
    "Lygaeus kalmii kalmii": 453928,
    "lkk": 453928,
    "Lygaeus kalmii angustomarginatus": 453927,
    "lka": 453927,
    "Lygaeus reclivatus": 261599,
    "lr": 261599,
    "Lygaeus reclivatus reclivatus": 1072445,
    "lrr": 1072445,
    "Lygaeus reclivatus enotus": 1072444,
    "lre": 1072444,
    # Commonly misidentified as the following
    "Xanthochilus saturnius": 325933,
    "Mediterranean Seed Bug": 325933,
    "msb": 325933
}
