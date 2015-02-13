from masters.calculations import constants

import numpy as np

# Raise all numpy exceptions
np.seterr(all='raise')


class BioxidationRate(object):
    """
    The initial rate assumes a CSTR
    """
    def __init__(self, ferric_initial=None, ferrous_initial=None, initial_cells=7.25e7):
        self.ferric = ferric_initial or 0.
        self.ferrous = ferrous_initial or 0.
        self.reactant_name = "Biomass"
        # self.component_conc = 0.00183439  # Assuming an initial biomass concentration
        self.component_conc = initial_cells * 4.8 * 10e-15 * 1000
        self.reaction_step = 0.0

    def __unicode__(self):
        return u"BIOX"

    def inhibited(self):
        pass

    def calculate_biomass_conc(self):
        return self.cell_number * 4.8 * 10e-15 * 1000

    def update_biomass_concentration(self):
        self.component_conc
        k_d = 0
        K = 0.0024 # Tunde

        # u_max = self.ferrous / (Ks + self.ferrous)
        u_max = (0.13 / 3600.0)

        if self.ferrous == 0:
            rate_biomass = 0.0
        else:
            try:
                rate_biomass = self.component_conc * (u_max  - k_d) / (1 + (K * np.divide(self.ferric, self.ferrous)))
            except Exception, e:
                # import ipdb; ipdb.set_trace()
                raise e

        self.component_conc = self.component_conc + (1.0 * rate_biomass)

    def simplified_hansford(self):
        # q_spec_growth_rate = 23.55 / 3600
        q_spec_growth_rate = 1.0 / 3600

        K = 0.0024 # Tunde
        if self.ferrous == 0:
            rate_ferrous = 0.
        else:
            rate_ferrous = - (self.component_conc * q_spec_growth_rate) / (1 + (K * np.divide(self.ferric, self.ferrous)))
        return rate_ferrous

    def update_global_reactant_concentrations(self, ferric, ferrous):
        self.ferric = ferric
        self.ferrous = ferrous

    def ferric_to_ferrous(self, rate_ferric_or_ferrous):
        """
        Converts the ferric rate to ferrous rate
        """
        return rate_ferric_or_ferrous * (-1)

    def update_step(self, step):
        self.reaction_step = step
        self.step = step

    def run(self):
        rate_ferrous = self.simplified_hansford()
        rate_ferric = self.ferric_to_ferrous(rate_ferrous)

        # This equation changes the biomass concentration
        self.update_biomass_concentration()
        # print self.component_conc

        data = {
            "rate_ferrous": rate_ferrous,
            "rate_ferric": rate_ferric,
            "component_moles": self.component_conc,
        }
        # return rate_ferrous, rate_ferric, 0
        return data


class MetalDissolutionRate(object):
    def __init__(self, metal_name, metal_initial, initial_ferric=None, system=None):
        self.reactant_name = metal_name
        self.metal_initial = metal_initial
        self.component_conc = metal_initial
        self.ferric = initial_ferric or 0.
        self.system = system or constants.BATCH
        self.metal_ion = 0
        self.step = 0
        self.system_step = 0.0
        self.reaction_step = 0.0
        self.metal_ion_previous = 0

    def metal_powder_rate(self):
        # Return 0 rate when the initial metal decreases to negative
        if self.component_conc < 0:
            return 0

        if self.ferric == 0:
            # This is because np.power(self.ferric, beta) = 1 if self.ferric = 0 and beta = 0 i.e. 0^0 = 1
            # Occurs in the case of Zinc
            rate_ferric = 0
        else:
            # rate_ferric = K * np.power(self.component_conc, alpha) * np.power(self.ferric, beta)
            # rate_ferric = K * np.power(self.ferric/self.ferrous, alpha)
            rate_ferric = self.calculate_based_on_conversion()
            # rate_ferric = self.shrinking_core_model()

        self.update_metal_reactant_concentration(rate_ferric)
        self.update_metal_ion_concentration()
        return rate_ferric

    def update_step(self, step):
        self.reaction_step += 1
        self.step = step

    def shrinking_core_model(self):
        K = constants.DATA[self.reactant_name]["equation"]["K"]
        n = constants.DATA[self.reactant_name]["equation"]["n"]
        conc = np.power(self.ferric, n)

        a =  3 * K * conc
        b = - 6 * np.power(K, 2) * np.power(conc, 2) * self.reaction_step
        c =  3 * np.power(K, 3) * np.power(conc, 3) * np.power(self.reaction_step, 2)
        return - (a + b + c) * self.metal_initial

    def calculate_based_on_conversion(self):
        K = constants.DATA[self.reactant_name]["equation"]["K"]
        n = constants.DATA[self.reactant_name]["equation"]["n"]

        if self.reactant_name == "Zn":
            X = 1 - np.exp(- np.power(K * (self.reaction_step + 1), 0.5))
        else:
            X = 1 - (1 - K*np.power(self.ferric, n) * (self.reaction_step + 1))**3
        # if X > 1:
        #     X = 1.

        rate_ferric = - 2 * (X * self.metal_initial - self.metal_ion)/(self.reaction_step+1)
        # rate_ferric = - 2 * (X * self.metal_ion_previous - self.metal_ion)
        return rate_ferric

    def update_metal_reactant_concentration(self, rate_ferric):
        # Problem here is thar for a multi COMPONENT SYSTEM NEED TO UPDATE
        # CONCENTRATIONS FROM OUTSIDE THE SYSTEM
        self.component_conc = self.component_conc + (rate_ferric / float(constants.DATA[self.reactant_name]["stoichiometry"]))

    def update_metal_ion_concentration(self):
        self.metal_ion = self.metal_initial - self.component_conc

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

    def rate_component_reaction(self, rate_ferrous):
        """
        Assuming a stoichiometric ratio of r_Cu2+ = r_Fe2+ / n
        """
        return rate_ferrous / float(constants.DATA[self.reactant_name]["stoichiometry"])


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
            "component_moles": self.component_conc,
            "ion_moles": self.metal_initial - self.component_conc,
            "rate_component": self.rate_component_reaction(rate_ferrous)
        }
        # return rate_ferrous, rate_ferric, self.component_conc #, self.metal_ion
        return data
