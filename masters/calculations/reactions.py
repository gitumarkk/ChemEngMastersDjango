from masters.calculations import constants

import numpy as np

class BioxidationRate(object):
    """
    The initial rate assumes a CSTR
    """
    def __init__(self, ferric_initial, ferrous_initial):
        self.ferric = ferric_initial
        self.ferrous = ferrous_initial

    def inhibited(self):
        pass

    def simplified_hansford(self):
        bacteria_conc = 1
        q_spec_growth_rate = 1

        temp_C_x_q_spec_growth_rate = 1.2e-5 # (mol.m^-3.s^-1)
        K = 5e-3
        rate_ferrous = (temp_C_x_q_spec_growth_rate) / (1 + (K * np.divide(self.ferric, self.ferrous)))
        return rate_ferrous

    def update_reactant_concentrations(self, ferric, ferrous):
        self.ferric = ferric
        self.ferrous = ferrous


class MetalDissolutionRate(object):
    def __init__(self, metal_name, metal_initial, initial_ferric=None, system=None):
        self.metal_name = metal_name
        self.metal_conc = metal_initial
        self.ferric = initial_ferric
        self.system = system or constants.BATCH

    def copper_metal_powder_rate(self):
        # Copper concentration depends on the next step
        K = -0.0042
        a = 0.5
        b = 0.64
        rate_ferric = K * np.power(self.metal_conc, a) * np.power(self.ferric, b)
        self.update_reactant_concentrations(rate_ferric)
        return rate_ferric

    def update_reactant_concentrations(self, rate_ferric):
        self.metal_conc += rate_ferric/2  # 2 for now beacuse of copper

        if self.system == constants.BATCH:
            # This is only updated in teh reactor
            self.ferric += rate_ferric


    def stoichiometry(self):
        """
        equation returns the stoichiometry of the metal vs ferrous, it will
        be used in working out the summation of the sates in the system.
        """
        pass

    def ferric_to_ferrous(self, rate_ferric):
        """
        Converts the ferric rate to ferrous rate
        """
        return rate_ferric * (-1)

    def run(self):
        if self.metal_name == constants.COPPER:
            rate_ferric = self.copper_metal_powder_rate()
            self.update_reactant_concentrations(rate_ferric)
            rate_ferrous = self.ferric_to_ferrous(rate_ferric)
            return rate_ferrous, rate_ferric, self.metal_conc
