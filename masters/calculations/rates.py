# Python
import math

# Project
from masters.calculations.rates_data import RATES_DATA
from masters.calculations import constants

class ProcessRatesData(object):
    """
    Given experimental data works out actual concentration of metals reactord

    convert:
        - {"time": 0, "Fe3+": 1.430, "FeTot": 1.412}
    To:
        - {"time": 0,
           "Fe3+": {"abs": 1.430, "moles": ""}, "FeTot": {"abs" : 1.412: "moles": ""},
           "rate_init": {"min": "", "sec": ""}, "rate_delta": {"min": "", "sec": ""},
           "metal": {"ion": "", "metal": ""}}

    """
    def __init__(self, component):
        self.component = component
        self.ASSAY_GRADIENT = 0.015
        self.data = RATES_DATA[self.component]
        self.stoichiometry = constants.DATA[self.component]["stoichiometry"]

    def assay_equation(self, value):
        value = value * 100 / (1000 * self.ASSAY_GRADIENT)
        return value

    def moles_iron(self, value):
        return self.assay_equation(value) / constants.DATA[constants.IRON]["Mr"]

    def moles_metal_left(self, initial_metal, rate):
        return (initial_metal / constants.DATA[self.component]["Mr"]) + (rate / self.stoichiometry)

    def run(self):
        for k, v in self.data.iteritems():
            if k == "structure":
                continue
            for k_2, v_2 in v.iteritems():
                i = 1
                for item in v_2:
                    item["Fe3+"]["moles"] = self.moles_iron(item["Fe3+"]["abs"])
                    item["FeTot"]["moles"] = self.moles_iron(item["FeTot"]["abs"])

                    if not (item["time"] == v_2[0]["time"]):
                        item["rate_init"] = {"min": (item["Fe3+"]["moles"] - v_2[0]["Fe3+"]["moles"]) / (item["time"] - v_2[0]["time"]),
                                            "sec": (item["Fe3+"]["moles"] - v_2[0]["Fe3+"]["moles"]) / ((item["time"] - v_2[0]["time"]) * 60.0)}

                        item["rate_delta"] = {"min": (item["Fe3+"]["moles"] - v_2[i - 1]["Fe3+"]["moles"]) / (item["time"] - v_2[i - 1]["time"]),
                                              "sec": (item["Fe3+"]["moles"] - v_2[i - 1]["Fe3+"]["moles"]) / ((item["time"] - v_2[i - 1]["time"]) * 60.0)}
                    else:
                        item["rate_init"] = {"min": 0.0,
                                            "sec": 0.0}
                        item["rate_delta"] = {"min": 0.0,
                                              "sec": 0.0}

                    reacted_metal = self.moles_metal_left(self.data["structure"][k_2]["initial_metal"], item["rate_init"]["min"])
                    item["metal"] = {"metal": reacted_metal,
                                     "ion": (self.data["structure"][k_2]["initial_metal"] / constants.DATA[self.component]["Mr"]) - reacted_metal}
                    ++i

        return self.data

class RateEquation(object):
    """
    Finds the rates equation for different metals based on experimental data

    Calculate the k, a and b values in the initial data
    """
    def __init__(self, component):
        rates = ProcessRatesData(component)
        self.data = rates.run()

    def alpha(self, data_a, data_b):
        if data_b["rate_init"]["min"] == 0.0:
            return 0

        r = data_a["rate_init"]["min"] / data_b["rate_init"]["min"]
        c = data_a["metal"]["metal"] / data_b["metal"]["metal"]
        return math.log(r) / math.log(c)


    def beta(self, data_a, data_b):
        if data_b["rate_init"]["min"] == 0.0:
            return 0

        r = data_a["rate_init"]["min"] / data_b["rate_init"]["min"]
        c = data_a['Fe3+']['moles'] / data_b['Fe3+']['moles']
        return math.log(r) / math.log(c)

    def run(self):
        self.data["rates_constant"] = []
        data_len = len(self.data["data"][1])
        for i in range(data_len):
            self.data["rates_constant"].append({
                "time": self.data["data"][1][i]["time"],
                "a": self.alpha(self.data["data"][1][i], self.data["data"][2][i]),
                # "a": (["rate_init"]["min"] , ["rate_init"]["min"]),
                "b": self.beta(self.data["data"][1][i], self.data["data"][3][i]),
            })
        return self.data
