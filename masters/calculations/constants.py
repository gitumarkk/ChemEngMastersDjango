BATCH = "BATCH"
SEMI_BATCH = "SEMI_BATCH"
CONTINUOUS = "CONTINUOUS"  # Assuming no flow of PCBs through the system

COPPER = "Cu"
TIN = "Sn"
ZINC = "Zn"

RATE_DATA = {
    COPPER: {"Mr": 63.546, "equation": {"k": -0.0042, "a": 0.5, "b": 0.64}},
    TIN: {"Mr": 118.71, "equation": {"k": -0.0026, "a": 0.15, "b": 1.312}},
    ZINC: {"Mr": 65.38, "equation": {"k": -0.0161, "a": 1.116, "b": -0.005}}
}
