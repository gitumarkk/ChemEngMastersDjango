from masters.calculations import constants

import numpy as np

class Bioxidation(object):
    def __init__(self):
        pass

    def inhibited(self):
        pass

    def simplified_hansford(self):
        pass


class CopperDissolutionRate(object):
    def __init__(self, copper_initial, initial_ferric=None, system=None):
        self.copper = copper_initial
        self.ferric = initial_ferric
        self.system = system or constants.BATCH

    def copper_metal_powder_rate(self):
        # Copper concentration depends on the next step
        K = -0.0042
        a = 0.5
        b = 0.64
        rate_ferric = K * np.power(self.copper, a) * np.power(self.ferric, b)
        self.update_reactant_concentrations(rate_ferric)
        return rate_ferric

    def update_reactant_concentrations(self, rate_ferric):
        self.copper += rate_ferric/2
        if self.system == constants.BATCH:
            self.ferric += rate_ferric
