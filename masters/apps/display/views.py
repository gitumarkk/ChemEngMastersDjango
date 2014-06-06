# Project
from json import dumps

# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse

# Project
from masters.calculations import system
from masters.calculations import reactors
from masters.calculations import reactions
from masters.calculations import constants

# Third Party
import numpy as np


def home(request):
    context = {}
    return render(request,
                  "display/home.html",
                  context)


def simulation(request):
    context = {}
    return render(request,
                  "display/simulation.html",
                  context)

def bioleach_reactor(request):
    sys = System()

    upstream = reactors.BaseUpStream()
    sys.create_reactor(reactors.CSTR, 10, upstream)

    data = sys.run_system()

    json_data = dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def reaction_rates(request, rate_type=None):
    data = []

    if rate_type == "bioxidation":
        data = run_bioxidation_raction_rates_simulation()
    elif rate_type == "chemical":
        data = run_copper_reaction_rates()

    json_data = dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def single_reactor(request, reactor_type=None):
    data = []

    if reactor_type == "chemical":
        data = run_chemical_single_reactor()
    json_data = dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def system_run(request, system_type=None):
    print "started"
    data = []
    if system_type == "tanks_in_series":
        data = tanks_in_series()
    json_data = dumps(data)

    print "complete"
    return HttpResponse(json_data, content_type='application/json')

def run_copper_reaction_rates():
    copper_conc = 0.064
    ferric_conc = 0.171
    copper = reactions.MetalDissolutionRate(constants.COPPER, copper_conc, ferric_conc)
    data = []
    i = 0
    while copper.ferric > 1e-9 and copper.metal_conc > 1e-9:
        temp = {}
        rate_ferrous, rate_ferric, copper_metal_conc  = copper.run()
        temp = {"ferric": copper.ferric, "rate_ferric": rate_ferric, "step": i, "copper": copper_metal_conc}
        data.append(temp)
        i = i + 1
    return data


def run_bioxidation_raction_rates_simulation():
    biox_reaction = reactions.BioxidationRate(0, 0)
    data = []

    RANGE = 1000
    for i in range(RANGE):
        temp = {}

        ferric = (i * 1.0/RANGE)
        ferrous = (1 - (i * 1.0/RANGE))

        biox_reaction.update_global_reactant_concentrations(ferric, ferrous)

        if not ferric == 0: # Avoid division by zero error
            np.seterr(divide='ignore')
            rate_ferrous, rate_ferric, metal_conc = biox_reaction.run()

            ferric_ferrous = np.divide(ferric, ferrous)

            temp = {"ferric_ferrous": ferric_ferrous, "rate_ferrous": rate_ferrous, "step": i}
            data.append(temp)
    return data

def run_chemical_single_reactor():
    data = []

    volume = 1 # m3
    copper_conc = 4 / 63.5

    upstream = reactors.BaseUpStream()
    cstr = reactors.CSTR(volume, upstream)
    metal_rate = reactions.MetalDissolutionRate(constants.COPPER,
                                                 copper_conc,
                                                 upstream.flow_out["components"]["ferric"],
                                                 system=constants.CONTINUOUS)
    cstr.update_component_rate(metal_rate)
    i = 0
    # metal_rate.ferric > 1e-9 and metal_rate.metal_conc > 1e-9
    while True:
        temp = {}

        cstr_data = cstr.run()
        # print metal_rate.ferric, metal_rate.metal_conc
        if metal_rate.ferric < 1e-9 or metal_rate.metal_conc < 1e-9:
            break

        temp = {"step": i}
        temp.update(cstr_data)
        data.append(temp)

        i = i + 1

    return data

def tanks_in_series():
    data = []
    biox_volume = 1
    chem_volume = 1
    copper_conc = final_copper_conc = 2 / 63.5  # mol.m^-3
    # Initializing the system
    sys = system.System()

    # Setting up the biox reactor
    upstream = reactors.BaseUpStream()
    biox_rate = reactions.BioxidationRate()
    biox_cstr = sys.create_reactor(reactors.CSTR, biox_volume, upstream)
    biox_cstr.update_component_rate(biox_rate)

    # Setting up the Chemical Reactor
    copper_rate = reactions.MetalDissolutionRate(constants.COPPER,
                                                copper_conc,
                                                system=constants.CONTINUOUS)
    chem_cstr = sys.create_reactor(reactors.CSTR, chem_volume, biox_cstr)
    chem_cstr.update_component_rate(copper_rate)

    biox_list = []
    chem_list = []

    i = 0
    while True:
        # temp = {}
        sys_data = sys.run()

        if copper_rate.metal_conc < 1e-9:
            break

        final_copper_conc = copper_rate.metal_conc

        sys_data[0].update({"step": i})
        sys_data[1].update({"step": i})

        biox_list.append(sys_data[0])
        chem_list.append(sys_data[1])

        i = i + 1
    # print ""
    # print ""
    # print "BIOXIDATION VOLUME: " + str(biox_volume)
    # print "BIOXIDATION DILUTION RATE: " + str(biox_cstr.get_dilution_rate())
    # print "CHEMICAL VOLUME: " + str(chem_volume)
    # print "CHEMICAL RATE: " + str(chem_cstr.get_dilution_rate())
    # print "INITIAL FERRIC CONC"
    # print upstream.flow_out

    _data = {"bioxidation": biox_list,
             "chemical": chem_list,
             "summary": {"bioxidation": {"ferric_in": biox_cstr.flow_in["components"]["ferric"],
                                         "ferrous_in": biox_cstr.flow_in["components"]["ferrous"],
                                         "volume": biox_volume},
                         "chemical": {"initial_copper_conc": copper_conc,
                                       "final_copper_conc": final_copper_conc,
                                       "volume": chem_volume},
                        "combined": {"VChem_VBiox": chem_volume/biox_volume}
                        }
             }
    return _data
