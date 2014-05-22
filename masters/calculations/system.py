# This module define the entire system and links the reactors together

# Project
from masters.calculations import reactors

# Third Party
import numpy as np


class System(object):
    def __init__(self):
        self.units = []

    def create_reactor(self, reactor, volume, upstream):
        # This will be used to add a reactor to the system
        # The reactor will reference upstream and downstream linkages
        volume = volume

        # upstream = reactors.BaseUpStream()
        self.reactor = reactor(volume, upstream)

    def run_system(self):
        """
            This is used to run the system, initially it can be defined as a flowrate
            or a time based thing, initially it will be flow rate based.
        """
        output = []

        RANGE = 1000
        for i in range(RANGE):
            temp = {}

            temp_flow = {"flowrate": 1.0,
                        "components": {"C_Fe2_plus": (i * 1.0/RANGE), "C_Fe3_plus": (1 - (i * 1.0/RANGE))}}

            self.reactor.upstream.set_flow_out(temp_flow)

            self.reactor.set_upstream(self.reactor.upstream)

            # Ignore case when C_Fe2_plus is 0
            if not self.reactor.flow_in["components"]["C_Fe2_plus"] == 0:
                np.seterr(divide='ignore')
                rate_ferrous = self.reactor.reaction()
                Fe_3p_Fe_2p = np.divide(self.reactor.flow_in["components"]["C_Fe3_plus"], self.reactor.flow_in["components"]["C_Fe2_plus"])

                temp["rate_ferrous"] = rate_ferrous
                temp["Fe_3p_Fe_2p"] = Fe_3p_Fe_2p
                temp["step"] = i
                output.append(temp)
        return output

    def run(self):
        """
        output is in the form of [{"reactor": ["", [""]]}]
        """
        output = []
        return output


    def update_units(self, unit):
        self.units.append(unit)
