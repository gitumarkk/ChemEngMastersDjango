# Project
from json import dumps
import time

# Django
from django.shortcuts import render
from django.http import HttpResponse

# Project
from masters.calculations import system
from masters.calculations import reactors
from masters.calculations import reactions
from masters.calculations import constants
from masters.calculations import export
from masters.calculations import rates


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


# def reaction_rates(request, rate_type=None):
#     data = []

#     if rate_type == "bioxidation":
#         data = run_bioxidation_raction_rates_simulation()
#     elif rate_type == "chemical":
#         data = run_copper_reaction_rates()

#     json_data = dumps(data)
#     return HttpResponse(json_data, content_type='application/json')


def reaction_rates(request, rate_type=None):
    data = []

    if rate_type == "bioxidation":
        data = run_bioxidation_raction_rates_simulation()
    elif rate_type == "chemical":
        rates_type = request.GET.get('rates_type', "ferric")

        copper = rates.RateEquation(constants.COPPER, rates_type=rates_type)
        zinc = rates.RateEquation(constants.ZINC, rates_type=rates_type)
        tin = rates.RateEquation(constants.TIN, rates_type=rates_type)

        copper_data = copper.run()
        zinc_data = zinc.run()
        tin_data = tin.run()

        data = {
            constants.COPPER: copper_data,
            constants.ZINC: zinc_data,
            constants.TIN: tin_data
        }

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
    data = process_get_parameters(request, system_type)
    if not data:
        data = {"success": False,
                "message": "Please choose attleast one metal conc",
                "type": "error"}
    json_data = dumps(data)
    print "complete"
    return HttpResponse(json_data, content_type='application/json')

def export_data(request, system_type=None):
    print "started"
    data = process_get_parameters(request, system_type)
    _export = export.ExportToExcel(data)
    wb_data = _export.run()

    fname = "%s_%s" % (system_type, int(time.time() * 100000))
    response = HttpResponse(wb_data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % fname
    print "complete"
    return response

def process_get_parameters(_request, _system_type):
    ferricFerrousRatio = _request.GET.get('ferricFerrousRatio', 0)
    chemicalVolume = _request.GET.get('chemicalVolume', 0)
    bioxidationVolume = _request.GET.get('bioxidationVolume', 0)
    totalIron = _request.GET.get("totalIron", 0)
    # initialCopper = _request.GET.get('initialCopper', 0)

    initial_metals = {
        "Cu": float(_request.GET.get('Cu', 0)),
        "Sn": float(_request.GET.get('Sn', 0)),
        "Zn": float(_request.GET.get('Zn', 0)),
    }

    if sum([v for k,v in initial_metals.iteritems()]) == 0:
        return False

    sys = system.System(float(bioxidationVolume),
                            float(chemicalVolume),
                            float(ferricFerrousRatio),
                            float(totalIron),
                            initial_metals=initial_metals)

    data = []
    if _system_type == "tanks_in_series":
        sys.build_tanks_in_series()

    if _system_type == "closed_cyclic":
        sys.build_cyclic_tanks()

    data = sys.run()
    return data

def run_copper_reaction_rates():
    copper_conc = 0.064
    ferric_conc = 0.171
    copper = reactions.MetalDissolutionRate(constants.COPPER, copper_conc, ferric_conc)
    data = []
    i = 0
    while copper.ferric > 1e-9 and copper.component_conc > 1e-9:
        temp = {}
        # rate_ferrous, rate_ferric, copper_component_conc  = copper.run()
        output = copper.run()
        temp = {"ferric": copper.ferric,  "step": i, "copper": output["component_moles"], "cupric": output["ion_moles"]}
        temp.update(output)
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
            # rate_ferrous, rate_ferric, component_conc = biox_reaction.run()
            output = biox_reaction.run()

            ferric_ferrous = np.divide(ferric, ferrous)

            temp = {"ferric_ferrous": ferric_ferrous, "step": i}
            temp.update(output)
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
    cstr.create_components(metal_rate)
    i = 0
    # metal_rate.ferric > 1e-9 and metal_rate.component_conc > 1e-9
    while True:
        temp = {}

        cstr_data = cstr.run()
        # print metal_rate.ferric, metal_rate.component_conc
        if metal_rate.ferric < 1e-9 or metal_rate.component_conc < 1e-9:
            break

        temp = {"step": i}
        temp.update(cstr_data)
        data.append(temp)

        i = i + 1

    return data
