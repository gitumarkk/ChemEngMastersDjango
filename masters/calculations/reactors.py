# Third Party
import numpy as np



class BaseUpStream(object):
    """
    This class contains the default upstream component, this is so that
    downstream.flow_in = upstream.flow_out
    """
    def __init__(self, ferric=None, ferrous=None, ratio=None, flow_out=None):
        RATIO = ratio or 1000
        # ferrous = 9 / 55.85
        ferric = ferric or 9 / 55.85
        ferrous = ferrous or ferric / RATIO
        self.flow_out = flow_out or {"flowrate": 1. / (1 * 60),  # m^3 / s
                                    "components": {"ferrous": ferrous , "ferric": ferric}}

    def set_flow_out(self, flow_out):
        self.flow_out = flow_out

class CSTRMixin(object):
    """
    This class simulates the cases that occur in all reactors
    """
    def __init__(self, volume, flow_rate_in, flow_rate_out):
        self.volume = volume
        self.flow_rate_in = flow_rate_in
        self.flow_rate_out = flow_rate_out


class BatchReactorMixin(object):
    pass


class CSTR(object):
    """
    This class simulates the cases that occur in all reactors.
    This system uses Fe2+ as the base for all components reactions,
    hence all reactions should be set in the basis of it.
    """
    TYPE = "CSTR"

    def __init__(self, volume, upstream):
        self.volume = volume  # m^3
        self.upstream = upstream  # Setting the upstream unit to allow for extensibility

        self.update_flow_in()  # set the intial flow in to be the same as upstream flow in
        self.set_flow_out_initial()

        self.ferric = self.flow_in["components"]["ferric"]
        self.ferrous = self.flow_in["components"]["ferrous"]
        self.components_rate = [] # Array holding the components in the reactor

    def update_component_rate(self, component):
        """
        Function that updates the components rate objects in the reactor
        """
        component.update_global_reactant_concentrations(self.ferric, self.ferrous)
        self.components_rate.append(component)

    def reaction(self):
        cummulative_rate_ferrous = 0  # Rate is dependent on prevoius concentrations and not
        cummulative_rate_ferric = 0

        cstr_data = {}  # specific rates of the individual op

        # previous rates
        for component in self.components_rate:
            rate_ferrous, rate_ferric, metal_conc = component.run()

            cummulative_rate_ferrous = cummulative_rate_ferrous + rate_ferrous
            cummulative_rate_ferric = cummulative_rate_ferric + rate_ferric

            # Assuming all rates occur once in the system
            cstr_data["components"] = {"rate_ferrous": rate_ferrous,
                                        "rate_ferric": rate_ferric,
                                        "metal_conc": metal_conc,
                                        "name": component.reactant_name}

        cstr_data["total_rate_ferrous"] = cummulative_rate_ferrous
        cstr_data["total_rate_ferric"] = cummulative_rate_ferric

        return cstr_data

    def update_reactor_ferric_and_ferrous_concentration(self, cstr_data):
        """
        This updates the total concentrations of ferric and ferrous in system after reaction

        As the ferric concentration is governed by
        [Fe2+]_out = -rate_ferrous / Dilution rate + [Fe2+]_in
        """

        # By including the dilution rate after the first step, there is a kink in the graph as there is a large drop in
        # Ferrous concentration
        self.ferrous = self.flow_in["components"]["ferrous"] + (cstr_data["total_rate_ferrous"] / self.get_dilution_rate())
        self.ferric = self.flow_in["components"]["ferric"] + (cstr_data["total_rate_ferric"] / self.get_dilution_rate())

        if self.ferric < 0:
            # This means that the ferric concentration is limiting
            self.ferric = 0.

        if self.ferrous < 0:
            # This means that the ferrous concentration is limiting
            self.ferrous = 0

    def update_flow_out_stream(self):
        """
        Updating the outflow stream
        """
        self.flow_out = {"flowrate": self.flow_in["flowrate"],
                        "components": {"ferrous": self.ferrous , "ferric": self.ferric}}

    def update_ferric_concentrations_in_components(self):
        for component in self.components_rate:
            component.update_global_reactant_concentrations(self.ferric, self.ferrous)

    def update_flow_in(self):
        """
        Function to set the inward flow rate according to the upstream
        """
        self.flow_in = self.upstream.flow_out

    def set_flow_out_initial(self):
        """
        Function to set the outward flow rate according to the upstream
        """
        self.flow_out = self.flow_in

    def get_dilution_rate(self):
        return self.flow_in["flowrate"] / self.volume

    def run(self):
        # 1) Update the inflow of the system as the upward flow may have changed
        self.update_flow_in()

        # 2) Run the reatcion
        cstr_data = self.reaction()

        # 3) Update the ferrous and ferric concentration of the system after the reaction
        self.update_reactor_ferric_and_ferrous_concentration(cstr_data)

        # 4) For each component in the reactors update the global ferric concentrations
        self.update_ferric_concentrations_in_components()

        # 5) Update the flow out stream from the CSTR
        self.update_flow_out_stream()

        return {"cstr_data": cstr_data, "flow_out": self.flow_out}
