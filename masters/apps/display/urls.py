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

    url(r'^reaction_rates/(?P<rate_type>.+)/$',
        'masters.apps.display.views.reaction_rates',
        name='reaction_rates'),

    url(r'^single_reactor/(?P<reactor_type>.+)/$',
        'masters.apps.display.views.single_reactor',
        name='single_reactor'),

    url(r'^system_run/(?P<system_type>.+)/$',
        'masters.apps.display.views.system_run',
        name='system_run'),
)
