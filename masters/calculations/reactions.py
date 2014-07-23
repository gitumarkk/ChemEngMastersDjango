from masters.calculations import constants

import numpy as np

# Raise all numpy exceptions
np.seterr(all='raise')


class BioxidationRate(object):
    """
    The initial rate assumes a CSTR
    """
    def __init__(self, ferric_initial=None, ferrous_initial=None):
        self.ferric = ferric_initial or 0.
        self.ferrous = ferrous_initial or 0.
        self.reactant_name = "Biomass"
        self.biomass_conc = 1  # Assuming an initial biomass concentration

    def __unicode__(self):
        return u"BIOX"

    def inhibited(self):
        pass

    def update_biomass_concentration(self):
        self.biomass_conc
        Ks = 1
        k_d = 0
        u_max = self.ferrous / (Ks + self.ferrous)
        rate_biomss = self.biomass_conc * (u_max  - k_d)
        self.biomass_conc = self.biomass_conc + (1 * rate_biomss)

    def simplified_hansford(self):
        q_spec_growth_rate = 1

        temp_C_x_q_spec_growth_rate = 1.2e-5 # (mol.m^-3.s^-1)
        K = 5e-3
        rate_ferrous = - (self.biomass_conc * temp_C_x_q_spec_growth_rate) / (1 + (K * np.divide(self.ferric, self.ferrous)))
        return rate_ferrous

    def update_global_reactant_concentrations(self, ferric, ferrous):
        self.ferric = ferric
        self.ferrous = ferrous

    def ferric_to_ferrous(self, rate_ferric_or_ferrous):
        """
        Converts the ferric rate to ferrous rate
        """
        return rate_ferric_or_ferrous * (-1)

    def run(self):
        rate_ferrous = self.simplified_hansford()
        rate_ferric = self.ferric_to_ferrous(rate_ferrous)
        data = {
            "rate_ferrous": rate_ferrous,
            "rate_ferric": rate_ferric
        }
        # return rate_ferrous, rate_ferric, 0
        return data


class MetalDissolutionRate(object):
    def __init__(self, metal_name, metal_initial, initial_ferric=None, system=None):
        self.reactant_name = metal_name
        self.metal_initial = metal_initial
        self.metal_conc = metal_initial
        self.ferric = initial_ferric or 0.
        self.system = system or constants.BATCH
        self.metal_ion = 0

    def metal_powder_rate(self):
        # Return 0 rate when the initial metal decreases to negative
        if self.metal_conc < 0:
            return 0

        K = constants.RATE_DATA[self.reactant_name]["equation"]["k"] # s-1
        alpha = constants.RATE_DATA[self.reactant_name]["equation"]["a"]
        beta = constants.RATE_DATA[self.reactant_name]["equation"]["b"]

        if self.ferric == 0:
            # This is because np.power(self.ferric, beta) = 1 if self.ferric = 0 and beta = 0 i.e. 0^0 = 1
            # Occurs in the case of Zinc
            rate_ferric = 0
        else:
            rate_ferric = K * np.power(self.metal_conc, alpha) * np.power(self.ferric, beta)
        # try:
        # except:
        #     import ipdb; ipdb.set_trace()

        self.update_metal_reactant_concentration(rate_ferric)
        self.update_metal_ion_concentration()
        return rate_ferric

    def update_metal_reactant_concentration(self, rate_ferric):
        # Problem here is thar for a multi COMPONENT SYSTEM NEED TO UPDATE
        # CONCENTRATIONS FROM OUTSIDE THE SYSTEM
        self.metal_conc = self.metal_conc + (rate_ferric / float(constants.RATE_DATA[self.reactant_name]["stoichiometry"]))

    def update_metal_ion_concentration(self):
        self.metal_ion = self.metal_initial - self.metal_conc

    def update_global_reactant_concentrations(self, ferric, ferrous):
        """
        As the ferric concentration is governed by
        [Fe2+]_out = -rate_ferrous / Dilution rate + [Fe2+]_in
        """
        self.ferric = ferric
        self.ferrous = ferrous

    def stoichiometry(self):
        """
        equation returns the stoichiometry of the metal vs ferrous, it will
        be used in working out the summation of the sates in the system.
        """
        pass

    def rate_metal_reaction(self, rate_ferrous):
        """
        Assuming a stoichiometric ratio of r_Cu2+ = r_Fe2+ / n
        """
        return rate_ferrous / float(constants.RATE_DATA[self.reactant_name]["stoichiometry"])


    def ferric_to_ferrous(self, rate_ferric):
        """
        Converts the ferric rate to ferrous rate
        """
        return rate_ferric * (-1)

    def run(self):
        # if self.reactant_name == constants.COPPER["symbol"]:
        rate_ferric = self.metal_powder_rate()

        # This should not be updated here but by the actual reactor
        self.update_metal_reactant_concentration(rate_ferric)
        rate_ferrous = self.ferric_to_ferrous(rate_ferric)

        data = {
            "rate_ferrous": rate_ferrous,
            "rate_ferric": rate_ferric,
            "metal_moles": self.metal_conc,
            "ion_moles": self.metal_initial - self.metal_conc,
            "rate_metal": self.rate_metal_reaction(rate_ferrous)
        }
        # return rate_ferrous, rate_ferric, self.metal_conc #, self.metal_ion
        return data
