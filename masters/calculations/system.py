# This module define the entire system and links the reactors together

# Project
from masters.calculations import reactors

# Third Party
import numpy as np


class System(object):
    def __init__(self):
        pass

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
            temp = {"_r_Fe_2p": [], "Fe_3p_Fe_2p": [], "step": []}

            temp_flow = {"flowrate": 1.0,
                        "components": {"C_Fe2_plus": (i * 1.0/RANGE), "C_Fe3_plus": (1 - (i * 1.0/RANGE))}}

            self.reactor.upstream.set_flow_out(temp_flow)

            self.reactor.set_upstream(self.reactor.upstream)

            # Ignore case when C_Fe2_plus is 0
            if not self.reactor.flow_in["components"]["C_Fe2_plus"] == 0:
                np.seterr(divide='ignore')
                _r_Fe_2p = self.reactor.reaction()
                Fe_3p_Fe_2p = np.divide(self.reactor.flow_in["components"]["C_Fe3_plus"], self.reactor.flow_in["components"]["C_Fe2_plus"])

                temp["_r_Fe_2p"] = _r_Fe_2p
                temp["Fe_3p_Fe_2p"] = Fe_3p_Fe_2p
                temp["step"] = i
                output.append(temp)
        return output
