from masters.calculations import constants

"""
Initial Structure::

{"time": 0, "Fe3+": #, "FeTot": #},


Final Structure::

{"time": 0, "Fe3+": #, "FeTot": #, Fe3+_mol: #, FeTot_mol: #, Fe3+/FeTot: #, initial_rate: #, metal_ions: #},
"""
# {"time": 0, "Fe3+": , "FeTot": },
COPPER_DATA = {
    "data" : {
        1: [
            {"time": 0, "Fe3+": {"abs": 1.430, "moles": ""}, "FeTot": {"abs": 1.412, "moles": ""}},
            {"time": 5, "Fe3+": {"abs": 1.193, "moles": ""}, "FeTot":{"abs": 1.412, "moles": ""}},
            {"time": 10, "Fe3+": {"abs": 0.928, "moles": ""}, "FeTot": {"abs": 1.394, "moles": ""}},
            {"time": 15, "Fe3+": {"abs": 0.913, "moles": ""}, "FeTot": {"abs": 1.433, "moles": ""}},
            {"time": 20, "Fe3+": {"abs": 0.842, "moles": ""}, "FeTot": {"abs": 1.363, "moles": ""}},
        ],
        2: [
            {"time": 0, "Fe3+": {"abs": 1.465, "moles": ""}, "FeTot": {"abs": 1.427, "moles": ""}},
            {"time": 5, "Fe3+": {"abs": 0.915, "moles": ""}, "FeTot": {"abs": 1.423, "1.387oles": ""}},
            {"time": 10, "Fe3+": {"abs": 0.757, "moles": ""}, "FeTot": {"abs": 1.387, "moles": ""}},
            {"time": 15, "Fe3+": {"abs": 0.643, "moles": ""}, "FeTot": {"abs": 1.387, "moles": ""}},
            {"time": 20, "Fe3+": {"abs": 0.521, "moles": ""}, "FeTot": {"abs": 1.372, "moles": ""}},
        ],
        3: [
            {"time": 0, "Fe3+": {"abs": 0.721, "moles": ""}, "FeTot": {"abs": 0.715, "moles": ""}},
            {"time": 5, "Fe3+": {"abs": 0.471, "moles": ""}, "FeTot": {"abs": 0.706, "moles": ""}},
            {"time": 10, "Fe3+": {"abs": 0.399, "moles": ""}, "FeTot": {"abs": 0.713, "moles": ""}},
            {"time": 15, "Fe3+": {"abs": 0.374, "moles": ""}, "FeTot": {"abs": 0.680, "moles": ""}},
            {"time": 20, "Fe3+": {"abs": 0.326, "moles": ""}, "FeTot": {"abs": 0.701, "moles": ""}},

        ]
    },
    "structure": {1: {"name": "2_g/L_Cu__9g/L_Fe", "initial_metal": 2},
                  2: {"name": "4_g/L_Cu__9g/L_Fe", "initial_metal": 4},
                  3: {"name": "2_g/L_Cu__4.5g/L_Fe", "initial_metal": 2}},
}

TIN_DATA = {
    "data": {
        1: [],
        2: [],
        3: []
    },
    "structure": {

    }
}

ZINC_DATA = {
    "data": {
        1: [],
        2: [],
        3: []
    },
    "structure": {

    }
}

RATES_DATA = {
        constants.COPPER: COPPER_DATA,
        constants.TIN: TIN_DATA,
        constants.ZINC: ZINC_DATA
    }
