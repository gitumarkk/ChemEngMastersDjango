BATCH = "BATCH"
SEMI_BATCH = "SEMI_BATCH"
CONTINUOUS = "CONTINUOUS"  # Assuming no flow of PCBs through the system

COPPER = "Cu"
TIN = "Sn"
ZINC = "Zn"
IRON = "Fe"

DATA = {
    COPPER: {
        "Mr": 63.546,
        # "equation": {"k": -0.0042, "a": 0.5, "b": 0.64},
        "equation": {"n": 0.56, "K": 0.2615748/60},
        "stoichiometry": 2,
    },

    TIN: {
        "Mr": 118.71,
        "equation": {"k": -0.0026, "a": 0.15, "b": 1.312},
        "stoichiometry": 4,
    },
    # ZINC: {"Mr": 65.38, "equation": {"k": -0.0161, "a": 1.116, "b": -0.005}}
    ZINC: {
        "Mr": 65.38,
        "equation": {"k": -0.0161, "a": 1.116, "b": 0},
        "stoichiometry": 2
    },
    IRON: {
        "Mr": 55.845
    }
}
# ZINC: b = -0.005 but since it is small can it be effectiviley 0
