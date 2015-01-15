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
        volumes = [1, 10, 1000]
        output = {}
        ferric_biox = {}
        ferric_chem = {}
        cupric_ions = {}


        for volume in volumes:
            sys = system.System(volume, 1, 1000, 9, initial_metals={"Cu": 2})
            sys.build_cyclic_tanks()
            output[volume] = sys.run()

        for k, data in output.iteritems():
            ferric_biox[k] = {"ferric": [], "time": []}
            for row in data["bioxidation"]:
                ferric_biox[k]["ferric"].append(row["ions"]["ferric"])
                ferric_biox[k]["time"].append(row["step"])

        i = 0
        for volume, ferric_data in ferric_biox.iteritems():
            plt.figure(i)
            plt.plot(ferric_data["time"], ferric_data["ferric"])
            i += 1
        plt.show()
