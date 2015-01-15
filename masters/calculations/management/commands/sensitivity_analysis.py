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
        time = []

        for volume in volumes:
            sys = system.System(volume, 1, 1000, 9, initial_metals={"Cu": 2})
            sys.build_cyclic_tanks()
            output[volume] = sys.run()
        print output[1]["bioxidation"][0]["ions"]
        print output[1]["bioxidation"][0]["flow_out"]

        for k, data in output.iteritems():
            ferric_biox[k] = []
            for row in data["bioxidation"]:
                ferric_biox[k].append(row["ions"]["ferric"])
                time.append(row["step"])

        i = 0
        # for volume, ferric in ferric_biox.iteritems():
        #     plt.figure(i)
        #     plt.plot(time, ferric)
        #     i += 1

        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        import ipdb; ipdb.set_trace()
        ax1.plot(time, ferric_biox[1])

        plt.show()
