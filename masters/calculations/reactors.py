# Third Party
import numpy as np



class BaseUpStream(object):
    """
    This class contains the default upstream component, this is so that
    downstream.flow_in = upstream.flow_out
    """
    def __init__(self, flow_out=None):
        self.flow_out = flow_out or {"flowrate": 1, "components": {"ferrous": 0.1, "ferric": 0.2}}

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
        self.volume = volume  # m3
        self.upstream = upstream  # Setting the upstream unit to allow for extensibility

        # Setting the inwards and outward flow rates
        self.set_flow_in()
        self.set_flow_out()

        # self.flow_in = flow_in  # {"flowrate": 999 /s , components: [(Fe2+, 9 mol/l), (Cu2+, 0.1 mol/l)]}

        # # The flowrate out in the initial case will be assumed to be equal to the flow rate in,
        # # only difference is that the component stream changes

        # self.flow_out = flow_out # {"flowrate": 999 /s , components: [(Fe2+, 9 mol/l), (Cu2+, 0.1 mol/l)]}
        self.components_rate = [] # Array holding the components in the reactor

    def update_component_rate(self, component):
        """
        Function that updates the components rate objects in the reactor
        """
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
            cstr_data["component"] = {"rate_ferrous": rate_ferrous,
                                        "rate_ferric": rate_ferric,
                                        "metal_conc": metal_conc,
                                        "name": component.metal_name}

        cstr_data["total_rate_ferrous"] = cummulative_rate_ferrous
        cstr_data["total_rate_ferric"] = cummulative_rate_ferric

        return cstr_data
        # return r_Fe2_plus

    def update_components_flow_out_after_reaction(self, rates):
        ferrous = self.flow_in["components"]["ferrous"] + rates["total_rate_ferrous"]
        ferric = self.flow_in["components"]["ferric"] + rates["total_rate_ferric"]

        self.flow_out = {"flowrate": self.flow_in["flowrate"],
                        "components": {"ferrous ": ferrous , "ferric": ferric}}

    def set_upstream(self, upstream):
        """
        Function to set the upstream component
        """
        self.upstream = upstream
        self.set_flow_in()

    def set_flow_in(self):
        """
        Function to set the inwar flow rate according to the upstream
        """
        self.flow_in = self.upstream.flow_out

    def set_flow_out(self):
        """
        Function to set the outward flow rate according to the upstream
        """
        self.flow_out = self.flow_in

    def run(self):
        cstr_data = self.reaction()
        self.update_components_flow_out_after_reaction(cstr_data)
        return {"cstr_data": cstr_data, "flow_out": self.flow_out}
