from masters.calculations.rates_data import RATES_DATA


class ProcessRatesData(object):
    """
    Given experimental data works out actual concentration of metals reactord
    """
    def __init__(self, run=None):
        self.run = run

    def get_experiment_data(self):
        RATES_DATA[self.run]

    def assay_equation(self):
        pass

    def moles_iron(self):
        pass

    def moles_metal_reacted(self):
        pass

    def stoichiometry(self):
        # Assume 2 initially
        return 2

class RateEquation(object):
    """
    Finds the rates equation for different metals based on experimental data
    """
