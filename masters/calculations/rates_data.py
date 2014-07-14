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
            {"time": 0, "Fe3+": 1.430, "FeTot": 1.412},
            {"time": 5, "Fe3+": 1.193, "FeTot": 1.412},
            {"time": 10, "Fe3+": 0.928, "FeTot": 1.394},
            {"time": 15, "Fe3+": 0.913, "FeTot": 1.433},
            {"time": 20, "Fe3+": 0.842, "FeTot": 1.363},
        ],
        2: [
            {"time": 0, "Fe3+": 1.465, "FeTot": 1.427},
            {"time": 5, "Fe3+": 0.915, "FeTot": 1.423},
            {"time": 10, "Fe3+": 0.757, "FeTot": 1.387},
            {"time": 15, "Fe3+": 0.643, "FeTot": 1.387},
            {"time": 20, "Fe3+": 0.521, "FeTot": 1.372},
        ],
        3: [
            {"time": 0, "Fe3+": 0.721, "FeTot": 0.715},
            {"time": 5, "Fe3+": 0.471, "FeTot": 0.706},
            {"time": 10, "Fe3+": 0.399, "FeTot": 0.713},
            {"time": 15, "Fe3+": 0.374, "FeTot": 0.680},
            {"time": 20, "Fe3+": 0.326, "FeTot": 0.701},

        ]
    },
    "structure": {1: "2_g/L_Cu__9g/L_Fe",
                  2: "4_g/L_Cu__9g/L_Fe",
                  3: "2_g/L_Cu__4.5g/L_Fe",}
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
        constants.COPPER["symbol"]: COPPER_DATA,
        constants.TIN["symbol"]: TIN_DATA,
        constants.ZINC["symbol"]: ZINC_DATA
    }
