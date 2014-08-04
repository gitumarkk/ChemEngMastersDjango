from masters.calculations import constants

"""
Initial Structure::

{"time": 0, "ferric": #, "FeTot": #},


Final Structure::

{"time": 0, "ferric": #, "FeTot": #, ferric_mol: #, FeTot_mol: #, ferric/FeTot: #, initial_rate: #, metal_ions: #},
"""
# {"time": 0, "ferric": , "FeTot": },
COPPER_DATA = {
    "data" : {
        1: [
            {"time": 0, "ferric": {"abs": 1.430, "moles": ""}, "FeTot": {"abs": 1.412, "moles": ""}},
            {"time": 5, "ferric": {"abs": 1.193, "moles": ""}, "FeTot":{"abs": 1.412, "moles": ""}},
            {"time": 10, "ferric": {"abs": 0.928, "moles": ""}, "FeTot": {"abs": 1.394, "moles": ""}},
            {"time": 15, "ferric": {"abs": 0.913, "moles": ""}, "FeTot": {"abs": 1.433, "moles": ""}},
            {"time": 20, "ferric": {"abs": 0.842, "moles": ""}, "FeTot": {"abs": 1.363, "moles": ""}},
        ],
        2: [
            {"time": 0, "ferric": {"abs": 1.465, "moles": ""}, "FeTot": {"abs": 1.427, "moles": ""}},
            {"time": 5, "ferric": {"abs": 0.915, "moles": ""}, "FeTot": {"abs": 1.423, "moles": ""}},
            {"time": 10, "ferric": {"abs": 0.757, "moles": ""}, "FeTot": {"abs": 1.387, "moles": ""}},
            {"time": 15, "ferric": {"abs": 0.643, "moles": ""}, "FeTot": {"abs": 1.387, "moles": ""}},
            {"time": 20, "ferric": {"abs": 0.521, "moles": ""}, "FeTot": {"abs": 1.372, "moles": ""}},
        ],
        3: [
            {"time": 0, "ferric": {"abs": 0.721, "moles": ""}, "FeTot": {"abs": 0.715, "moles": ""}},
            {"time": 5, "ferric": {"abs": 0.471, "moles": ""}, "FeTot": {"abs": 0.706, "moles": ""}},
            {"time": 10, "ferric": {"abs": 0.399, "moles": ""}, "FeTot": {"abs": 0.713, "moles": ""}},
            {"time": 15, "ferric": {"abs": 0.374, "moles": ""}, "FeTot": {"abs": 0.680, "moles": ""}},
            {"time": 20, "ferric": {"abs": 0.326, "moles": ""}, "FeTot": {"abs": 0.701, "moles": ""}},

        ]
    },
    "structure": {1: {"name": "2_g/L_Cu__9g/L_Fe", "initial_metal": 0.2034},
                  2: {"name": "4_g/L_Cu__9g/L_Fe", "initial_metal": 0.4075},
                  3: {"name": "2_g/L_Cu__4.5g/L_Fe", "initial_metal": 0.2065}},
}

TIN_DATA = {
    "data" : {
        1: [
            {"time": 0, "ferric": {"abs": 1.657, "moles": ""}, "FeTot": {"abs": 1.577, "moles": ""}},
            {"time": 5, "ferric": {"abs": 1.403, "moles": ""}, "FeTot": {"abs": 1.637, "moles": ""}},
            {"time": 10, "ferric": {"abs": 1.194, "moles": ""}, "FeTot": {"abs": 1.582, "moles": ""}},
            {"time": 15, "ferric": {"abs": 1.183, "moles": ""}, "FeTot": {"abs": 1.547, "moles": ""}},
            {"time": 20, "ferric": {"abs": 1.082, "moles": ""}, "FeTot": {"abs": 1.584, "moles": ""}},
            {"time": 25, "ferric": {"abs": 1.146, "moles": ""}, "FeTot": {"abs": 1.581, "moles": ""}},
            {"time": 30, "ferric": {"abs": 1.062, "moles": ""}, "FeTot": {"abs": 1.552, "moles": ""}},
        ],
        2: [
            {"time": 0, "ferric": {"abs": 1.638, "moles": ""}, "FeTot": {"abs": 1.657, "moles": ""}},
            {"time": 5, "ferric": {"abs": 1.246, "moles": ""}, "FeTot":{"abs": 1.611, "moles": ""}},
            {"time": 10, "ferric": {"abs": 1.124, "moles": ""}, "FeTot": {"abs": 1.582, "moles": ""}},
            {"time": 15, "ferric": {"abs": 0.858, "moles": ""}, "FeTot": {"abs": 1.602, "moles": ""}},
            {"time": 20, "ferric": {"abs": 0.777, "moles": ""}, "FeTot": {"abs": 1.600, "moles": ""}},
            {"time": 25, "ferric": {"abs": 0.703, "moles": ""}, "FeTot": {"abs": 1.575, "moles": ""}},
            {"time": 30, "ferric": {"abs": 0.716, "moles": ""}, "FeTot": {"abs": 1.641, "moles": ""}},
        ],
        3: [
            {"time": 0, "ferric": {"abs": 0.823, "moles": ""}, "FeTot": {"abs": 0.858, "moles": ""}},
            {"time": 5, "ferric": {"abs": 0.677, "moles": ""}, "FeTot": {"abs": 0.811, "moles": ""}},
            {"time": 10, "ferric": {"abs": 0.625, "moles": ""}, "FeTot": {"abs": 0.829, "moles": ""}},
            {"time": 15, "ferric": {"abs": 0.547, "moles": ""}, "FeTot": {"abs": 0.791, "moles": ""}},
            {"time": 20, "ferric": {"abs": 0.531, "moles": ""}, "FeTot": {"abs": 0.877, "moles": ""}},
            {"time": 25, "ferric": {"abs": 0.498, "moles": ""}, "FeTot": {"abs": 0.858, "moles": ""}},
            {"time": 30, "ferric": {"abs": 0.470, "moles": ""}, "FeTot": {"abs": 0.801, "moles": ""}},
        ]
    },
    "structure": {1: {"name": "2_g/L_Sn__11g/L_Fe", "initial_metal": 2},
                  2: {"name": "4_g/L_Sn__11g/L_Fe", "initial_metal": 4},
                  3: {"name": "2_g/L_Sn__5.5g/L_Fe", "initial_metal": 2}},
}

ZINC_DATA = {
    "data" : {
        1: [
            {"time": 0, "ferric": {"abs": 1.540, "moles": ""}, "FeTot": {"abs": 1.541, "moles": ""}},
            {"time": 5, "ferric": {"abs": 1.166, "moles": ""}, "FeTot":{"abs": 1.560, "moles": ""}},
            {"time": 10, "ferric": {"abs": 1.158, "moles": ""}, "FeTot": {"abs": 1.558, "moles": ""}},
            {"time": 15, "ferric": {"abs": 1.168, "moles": ""}, "FeTot": {"abs": 1.566, "moles": ""}},
            {"time": 20, "ferric": {"abs": 1.122, "moles": ""}, "FeTot": {"abs": 1.596, "moles": ""}},
            {"time": 25, "ferric": {"abs": 1.134, "moles": ""}, "FeTot": {"abs": 1.571, "moles": ""}},
            {"time": 30, "ferric": {"abs": 1.108, "moles": ""}, "FeTot": {"abs": 1.583, "moles": ""}},
        ],
        2: [
            {"time": 0, "ferric": {"abs": 1.595, "moles": ""}, "FeTot": {"abs": 1.618, "moles": ""}},
            {"time": 5, "ferric": {"abs": 0.861, "moles": ""}, "FeTot": {"abs": 1.570, "moles": ""}},
            {"time": 10, "ferric": {"abs": 0.799, "moles": ""}, "FeTot": {"abs": 1.574, "moles": ""}},
            {"time": 15, "ferric": {"abs": 0.743, "moles": ""}, "FeTot": {"abs": 1.565, "moles": ""}},
            {"time": 20, "ferric": {"abs": 0.746, "moles": ""}, "FeTot": {"abs": 1.585, "moles": ""}},
            {"time": 25, "ferric": {"abs": 0.713, "moles": ""}, "FeTot": {"abs": 1.548, "moles": ""}},
            {"time": 30, "ferric": {"abs": 0.726, "moles": ""}, "FeTot": {"abs": 1.565, "moles": ""}},
        ],
        3: [
            {"time": 0, "ferric": {"abs": 0.767, "moles": ""}, "FeTot": {"abs": 0.777, "moles": ""}},
            {"time": 5, "ferric": {"abs": 0.421, "moles": ""}, "FeTot": {"abs": 0.778, "moles": ""}},
            {"time": 10, "ferric": {"abs": 0.383, "moles": ""}, "FeTot": {"abs": 0.804, "moles": ""}},
            {"time": 15, "ferric": {"abs": 0.387, "moles": ""}, "FeTot": {"abs": 0.786, "moles": ""}},
            {"time": 20, "ferric": {"abs": 0.387, "moles": ""}, "FeTot": {"abs": 0.809, "moles": ""}},
            {"time": 25, "ferric": {"abs": 0.371, "moles": ""}, "FeTot": {"abs": 0.783, "moles": ""}},
            {"time": 30, "ferric": {"abs": 0.376, "moles": ""}, "FeTot": {"abs": 0.808, "moles": ""}},

        ]
    },
    "structure": {1: {"name": "2_g/L_Zn__11g/L_Fe", "initial_metal": 0.2081},
                  2: {"name": "4_g/L_Zn__11g/L_Fe", "initial_metal": 0.4017},
                  3: {"name": "2_g/L_Zn__5.5g/L_Fe", "initial_metal": 0.2046}},
}

RATES_DATA = {
        constants.COPPER: COPPER_DATA,
        constants.TIN: TIN_DATA,
        constants.ZINC: ZINC_DATA
    }

# {
#     "data" : {
#         1: [
#             {"time": 0, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},
#             {"time": 5, "ferric": {"abs": 0, "moles": ""}, "FeTot":{"abs": 0, "moles": ""}},
#             {"time": 10, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},
#             {"time": 15, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},
#             {"time": 20, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},
#         ],
#         2: [
#             {"time": 0, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},
#             {"time": 5, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},
#             {"time": 10, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},
#             {"time": 15, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},
#             {"time": 20, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},
#         ],
#         3: [
#             {"time": 0, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},
#             {"time": 5, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},
#             {"time": 10, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},
#             {"time": 15, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},
#             {"time": 20, "ferric": {"abs": 0, "moles": ""}, "FeTot": {"abs": 0, "moles": ""}},

#         ]
#     },
#     "structure": {1: {"name": "2_g/L_Sn__9g/L_Fe", "initial_metal": 2},
#                   2: {"name": "4_g/L_Sn__9g/L_Fe", "initial_metal": 4},
#                   3: {"name": "2_g/L_Sn__4.5g/L_Fe", "initial_metal": 2}},
# }
