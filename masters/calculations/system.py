# This module define the entire system and links the reactors together
# Python
import time

# Project
from masters.calculations import reactors
from masters.calculations import reactions
from masters.calculations import constants


class System(object):
    def __init__(self, biox_volume, chem_volume, ferric_ferrous, total_iron, initial_metals={}, initial_cells=7.25e7, additions=False):
        self.units = []
        self.biox_volume = biox_volume or 1.0
        self.chem_volume = chem_volume or 1.0
        self.initial_cells = initial_cells
        # self.initial_copper = (initial_copper or 2) / 63.5  # Need to divide by Volume / self.chem_volume
        self.ferric_ferrous = ferric_ferrous or 1000.0
        self.total_iron = (9.0 or total_iron) # Converting to g/m^3

        self.ferrous = self.calculate_initial_ferrous_conc() / 55.85
        self.ferric = self.calculate_initial_ferric_conc() / 55.85

        self.initial_metals = self.convert_initial_metals_to_moles(initial_metals)

        self.img = None
        self.system_type = None
        self.system_components = [] # List of all the ions in the system

        self.FINAL_CONVERSION = 0.95

        # Addition
        self.additions = additions
        self.additions_index = 1

        self.MAX_TIME = 90 if self.additions else 10 # seconds

    def convert_initial_metals_to_moles(self, initial_metals):
        for k, v in initial_metals.iteritems():
            initial_metals[k] = v / constants.DATA[k]["Mr"]
        return initial_metals

    def calculate_initial_ferric_conc(self):
        return (self.total_iron * self.ferric_ferrous) / (self.ferric_ferrous + 1.0)

    def calculate_initial_ferrous_conc(self):
        return self.total_iron / (self.ferric_ferrous + 1.0)

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

    def add_reactants_to_chem_cstr(self):
        for k, v in self.initial_metals.iteritems():
            metal = reactions.MetalDissolutionRate(
                        k,
                        v,
                        system=constants.CONTINUOUS
                    )
            self.chem_cstr.create_components(metal)
            self.system_components.append(metal.reactant_name)

    def build_tanks_in_series(self):
        # Setting up the biox reactor
        self.upstream = reactors.BaseUpStream(ferric=self.ferric,
                                              ferrous=self.ferrous,
                                              ratio=self.ferric_ferrous)
        self.biox_rate = reactions.BioxidationRate(initial_cells=self.initial_cells)
        self.biox_cstr = self.create_reactor(reactors.CSTR, self.biox_volume, self.upstream)
        self.biox_cstr.create_components(self.biox_rate)

        self.system_components.append(self.biox_rate.reactant_name)

        # Setting up the Chemical Reactor
        # self.copper_rate = reactions.MetalDissolutionRate(
        #                                     constants.COPPER,
        #                                     self.initial_copper,
        #                                     system=constants.CONTINUOUS)
        self.chem_cstr = self.create_reactor(reactors.CSTR, self.chem_volume, self.biox_cstr)
        self.add_reactants_to_chem_cstr()
        # self.chem_cstr.create_components(self.copper_rate)
        # That the system can be aware of all ions/ reactants
        # self.system_components.append(self.copper_rate.reactant_name)

        self.add_system_ions_to_reactors()
        self.img = "/static/img/system/tanks_in_series.png"
        self.system_type = "Tanks in Series"

    def build_cyclic_tanks(self):

        # This is temporary as once the chemical reactor is built,
        # the upstream will be updated
        upstream = reactors.BaseUpStream(ferric=self.ferric,
                                         ferrous=self.ferrous,
                                         ratio=self.ferric_ferrous)

        # Building the Bioxidation Reactor
        self.biox_rate = reactions.BioxidationRate(initial_cells=self.initial_cells)
        self.biox_cstr = self.create_reactor(reactors.CSTR, self.biox_volume, upstream)
        self.biox_cstr.create_components(self.biox_rate)
        self.system_components.append(self.biox_rate.reactant_name)

        # Setting up the Chemical Reactor
        # self.copper_rate = reactions.MetalDissolutionRate(
        #                                     constants.COPPER,
        #                                     self.initial_copper,
        #                                     system=constants.CONTINUOUS)
        self.chem_cstr = self.create_reactor(reactors.CSTR, self.chem_volume, self.biox_cstr)
        # self.chem_cstr.create_components(self.copper_rate)
        # self.system_components.append(self.copper_rate.reactant_name)
        self.add_reactants_to_chem_cstr()

        # Updating the biox_cstr upstream
        self.biox_cstr.upstream = self.chem_cstr
        self.biox_cstr.update_flow_in()

        self.add_system_ions_to_reactors()
        self.img = "/static/img/system/closed_loop.png"
        self.system_type = "Closed Cyclic Tanks"

    def add_system_ions_to_reactors(self):
        for unit in self.units:
            unit.create_ions_in_reactor(self.system_components)

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

    def convert_to_minutes(self, i):
        return i / 60.0

    def check_conversion_above_threshhold(self):
        """
        Checks if the cummulative conversion is over the specified threshold
        """
        total_initial_conc = sum([v for k,v in self.initial_metals.iteritems()])
        total_current_conc = sum([ component.component_conc for component in self.chem_cstr.components])
        # print total_initial_conc, total_current_conc
        return total_current_conc < ((1 - self.FINAL_CONVERSION) * total_initial_conc)

    def update_step_in_units(self, step):
        for unit in self.units:
            unit.step = step

    def additions_update(self):
        self.chem_cstr.components[0].component_conc = 4.0 / 63.55
        self.initial_metals["Cu"] = 4.0 / 63.55
        self.chem_cstr.components[0].metal_ion = 0.0
        self.chem_cstr.components[0].reaction_step = 0
        self.additions_index += 1

    def check_ferrous_ion_above_threshold(self):
        return self.biox_cstr.ions["ferric"] >= self.ferric

    def run(self):
        biox_list = []
        chem_list = []
        summary_list = []

        t0 = time.clock()

        i = 0
        while True:
            # temp = {}
            self.update_step_in_units(i)
            sys_data = self.step()

            # Should be sum of the metal concentrations
            # If sum(self.metals_rate) < sum(self.initial_rates)
            metal_converted = self.check_conversion_above_threshhold()
            if self.additions:
                if metal_converted and self.check_ferrous_ion_above_threshold():
                    if self.additions_index < 6:
                        self.additions_update()
                    else:
                        status = {"success": True, "message": "Simulation completed succesfully"}
                        break
            else:
                if metal_converted:
                    status = {"success": True, "message": "Simulation completed succesfully"}
                    break


            if time.clock() - t0 > self.MAX_TIME:
                status = {"success": False, "message": "Simulation reached max time of %s" % self.MAX_TIME}
                break

            # final_copper_conc = self.copper_rate.component_conc
            final_component_conc = {component.reactant_name: component.component_conc for component in self.chem_cstr.components}

            sys_data[0].update({"step": self.convert_to_minutes(i)})
            sys_data[1].update({"step": self.convert_to_minutes(i)})

            biox_list.append(sys_data[0])
            chem_list.append(sys_data[1])

            try:
                summary_list.append({"step": self.convert_to_minutes(i),
                                "rate_ratio": abs(sys_data[1]["cstr_data"]["total_rate_ferric"] / sys_data[0]["cstr_data"]["total_rate_ferric"])})
            except Exception, e:
                # import ipdb; ipdb.set_trace()
                raise e


            i = i + 1

        _data = {"bioxidation": biox_list,
                 "chemical": chem_list,
                 "summary": {"bioxidation": {"ferric_in": self.biox_cstr.flow_in["components"]["ferric"],
                                             "ferrous_in": self.biox_cstr.flow_in["components"]["ferrous"],
                                             "volume": self.biox_volume,
                                             "equation": "",
                                             "dilution": self.biox_cstr.get_dilution_rate()},
                             "chemical": {"initial_component_conc": self.initial_metals,
                                           "final_component_conc": final_component_conc,
                                           # "conversion": (self.initial_copper - final_copper_conc) / self.initial_copper,
                                           "volume": self.chem_volume,
                                           "equation": "",
                                           "dilution": self.chem_cstr.get_dilution_rate()},
                            "combined": {"VChem_VBiox": self.chem_volume/self.biox_volume,
                                         "System Type": self.system_type},
                            "system": {"img": self.img},
                            "status": status,
                            "data": summary_list
                            }
                }
        return _data
