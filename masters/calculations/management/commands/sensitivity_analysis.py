# Python
from optparse import make_option

# Django
from django.core.management.base import BaseCommand

# Project
from masters.calculations import system

# Third party
import matplotlib.pyplot as plt


class Command(BaseCommand):
    # help = "Which simulation do you want to run, --volume, --initial_mass, --ferric_ferrous"
    # option_list = BaseCommand.option_list + (
    #     make_option('--total', dest='total', type='str', default="--volume",
    #                     help='How many families to create'),)

    def handle(self, *args, **kwargs):
        self.volume_sensitivity_analysis()

    def volume_sensitivity_analysis(self):
        volumes = [1, 10, 1000]
        output = {}
        ferric_biox = {}
        ferric_chem = {}
        cupric_chem = {}


        for volume in volumes:
            sys = system.System(volume, 1, 1000, 9, initial_metals={"Cu": 20})
            sys.build_cyclic_tanks()
            output[volume] = sys.run()

        for k, data in output.iteritems():
            ferric_biox[k] = {"ferric": [], "time": []}
            for row in data["bioxidation"]:
                ferric_biox[k]["ferric"].append(row["ions"]["ferric"])
                ferric_biox[k]["time"].append(row["step"])

            ferric_chem[k] = {"ferric": [], "time": []}
            for row in data["chemical"]:
                ferric_chem[k]["ferric"].append(row["ions"]["ferric"])
                ferric_chem[k]["time"].append(row["step"])

            cupric_chem[k] = {"cupric": [], "time": []}
            for row in data["chemical"]:
                cupric_chem[k]["cupric"].append(row["ions"]["Cu"])
                cupric_chem[k]["time"].append(row["step"])

        i = 0
        # for volume, ferric_data in ferric_biox.iteritems():
        #     plt.figure(i)
        #     plt.plot(ferric_data["time"], ferric_data["ferric"])
        #     i += 1

        fig = plt.figure(1)
        fig.suptitle("ferric ion concentration in biooxidation reactor")
        ax = fig.add_subplot(111)

        ax.set_xlabel("Time (min)")
        ax.set_ylabel("Ferric ion concentration (mol/l)")

        ax.plot(ferric_biox[1]["time"], ferric_biox[1]["ferric"], label="1 L")
        ax.plot(ferric_biox[10]["time"], ferric_biox[10]["ferric"], 'r--', label="10 L")
        ax.plot(ferric_biox[1000]["time"], ferric_biox[1000]["ferric"], label="1000 L")
        plt.legend()


        fig = plt.figure(2)
        fig.suptitle("ferric ion concentration in Metal dissolution reactor")
        ax = fig.add_subplot(111)

        ax.set_xlabel("Time (min)")
        ax.set_ylabel("Ferric ion concentration (mol/l)")

        ax.plot(ferric_chem[1]["time"], ferric_chem[1]["ferric"], label="1 L")
        ax.plot(ferric_chem[10]["time"], ferric_chem[10]["ferric"], 'r--', label="10 L")
        ax.plot(ferric_chem[1000]["time"], ferric_chem[1000]["ferric"], label="1000 L")

        plt.legend()


        fig = plt.figure(3)
        fig.suptitle("cupric ion concentration in Metal dissolution reactor")
        ax = fig.add_subplot(111)

        ax.set_xlabel("Time (min)")
        ax.set_ylabel("Cupric ion concentration (mol/l)")

        ax.plot(cupric_chem[1]["time"], cupric_chem[1]["cupric"], label="1 L")
        ax.plot(cupric_chem[10]["time"], cupric_chem[10]["cupric"], 'r--', label="10 L")
        ax.plot(cupric_chem[1000]["time"], cupric_chem[1000]["cupric"], label="1000 L")

        plt.legend()
        plt.show()
