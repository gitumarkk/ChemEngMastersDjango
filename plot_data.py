from masters.calculations import system

# Third party
import matplotlib.pyplot as plt


def handle(*args, **kwargs):
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
    # for volume, ferric_data in ferric_biox.iteritems():
    #     plt.figure(i)
    #     plt.plot(ferric_data["time"], ferric_data["ferric"])
    #     i += 1


    import ipdb; ipdb.set_trace()
    plt.plot(ferric_biox[1]["time"], ferric_biox[1]["ferric"])
    plt.show()
handle()
