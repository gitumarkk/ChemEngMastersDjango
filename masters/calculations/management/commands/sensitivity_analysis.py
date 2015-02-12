# Python
from optparse import make_option

# Django
from django.core.management.base import BaseCommand

# Project
from masters.calculations import system

# Third party
import matplotlib.pyplot as plt

CU = 20
FERRIC_FERROUS = 1000
CHEM = 1
BIOX = 1
IRON = 9

class Command(BaseCommand):
    args = "volume"
    help = "Which simulation do you want to run: usage is --simulate volume or --simulate metal or --simulate ferric_ratio"
    # option_list = BaseCommand.option_list + (
    #     make_option('--total', dest='total', type='str', default="--volume",
    #                     help='How many families to create'),)

    option_list = BaseCommand.option_list + (
                    make_option('-s',
                                '--simulate',
                                dest='simulate',
                                default="volume",
                                type="str",
                                help=help),)

    def handle(self, *args, **kwargs):
        if kwargs["simulate"] == "volume":
            self.simulate = "volume"
            self.volume_sensitivity_analysis()

        elif kwargs["simulate"] == "metal":
            self.simulate = "initial_metal"
            self.metal_sensitivity_analysis()

        elif kwargs["simulate"] == "ferric_ratio":
            self.simulate = "ferric_ratio"
            self.ferric_ferrous_sensitivity_analysis()

        elif kwargs["simulate"] == "mixed_metals":
            self.simulate = "mixed_metals"
            self.mixed_metals_sensitivity_analysis()

        elif kwargs["simulate"] == "cells":
            self.simulate = "cells"
            self.microorganism_sensitivity_analysis()

        elif kwargs["simulate"] == "experiments":
            self.simulate = "experiments"
            self.experimental_sensitivity_analysis()


    def experimental_sensitivity_analysis(self):
        analysis_list = [(1, "1 L")]
        output = {}

        for row in analysis_list:
            BIOX = row[0]
            sys = system.System(BIOX, CHEM, FERRIC_FERROUS, IRON, initial_metals={"Cu": CU})
            sys.build_cyclic_tanks()
            output[row[1]] = sys.run()

        self.plot_sensitivity_analysis(output, analysis_list)

    def volume_sensitivity_analysis(self):
        analysis_list = [(1, "1 L"),
                         (3, "3 L"),
                         (6, "6 L"),
                         (9, "9 L"),
                         (12, "12 L"),
                         (1000, "1000 L")]
        output = {}

        for row in analysis_list:
            BIOX = row[0]
            sys = system.System(BIOX, CHEM, FERRIC_FERROUS, IRON, initial_metals={"Cu": CU})
            sys.build_cyclic_tanks()
            output[row[1]] = sys.run()

        self.plot_sensitivity_analysis(output, analysis_list)


    # def metal_sensitivity_analysis(self):
    #     analysis_list = [(2, "2 g Cu"),(10, "10 g Cu"), (20, "20 g Cu")]
    #     default = {"biox": 1, "chem": 1, "ferric_ferrous": 1000}
    #     _analysis_list = [{"Cu": 2, "label": "2 g Cu"},
    #                          {"Cu": 10, "label": "10 g Cu"},
    #                          {"Cu": 20, "label": "20 g Cu"},
    #                          {"Cu": 20, "label": "20 g Cu at 10 L Biooxidation Volume"}]

    #     for item in _analysis_list:
    #         item.update(default)
    #     item[len(item) - 1]["biox"] = 10
    #     self.run_sensitivity_analysis(analysis_list)

    def metal_sensitivity_analysis(self):
        analysis_list = [(2, "2 g Cu"),
                         (5, "5 g Cu"),
                         (10, "10 g Cu"),
                         (15, "15 g Cu"),
                         (20, "20 g Cu")]
        # default = {"biox": 1, "chem": 1, "ferric_ferrous": 1000}
        # ____analysis_list = [{"Cu": 2, "label": "2 g Cu"},(10, "10 g Cu"), (20, "20 g Cu")]

        output = {}
        for row in analysis_list:
            CU = row[0]
            sys = system.System(BIOX, CHEM, FERRIC_FERROUS, IRON, initial_metals={"Cu": CU})
            sys.build_cyclic_tanks()
            output[row[1]] = sys.run()

        sys = system.System(10, 1, FERRIC_FERROUS, IRON, initial_metals={"Cu": 20})
        sys.build_cyclic_tanks()
        output["20 g Cu (10 L Bioox)"] = sys.run()

        analysis_list.append((20, "20 g Cu (10 L Bioox)"))
        self.plot_sensitivity_analysis(output, analysis_list)

    def mixed_metals_sensitivity_analysis(self):
        analysis_list = [(0, "Mixed Metal")]
        ZN = SN = CU = 2
        BIOX = 10

        output = {}
        sys = system.System(BIOX, CHEM, FERRIC_FERROUS, IRON, initial_metals={"Cu": CU, "Sn": SN, "Zn": ZN})
        sys.build_cyclic_tanks()
        output["Mixed Metal"] = sys.run()

        # sys = system.System(10, 1, FERRIC_FERROUS, IRON, initial_metals={"Cu": 20})
        # sys.build_cyclic_tanks()
        # output["20 g Cu at 10 L Bioox. Vol"] = sys.run()

        # analysis_list.append((20, "20 g Cu at 10 L Bioox. Vol"))
        self.plot_sensitivity_analysis(output, analysis_list)

    def ferric_ferrous_sensitivity_analysis(self):
        analysis_list = [(1000, "1000"),
                         (10, "10"),
                         (1, "1"),
                         (0.1, "0.1")]
        # default = {"biox": 1, "chem": 1, "ferric_ferrous": 1000}
        # ____analysis_list = [{"Cu": 2, "label": "2 g Cu"},(10, "10 g Cu"), (20, "20 g Cu")]

        output = {}

        for row in analysis_list:
            FERRIC_FERROUS = row[0]
            sys = system.System(BIOX, CHEM, FERRIC_FERROUS, IRON, initial_metals={"Cu": CU})
            sys.build_cyclic_tanks()
            output[row[1]] = sys.run()

        sys = system.System(10, 1, 0.1, 9, initial_metals={"Cu": CU})
        sys.build_cyclic_tanks()
        output["0.1 (10 L Bioox)"] = sys.run()

        analysis_list.append((20, "0.1 (10 L Bioox)"))
        self.plot_sensitivity_analysis(output, analysis_list)

    def microorganism_sensitivity_analysis(self):
        analysis_list = [(1e4, "1e4"),
                         (1e5, "1e5"),
                         (1e6, "1e6"),
                         (1e7, "1e7"),
                         (1e8, "1e8"),
                         (1e9, "1e9")]
        # default = {"biox": 1, "chem": 1, "ferric_ferrous": 1000}
        # ____analysis_list = [{"Cu": 2, "label": "2 g Cu"},(10, "10 g Cu"), (20, "20 g Cu")]

        output = {}
        CU = 20
        for row in analysis_list:
            BIOMASS = row[0]
            sys = system.System(BIOX, CHEM, FERRIC_FERROUS, IRON, initial_metals={"Cu": CU}, initial_cells=BIOMASS)
            sys.build_cyclic_tanks()
            output[row[1]] = sys.run()

        sys = system.System(10, 1, 0.1, 9, initial_metals={"Cu": CU})
        sys.build_cyclic_tanks()
        self.plot_sensitivity_analysis(output, analysis_list)

    def plot_sensitivity_analysis(self, sys_data, analysis_list):
        ferric_biox = {}
        ferric_chem = {}
        metals_chem = {}

        for k, data in sys_data.iteritems():
            ferric_biox[k] = {"ferric": [], "time": [], "biomass": [], "Cu2+": []}
            for row in data["bioxidation"]:
                ferric_biox[k]["ferric"].append(row["ions"]["ferric"])
                ferric_biox[k]["time"].append(row["step"])
                ferric_biox[k]["biomass"].append(row["cstr_data"]["components"]["Biomass"]["component_moles"])
                ferric_biox[k]["Cu2+"].append(row["flow_out"]["components"]["Cu"])

            ferric_chem[k] = {"ferric": [], "time": []}
            for row in data["chemical"]:
                ferric_chem[k]["ferric"].append(row["ions"]["ferric"])
                ferric_chem[k]["time"].append(row["step"])

            metals_chem[k] = {"Cu2+": [], "time": [], "Zn2+": [], "Sn2+": [], "copper": []}
            for row in data["chemical"]:
                metals_chem[k]["copper"].append(row["cstr_data"]["components"]["Cu"]["component_moles"])
                metals_chem[k]["Cu2+"].append(row["ions"]["Cu"])
                metals_chem[k]["time"].append(row["step"])

                if self.simulate == "mixed_metals":
                    metals_chem[k]["Zn2+"].append(row["ions"]["Zn"])
                    metals_chem[k]["Sn2+"].append(row["ions"]["Sn"])

        # line_choice = ["k", "b--", "r-.", "g:"]

        fig = plt.figure(1, figsize=(8, 8))
        # fig.suptitle("Ferric ion Concentration in Biooxidation Reactor")
        fig_subplot = fig.add_subplot(321)
        fig_subplot.set_xlabel("Time (min)")
        fig_subplot.set_ylabel("[Fe3+] (mol/l)")
        fig_subplot.set_ylim(0, 0.18)
        fig_subplot.set_title("[Fe3+] in Bioox Reactor (A)")
        fig_subplot.grid('on')


        for i, item in enumerate(analysis_list):
            line, = fig_subplot.plot(ferric_biox[item[1]]["time"], ferric_biox[item[1]]["ferric"], label=item[1])
            line.set_linewidth(2)
        # plt.legend(ncol=2, mode="expand", loc=3, borderaxespad=0., bbox_to_anchor=(0., 1.02, 1., .102))
        # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        # fig.savefig('simulation_figures/'+self.simulate+'/ferric_ion_concentration_biooxidation_reactor.png',
        #         bbox_inches='tight')


        fig_subplot = fig.add_subplot(322)
        fig_subplot.set_xlabel("Time (min)")
        fig_subplot.set_ylabel("[Fe3+] (mol/l)")
        fig_subplot.set_ylim(0, 0.18)
        fig_subplot.set_title("[Fe3+] in Chem reactor (B)")
        fig_subplot.grid('on')

        for i, item in enumerate(analysis_list):
            line, = fig_subplot.plot(ferric_chem[item[1]]["time"], ferric_chem[item[1]]["ferric"], label=item[1])
            line.set_linewidth(2)
        # plt.legend(ncol=2, mode="expand", loc=3, borderaxespad=0., bbox_to_anchor=(0., 1.02, 1., .102))
        # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        # fig.savefig('simulation_figures/'+self.simulate+'/ferric_ion_concentration_chemical_reactor.png',
        #             bbox_inches='tight')


        # fig = plt.figure(2, figsize=(8, 8))
        # fig.suptitle("Ferric ion Concentration in Biooxidation Reactor")
        fig_subplot = fig.add_subplot(323)
        fig_subplot.set_xlabel("Time (min)")
        fig_subplot.set_ylabel("[Cu2+] (mol/l)")
        fig_subplot.set_title("[Cu2+] in Bioox Reactor (C)")
        # fig_subplot.set_ylim(0, 0.18)
        fig_subplot.grid('on')

        for i, item in enumerate(analysis_list):
            line, = fig_subplot.plot(ferric_biox[item[1]]["time"], ferric_biox[item[1]]["Cu2+"], label=item[1])
            line.set_linewidth(2)



        # fig = plt.figure(3, figsize=(8, 8))
        # fig.suptitle("Ferric ion concentration in Metal dissolution reactor")


        # fig = plt.figure(4, figsize=(8, 8))
        # fig.suptitle("Cupric Ion Concentration in Metal Dissolution Reactor")
        fig_subplot = fig.add_subplot(324)
        fig_subplot.set_xlabel("Time (min)")
        fig_subplot.set_ylabel("[Cu2+] (mol/l)")
        fig_subplot.set_title("[Cu2+] in Chem Reactor (D)")
        fig_subplot.grid('on')

        for i, item in enumerate(analysis_list):
            label = item[1] if self.simulate != "mixed_metals" else "Copper"
            line, = fig_subplot.plot(metals_chem[item[1]]["time"], metals_chem[item[1]]["Cu2+"], label=label)
            line.set_linewidth(2)

            if self.simulate == "mixed_metals":
                line, = fig_subplot.plot(metals_chem[item[1]]["time"], metals_chem[item[1]]["Zn2+"], label="Zinc")
                line.set_linewidth(2)

                line, = fig_subplot.plot(metals_chem[item[1]]["time"], metals_chem[item[1]]["Sn2+"], label="Tin")
                line.set_linewidth(2)


        fig_subplot = fig.add_subplot(325)
        fig_subplot.set_xlabel("Time (min)")
        fig_subplot.set_ylabel("[Biomass] (mol/l)")
        fig_subplot.set_title("[Biomass] in Bioox Reactor (E)")
        # fig_subplot.set_ylim(0, 0.18)
        fig_subplot.grid('on')

        for i, item in enumerate(analysis_list):
            line, = fig_subplot.plot(ferric_biox[item[1]]["time"], ferric_biox[item[1]]["biomass"], label=item[1])
            line.set_linewidth(2)


        fig_subplot = fig.add_subplot(326)
        fig_subplot.set_xlabel("Time (min)")
        fig_subplot.set_ylabel("[Copper] (mol/l)")
        fig_subplot.set_title("[Copper] in Chem Reactor [F]")
        # fig_subplot.set_ylim(0, 0.18)
        fig_subplot.grid('on')

        for i, item in enumerate(analysis_list):
            line, = fig_subplot.plot(metals_chem[item[1]]["time"], metals_chem[item[1]]["copper"], label=item[1])
            line.set_linewidth(2)


        plt.legend(ncol=3, mode="expand", borderaxespad=0., bbox_to_anchor=(-1.2, -0.3, 1.*2, .102))
        # plt.legend(loc='center left', bbox_to_anchor=(1, 1))
        # plt.subplots_adjust(bottom=0.5)

        plt.tight_layout(h_pad=0.5)
        fig.savefig('simulation_figures/' + self.simulate +'.png',
                    bbox_inches='tight', pad_inches=0.5)


        plt.show()
