# Django
from django.test import TestCase

# Project
from masters.calculations import system
from masters.calculations import reactors
from masters.calculations import reactions

class TestCreatingReactors(TestCase):
    def setUp(self):
        self.volume = 10 # m3

    def test_creating_cstr_reactor(self):
        upstream = reactors.BaseUpStream()
        cstr = reactors.CSTR(self.volume, upstream)
        self.assertEqual(cstr.flow_in, upstream.flow_out)
        self.assertEqual(cstr.flow_in, cstr.flow_out)

        self.assertIsNotNone(cstr.flow_in)


class TestRunningSystem(TestCase):
    def setUp(self):
        self.volume_cstr = 10 #
        self.upstream_flow_out = {"flowrate": 1, "components": {"C_Fe2_plus": 0.1, "C_Fe3_plus": 0.2}}

    def test_system_runs_okay(self):
        sys = system.System()

        upstream = reactors.BaseUpStream(flow_out=self.upstream_flow_out)
        sys.create_reactor(reactors.CSTR, self.volume_cstr, upstream)

        # Asserts
        self.assertEqual(sys.reactor.volume, self.volume_cstr)
        self.assertEqual(sys.reactor.flow_in, self.upstream_flow_out)
        self.assertEqual(sys.reactor.flow_in, sys.reactor.flow_out)

        # Running the reactor
        output = sys.run_system()


class TestReactionRates(TestCase):
    def setUp(self):
        super(TestReactionRates, self).setUp()

    def test_initial_reactor_running(self):
        copper_conc = 2/65.3
        ferric_conc = 0.0001
        copper = reactions.CopperDissolutionRate(copper_conc, ferric_conc)
        rate_ferric = copper.copper_metal_powder_rate()
