# This module define the entire system and links the reactors together

# Project
from masters.calculations import reactors
from masters.calculations import reactions
from masters.calculations import constants

# Third Party
import numpy as np


class System(object):
    def __init__(self, biox_volume, chem_volume, initial_copper, ferric_ferrous, total_iron):
        self.units = []
        self.biox_volume = biox_volume or 1
        self.chem_volume = chem_volume or 1
        self.initial_copper = (initial_copper or 2) / 63.5  # Converting to moles / l
        self.ferric_ferrous = ferric_ferrous or 1000
        self.total_iron = (9 or total_iron) / 1000 # Converting to g/m^3

        self.ferrous = (self.total_iron / self.ferric_ferrous) / 55.85
        self.ferric = (self.total_iron * self.ferric_ferrous) / 55.85

        self.img = None

    def create_reactor(self, reactor, volume, upstream):
        # This will be used to add a reactor to the system
        # The reactor will reference upstream and downstream linkages
        volume = volume

        # upstream = reactors.BaseUpStream()
        reactor = reactor(volume, upstream)
        self.update_units(reactor)
        return reactor

    def update_units(self, unit):
        # Can be a reactor, pump or whatever
        self.units.append(unit)

    def build_tanks_in_series(self):
        # Setting up the biox reactor
        self.upstream = reactors.BaseUpStream(ferric=self.ferric,
                                              ferrous=self.ferrous,
                                              ratio=self.ferric_ferrous)
        self.biox_rate = reactions.BioxidationRate()
        self.biox_cstr = self.create_reactor(reactors.CSTR, self.biox_volume, self.upstream)
        self.biox_cstr.update_component_rate(self.biox_rate)

        # Setting up the Chemical Reactor
        self.copper_rate = reactions.MetalDissolutionRate(
                                            constants.COPPER,
                                            self.initial_copper,
                                            system=constants.CONTINUOUS)
        chem_cstr = self.create_reactor(reactors.CSTR, self.chem_volume, self.biox_cstr)
        chem_cstr.update_component_rate(self.copper_rate)

        self.img = ""

    def build_cyclic_tanks(self):
        pass

    def step(self):
        """
        output is in the form of [{"reactor": ["", [""]]}]
        Assuming an ordered list where the reactors in the list is in the order it was created
        """
        # for unit in self.units:
        #     unit.run()
        # import ipdb; ipdb.set_trace()
        output = [unit.run() for unit in self.units]
        return output

    def run(self):
        biox_list = []
        chem_list = []

        i = 0
        while True:
            # temp = {}
            sys_data = self.step()

            if self.copper_rate.metal_conc < 1e-9:
                break

            final_copper_conc = self.copper_rate.metal_conc

            sys_data[0].update({"step": i})
            sys_data[1].update({"step": i})

            biox_list.append(sys_data[0])
            chem_list.append(sys_data[1])

            i = i + 1

        _data = {"bioxidation": biox_list,
                 "chemical": chem_list,
                 "summary": {"bioxidation": {"ferric_in": self.biox_cstr.flow_in["components"]["ferric"],
                                             "ferrous_in": self.biox_cstr.flow_in["components"]["ferrous"],
                                             "volume": self.biox_volume},
                             "chemical": {"initial_copper_conc": self.initial_copper,
                                           "final_copper_conc": final_copper_conc,
                                           "volume": self.chem_volume},
                            "combined": {"VChem_VBiox": self.chem_volume/self.biox_volume}
                            }
                 }
        return _data
