# Third Party
import numpy as np



class BaseUpStream(object):
    """
    This class contains the default upstream component, this is so that
    downstream.flow_in = upstream.flow_out
    """
    def __init__(self, flow_out=None):
        self.flow_out = flow_out or {"flowrate": 1, "components": {"C_Fe2_plus": 0.1, "C_Fe3_plus": 0.2}}

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
    This system uses Fe2+ as the base
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
        self.components = [] # Array holding the components in the reactor

    def update_component_stream(self, component):
        self.components.append(component)

    def reaction(self):
        C_x = 1
        q_spec_growth_rate = 1

        C_Fe2_plus = self.flow_in["components"]["C_Fe2_plus"]
        C_Fe3_plus = self.flow_in["components"]["C_Fe3_plus"]

        temp_C_x_q_spec_growth_rate = 1.2e-5 # (mol.m^-3.s^-1)
        K = 5e-3

        r_Fe2_plus = (temp_C_x_q_spec_growth_rate) / (1 + (K * np.divide(C_Fe3_plus, C_Fe2_plus)))

        self.update_flow_out_after_reaction(r_Fe2_plus)
        return r_Fe2_plus

    def update_flow_out_after_reaction(self, r_Fe2_plus):
        C_Fe2_plus = self.flow_in["components"]["C_Fe2_plus"] + r_Fe2_plus
        C_Fe3_plus = self.flow_in["components"]["C_Fe3_plus"] - r_Fe2_plus

        self.flow_out = {"flowrate": self.flow_in["flowrate"],
                        "components": {"C_Fe2_plus": C_Fe2_plus, "C_Fe3_plus": C_Fe3_plus}}

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
