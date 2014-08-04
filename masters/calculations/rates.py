# Python
import math

# Project
from masters.calculations.rates_data import RATES_DATA
from masters.calculations import constants

class ProcessRatesData(object):
    """
    Given experimental data works out actual concentration of metals reactord

    convert:
        - {"time": 0, "ferric": 1.430, "FeTot": 1.412}
    To:
        - {"time": 0,
           "ferric": {"abs": 1.430, "moles": ""}, "FeTot": {"abs" : 1.412: "moles": ""},
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
        return self.grams_metal_to_moles(initial_metal) + (rate / self.stoichiometry)

    def grams_metal_to_moles(self, initial_metal):
        return (initial_metal / constants.DATA[self.component]["Mr"]) * 1000 / 100

    def run(self):
        for k, v in self.data.iteritems():
            if k == "structure":
                continue
            # try:
            #     [(k_2, v_2) for k_2, v_2 in v.iteritems()]
            # except:
            #     import ipdb; ipdb.set_trace()
            for k_2, v_2 in v.iteritems():
                i = 1
                for item in v_2:
                    item["ferric"]["moles"] = self.moles_iron(item["ferric"]["abs"])
                    item["FeTot"]["moles"] = self.moles_iron(item["FeTot"]["abs"])
                    ferric_ferrous = item["ferric"]["moles"] / (item["FeTot"]["moles"] - item["ferric"]["moles"])
                    item["ferric_ferrous"] = ferric_ferrous if ferric_ferrous > 0 else 1000

                    if not (item["time"] == v_2[0]["time"]):
                        item["rate_init"] = {"min": (item["ferric"]["moles"] - v_2[0]["ferric"]["moles"]) / (item["time"] - v_2[0]["time"]),
                                            "sec": (item["ferric"]["moles"] - v_2[0]["ferric"]["moles"]) / ((item["time"] - v_2[0]["time"]) * 60.0)}

                        item["rate_delta"] = {"min": (item["ferric"]["moles"] - v_2[i - 1]["ferric"]["moles"]) / (item["time"] - v_2[i - 1]["time"]),
                                              "sec": (item["ferric"]["moles"] - v_2[i - 1]["ferric"]["moles"]) / ((item["time"] - v_2[i - 1]["time"]) * 60.0)}
                    else:
                        item["rate_init"] = {"min": 0.0,
                                            "sec": 0.0}
                        item["rate_delta"] = {"min": 0.0,
                                              "sec": 0.0}

                    diff_iron = (item["ferric"]["moles"] - v_2[0]["ferric"]["moles"])
                    item["delta_ferric"] = diff_iron
                    initial_metal_moles = self.grams_metal_to_moles(self.data["structure"][k_2]["initial_metal"])

                    ion_at_t = diff_iron/constants.DATA[self.component]["stoichiometry"]

                    # if ion_at_t < 0:
                    #     ion_at_t = initial_metal_moles * 0.999

                    metal_at_t = (initial_metal_moles + ion_at_t)
                    item["metal"] = {"ion": abs(ion_at_t),
                                     "metal": metal_at_t if metal_at_t > 0 else initial_metal_moles * 0.001}
                    ++i

        return self.data

class RateEquation(object):
    """
    Finds the rates equation for different metals based on experimental data

    Calculate the k, a and b values in the initial data
    """
    def __init__(self, component, rates_type="ferric"):
       self.component = component
       self.rates_type = rates_type


    def alpha(self, original_c, data_a, data_b):
        if data_b["rate_init"]["min"] == 0.0:
            return 0

        _r = data_a["rate_init"]["min"] / data_b["rate_init"]["min"]
        # _c = data_a["metal"]["metal"] / data_b["metal"]["metal"]
        # return math.log(_r) / math.log(_c)
        return math.log(_r) / math.log(original_c)


    def beta(self, original_f, data_a, data_b):
        if data_b["rate_init"]["min"] == 0.0:
            return 0

        _r = data_a["rate_init"]["min"] / data_b["rate_init"]["min"]

        # if self.rates_type == "ferric_ferrous":
        #     _c = data_a['ferric']['moles'] / data_b['ferric']['moles']
        # else:
        #     _c = data_a['ferric_ferrous'] / data_b['ferric_ferrous']

        # return math.log(_r) / math.log(_c)
        return math.log(_r) / math.log(original_f)

    def rate_constant(self, data, a, b):
        try:
            data["rate_init"]["min"] / ((data["ferric"]["moles"]**a) * (data["metal"]["metal"]**b))
        except Exception:
            return 0.0  # If b is too high the result does not make sense

        if self.rates_type == "ferric_ferrous":
            return data["rate_init"]["min"] / ((data["ferric_ferrous"]**b) * (data["metal"]["metal"]**a))
        else:
            return data["rate_init"]["min"] / ((data["ferric"]["moles"]**b) * (data["metal"]["metal"]**a))

    def run(self):
        rates = ProcessRatesData(self.component)
        data = rates.run().copy()

        data["rates_constant"] = []
        data_len = len(data["data"][1])

        original_c_ratio = (data["data"][1][0]["metal"]["metal"]/ data["data"][2][0]["metal"]["metal"])
        original_f_ratio = (data["data"][1][0]['ferric']['moles']/data["data"][3][0]['ferric']['moles'])

        for i in range(data_len):
            a = self.alpha(original_c_ratio, data["data"][1][i], data["data"][2][i]) # a is for metal dependency
            b = self.beta(original_f_ratio, data["data"][1][i], data["data"][3][i]) # b is for iron dependency

            k_1 = self.rate_constant(data["data"][1][i], a, b)
            k_2 = self.rate_constant(data["data"][2][i], a, b)
            k_3 = self.rate_constant(data["data"][3][i], a, b)

            data["rates_constant"].append({
                "time": data["data"][1][i]["time"],
                "a": a,
                # "a": (["rate_init"]["min"] , ["rate_init"]["min"]),
                "b": b,
                "k": {1 : k_1,
                      2 : k_2,
                      3 : k_3,
                      "average": (k_1 + k_2 + k_3) / 3
                    }
            })
        return data
