# Project
from json import dumps

# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse

# Project
from masters.calculations.system import System
from masters.calculations import reactors
from masters.calculations import reactions

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


def copper_reaction_rates(request):
    copper_conc = 0.064
    ferric_conc = 0.171
    copper = reactions.CopperDissolutionRate(copper_conc, ferric_conc)
    data = []
    i = 0
    while copper.ferric > 1e-9 and copper.copper > 1e-9:
        temp = {}
        rate_ferric = copper.copper_metal_powder_rate()
        temp = {"ferric": copper.ferric, "rate_ferric": rate_ferric, "step": i, "copper": copper.copper}
        data.append(temp)
        i = i + 1

    json_data = dumps(data)
    return HttpResponse(json_data, content_type='application/json')
