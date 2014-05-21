from django.conf.urls import patterns, url


urlpatterns = patterns('',
    # Examples:
    url(r'^$',
        'masters.apps.display.views.home',
        name='home'),

    url(r'^simulations/$',
        'masters.apps.display.views.simulation',
        name='simulation'),

    url(r'^bioleach_reactor/$',
        'masters.apps.display.views.bioleach_reactor',
        name='bioleach_reactor'),

    url(r'^copper_reaction_rates/$',
        'masters.apps.display.views.copper_reaction_rates',
        name='copper_reaction_rates'),
)
