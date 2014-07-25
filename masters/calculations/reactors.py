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
        ferric = ferric or 9 / 55.85  # / VOLUME
        ferrous = ferrous or ferric / RATIO
        self.flow_out = flow_out or {"flowrate": 1. / (1 * 60),  # l / s
                                    "components": {"ferrous": ferrous , "ferric": ferric}}

    def set_flow_out(self, flow_out):
        self.flow_out = flow_out


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
        self.components = [] # Array holding the components in the reactor
        self.cstr_data = {}
        self.ions = {}

    def create_components(self, component):
        """
        Function that updates the components rate objects in the reactor
        """
        component.update_global_reactant_concentrations(self.ferric, self.ferrous)
        self.components.append(component)

    def create_ions_in_reactor(self, system_components):
        for component_name in system_components:
            self.ions[component_name] = 0

    def reaction(self):
        cummulative_rate_ferrous = 0  # Rate is dependent on prevoius concentrations and not
        cummulative_rate_ferric = 0

        _cstr_data = {"components": {}}  # specific rates of the individual op

        # previous rates
        for component in self.components:
            # rate_ferrous, rate_ferric, component_conc = component.run()
            output = component.run()
            # rate_component_conc]
            rate_ferrous = output.get("rate_ferrous", 0.)
            rate_ferric = output.get("rate_ferric", 0.)
            rate_component = output.get("rate_component", 0.)
            component_moles = output.get("component_moles", 0.)
            ion_moles = output.get("ion_moles", 0.)

            cummulative_rate_ferrous = cummulative_rate_ferrous + rate_ferrous
            cummulative_rate_ferric = cummulative_rate_ferric + rate_ferric

            _cstr_data["components"][component.reactant_name] = {
                            "rate_ferrous": rate_ferrous,
                            "rate_ferric": rate_ferric,
                            "component_moles": component_moles,
                            "ion_moles": ion_moles,
                            "rate_component": rate_component
                        }

        _cstr_data["total_rate_ferrous"] = cummulative_rate_ferrous
        _cstr_data["total_rate_ferric"] = cummulative_rate_ferric

        return _cstr_data

    def calculate_reactor_ferric_and_ferrous_concentration(self):
        """
        Calculating f(x, y) in the reactor, before applying the (y(t) + h * (f(x, y)))
        (v_chem*C_Fe2+_in - v_chem*C_Fe2+_out  + Vol_chem * total_rate_ferrous)
        """
        flow_diff_ferrous = (self.flow_in["components"]["ferrous"] - self.flow_out["components"]["ferrous"]) * self.get_dilution_rate()
        ferrous_conc = flow_diff_ferrous + self.cstr_data["total_rate_ferrous"]

        flow_diff_ferric = (self.flow_in["components"]["ferric"] - self.flow_out["components"]["ferric"]) * self.get_dilution_rate()
        ferric_conc = flow_diff_ferric + self.cstr_data["total_rate_ferric"]

        return ferrous_conc, ferric_conc

    def calculate_metal_ion_concentrations(self, key):
        """
        calculate y(t+1) by adding y(t) + h * ( f(x, y) )
        """

        if self.flow_in["components"].get(key) == None:
            # print "self.flow_in[components].get(key) == NONE", key
            self.flow_in["components"][key] = 0.0

        # if 0: evaluates to false
        # print self.flow_out["components"], self.flow_out["components"].get(key), key
        if self.flow_out["components"].get(key) == None:
            # print "self.flow_out[components].get(key) == NONE", key
            self.flow_out["components"][key] = 0.0

        # ERROR IS THAT IT ONLY CALCULATES THE CONCENTRATION OF THE CSTR KEY HENCE IF
        # BIOXIDATION REACTOR AND THE KEY IS CU THE FLOW OUT WILL NEVER GET CALCULATED
        # flow_in = self.flow_in["components"] if self.flow_in["components"].get(key) else
        flow_diff = (self.flow_in["components"][key] - self.flow_out["components"][key]) * self.get_dilution_rate()

        # If the system component is part of original reactor components work out rate else work out the flow rate
        if self.cstr_data["components"].get(key):
            ion_conc = flow_diff + self.cstr_data["components"][key]["rate_component"]
        else:
            ion_conc = flow_diff
        # ion_conc = flow_diff + self.cstr_data["components"][key]["rate_component"]
        ion_name = key

        # If self.cstr_data["components"].get(key) == None: ion_conc=flow_dif
        return ion_conc, ion_name

    def perform_euler_calculation(self):
        """
        This updates the total concentrations of ferric and ferrous in system after reaction based on the Euler method
        """
        ferrous_conc, ferric_conc = self.calculate_reactor_ferric_and_ferrous_concentration()
        self.ferrous = self.ferrous + (1 * ferrous_conc) # Assuming step = 1
        self.ferric = self.ferric + (1 * ferric_conc) # Assuming step = 1

        if self.ferric < 0:
            # This means that the ferric concentration is limiting
            self.ferric = 0.

        if self.ferrous < 0:
            # This means that the ferrous concentration is limiting
            self.ferrous = 0

        self.ions["ferric"] = self.ferric
        self.ions["ferrous"] = self.ferrous

        ions = {
            "ferric": self.ferric,
            "ferrous": self.ferrous,
        }

        for key in self.ions.keys():
            if key in ions.keys():  # Do not calculate what has already been calculated
                continue
            ion_conc, ion_name = self.calculate_metal_ion_concentrations(key)
            ion_update = self.ions[ion_name] + (1 * ion_conc)
            ions[ion_name] = ion_update

        # Should be a for loop for a multi-component system
        # ion_conc, ion_name = self.calculate_metal_ion_concentrations()
        # ion_update = self.ions[ion_name] + (1 * ion_conc)

        # Need to create a link to the system components
        # ions = {
        #     "ferric": self.ferric,
        #     "ferrous": self.ferrous,
        #     ion_name: ion_update
        # }

        # Adding the system components to the new output adue to python holding its dict reference
        for k, v in self.ions.iteritems():
            if k not in ions:
                ions[k] = v
        # import ipdb; ipdb.set_trace()
        self.ions = ions


    def update_flow_out_stream(self):
        """
        Updating the outflow stream
        """
        # _comp = {"ferric": self.ferric, "ferrous": self.ferrous, "Cu": self.ions["Cu"], "Bacteria": self.ions["Bacteria"]}
        # _comp = self.ions
        # print self.ions["ferric"] - self.ferric, self.ions["ferrous"] - self.ferrous
        self.flow_out = {"flowrate": self.flow_in["flowrate"],
                        "components": self.ions}

    def update_ferric_concentrations_in_components(self):
        for component in self.components:
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
        self.cstr_data = self.reaction()

        # 3) Update the ferrous and ferric concentration of the system after the reaction
        # self.update_reactor_ferric_and_ferrous_concentration()
        self.perform_euler_calculation()

        # 4) For each component in the reactors update the global ferric concentrations
        self.update_ferric_concentrations_in_components()

        # 5) Update the flow out stream from the CSTR
        self.update_flow_out_stream()

        return {"cstr_data": self.cstr_data,
                "flow_out": self.flow_out,
                "flow_in": self.flow_in,
                "ions": self.ions}
